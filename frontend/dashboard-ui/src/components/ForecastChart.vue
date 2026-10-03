<script lang="ts">
/**
 * Pre-built chart series for views that assemble their data from
 * other sources than a stored forecast group (e.g. the market view
 * joining forecast and its basis runs). Carries its own timestamps
 * and the metric that resolves the unit.
 */
export interface ChartEntry {
    label: string;
    /** The metric resolving the unit and label. */
    metric: string;
    /** [timestamp, value] pairs; nulls break the line. */
    data: [timestamp: string, value: number | null][];
    dashed?: boolean;
}

export default {};
</script>

<script setup lang="ts">

import { computed } from "vue";
import VChart from "vue-echarts";

import type { WeatherForecast, AssetForecast, PortfolioForecast, TimeSeries } from "../api/forecast";
import type { EnergyMarketForecast } from "../api/energy-market";
import { decodeSeries, type DecodedSeries, type QuantileSeries, type ScalarSeries } from "../api/time-series-decode";
import type { Asset } from "../api/asset";
import type { Portfolio } from "../api/portfolio";

const props = defineProps<{
    /** Omitted when the chart is driven by `entries` instead. */
    forecast?: WeatherForecast|AssetForecast|PortfolioForecast|EnergyMarketForecast,
    forecastType: string,
    asset?: Asset | null,
    portfolio?: Portfolio | null,
    /** Metrics to keep; all series are shown by default. */
    metrics?: string[],
    /** Entry-driven mode; renders the given series as lines. */
    entries?: ChartEntry[],
    /** Chart title override for entry-driven mode. */
    title?: string
}>();
const chartTitle = computed(() => {

    if (props.title) {
        return props.title;
    }

    if (props.asset) {
        return `${props.asset.name} - ${props.forecastType} Forecast`;
    }

    if (props.portfolio) {
        return `${props.portfolio.name} - Portfolio Forecast`;
    }

    if (props.forecast && "market" in props.forecast) {
        return `${props.forecastType}-${props.forecast.market}`;
    }

    return `${props.forecastType} Forecast`;

});

function createTimestamp(
    slotIndex: number
): string {

    if (!props.forecast) {
        throw new Error("No forecast prop to create slot timestamps from");
    }

    const start = new Date(
        props.forecast.forecast.time_series_time_base.start
    );

    const resolution =
        props.forecast.forecast.time_series_time_base.resolution_seconds;


    const timestamp = new Date(
        start.getTime()
        +
        slotIndex * resolution * 1000
    );


    return timestamp.toLocaleString(
        "de-DE",
        {
            day: "2-digit",
            month: "2-digit",
            hour: "2-digit",
            minute: "2-digit"
        }
    );
}

function metricLabel(metric: string): string {

    switch(metric) {

        case "wind_speed":
            return "Windgeschwindigkeit";

        case "temperature":
            return "Temperatur";

        case "cloud_cover":
            return "Bewölkung";

        case "active_power":
            return "Wirkleistung";

        case "day_ahead_electricity_price":
            return "Day-Ahead-Preis";

        default:
            return metric;

    }

}

function metricUnit(metric: string): string {

    switch(metric.split(" ")[0]) {

        case "wind_speed":
            return "m/s";

        case "temperature":
            return "°C";

        case "cloud_cover":
            return "%";

        case "active_power":
            return "kW";
        case "day_ahead_electricity_price":
            return "€/MWh";
        case "global_solar_irradiance":
        case "direct_normal_irradiance":
        case "diffuse_irradiance":
            return "W/m²";

        default:
            return "";

    }

}

/**
 * Chart display strategies.
 *
 * Each strategy turns one decoded API series into ECharts series
 * entries pushed onto `chartSeries`. Data tuples are
 * [timestamp, value, label] — label feeds the tooltip formatter,
 * which resolves the unit from it.
 */
type StrategyFn = (
    series: TimeSeries,
    decoded: DecodedSeries,
    chartSeries: any[]
) => void;

/**
 * Uncertainty band for a 3-quantile series:
 * lower/median traces plus a stacked translucent band between
 * median and each bound. Requires exactly one lower, one median
 * and one upper level (other quantile counts are skipped).
 */
function quantileBandStrategy(
    series: TimeSeries,
    decoded: DecodedSeries,
    chartSeries: any[]
): void {

    if (decoded.kind !== "quantile") {
        throw new Error(`quantileBandStrategy got a ${decoded.kind} series`);
    }

    if (decoded.quantiles.length !== 3
        || decoded.slots.some(slot => slot.values.length !== 3)) {
        console.warn(
            `Series ${series.metric}: expected 3 quantile levels, skipping`
        );
        return;
    }

    // Levels are ascending: lower / median / upper.
    const { labelFor } = decoded;
    const levelLabel = (levelIndex: number) => series.metric + " " + labelFor(levelIndex);
    const lowerLevel = levelLabel(0);
    const medianLevel = levelLabel(1);
    const upperLevel = levelLabel(2);

    const lowerData = decoded.slots.map(slot => [
        createTimestamp(slot.slotIndex),
        slot.values[0],
        lowerLevel
    ]);
    const upperData = decoded.slots.map(slot => [
        createTimestamp(slot.slotIndex),
        slot.values[2],
        upperLevel
    ]);
    const medianData = decoded.slots.map(slot => [
        createTimestamp(slot.slotIndex),
        slot.values[1],
        medianLevel
    ]);

    const lowerBandData = decoded.slots.map(slot => [
        createTimestamp(slot.slotIndex),
        (slot.values[1] as number) - (slot.values[0] as number),
        series.metric
    ]);
    const upperBandData = decoded.slots.map(slot => [
        createTimestamp(slot.slotIndex),
        (slot.values[2] as number) - (slot.values[1] as number),
        series.metric
    ]);

    const bandStack = `${series.metric}-band`;
    const seriesName = `${metricLabel(series.metric)} uncertainty`
    chartSeries.push({ // Lower bound trace
        name: seriesName,//`Quantile ${decoded.labelFor(0)}`,
        type: "line",
        data: lowerData,
        stack: bandStack,
        symbol: "none",
        lineStyle: { opacity: 0.3 },
        areaStyle: { opacity: 0 }
    });
    chartSeries.push({ // Translucent area between lower bound and median
        name: seriesName,//`Area ${decoded.labelFor(0)}-${decoded.labelFor(1)}`,
        ...bandAreaEntry(bandStack, lowerBandData)
    });
    chartSeries.push({ // Translucent area between upper bound and median
        name: seriesName,//`Area ${decoded.labelFor(1)}-${decoded.labelFor(2)}`,
        ...bandAreaEntry(bandStack, upperBandData)
    });
    chartSeries.push({ // Median line
        name: seriesName,//`Quantile ${decoded.labelFor(1)}`,
        type: "line",
        data: medianData,
        symbol: "none",
        lineStyle: { opacity: 1 },
        areaStyle: { opacity: 0 }
    });
    chartSeries.push({ // Upper bound trace
        name: seriesName,//`Quantile ${decoded.labelFor(2)}`,
        type: "line",
        data: upperData,
        symbol: "none",
        lineStyle: { opacity: 0.3 },
        areaStyle: { opacity: 0 }
    });
}

function bandAreaEntry(
    stack: string,
    data: any[]
): Record<string, unknown> {
    return {
        type: "line",
        data: data,
        stack: stack,
        symbol: "none",
        lineStyle: { opacity: 0 },
        areaStyle: { opacity: 0.15 },
        tooltip: {
            show: false // This excludes this specific series from the tooltip
        }
    };
}

/** Single opaque line: one value per slot, no band. */
function scalarLineStrategy(
    series: TimeSeries,
    decoded: DecodedSeries,
    chartSeries: any[]
): void {

    if (decoded.kind !== "scalar") {
        throw new Error(`scalarLineStrategy got a ${decoded.kind} series`);
    }

    chartSeries.push({
        name: metricLabel(series.metric),
        type: "line",
        data: decoded.slots.map(slot => [
            createTimestamp(slot.slotIndex),
            slot.value,
            series.metric
        ]),
        symbol: "none",
        lineStyle: { opacity: 1 },
        areaStyle: { opacity: 0 }
    });
}

/**
 * Dispatch by decoded payload semantics; unknown definitions
 * throw and are skipped per series, never killing the chart.
 */
const strategyRegistry: Record<string, StrategyFn> = {
    quantile: quantileBandStrategy,
    scalar: scalarLineStrategy
};

/**
 * Entry-driven rendering: one opaque line per entry; dashed
 * entries carry the observation-phase line style.
 */
function entryStrategy(
    entry: ChartEntry,
    chartSeries: any[]
): void {

    chartSeries.push({
        name: entry.label,
        type: "line",
        data: entry.data.map(pair => [
            pair[0],
            pair[1],
            entry.metric
        ]),
        symbol: "none",
        lineStyle: entry.dashed
            ? { type: "dashed", opacity: 1 }
            : { opacity: 1 },
        connectNulls: false,
        areaStyle: { opacity: 0 }
    });
}

const option = computed(() => {

    const chartSeries = [];

    if (props.entries) {
        props.entries.forEach(entry => entryStrategy(entry, chartSeries));
    } else {
    props.forecast?.forecast.time_series.forEach(series => {
        // For the time being filter only series relevant to pv asset prediction
        const metrics = props.metrics ?? [
            'direct_normal_irradiance', 'diffuse_irradiance', 'active_power'
        ];
        if(!metrics.includes(series.metric)) {
            return
        }

        try {
            const decoded = decodeSeries(series);
            strategyRegistry[decoded.kind](series, decoded, chartSeries);
        }
        catch (e) {
            console.error(`Skipping series ${series.metric}:`, e);
        }

    });
    }


    return {
        title: {
            text: chartTitle.value,
            left: "center"
        },

        tooltip: {
            trigger: "axis",
                formatter(params) {

                    return params.map(item => {

                        const metric =
                            item.value[2];

                        const unit =
                            metricUnit(metric);


                        return `
                            ${item.marker}
                            ${metric}:
                            ${new Intl.NumberFormat("de-DE", { maximumFractionDigits: 2 }).format(
    item.value[1],
  )} ${unit}
                        `;

                    }).join("<br/>");

                }
        },


        legend: {
            top: 0,
            left: 0
        },


        grid: {
            left: 50,
            right: 30,
            top: 50,
            bottom: 60
        },


        xAxis: {

            type: "category",

            axisLabel: {
                rotate: 45
            }

        },


        yAxis: {

            type: "value"

        },


        series: chartSeries

    };

});


</script>


<template>

<div class="forecast-chart">

    <VChart
        :option="option"
        autoresize
    />

</div>

</template>


<style scoped>

.forecast-chart {

    width: 100%;
    height: 450px;

}

</style>