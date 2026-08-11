<script setup lang="ts">

import { computed } from "vue";
import VChart from "vue-echarts";

import type { WeatherForecast, AssetForecast } from "../api/forecast";
import type { Asset } from "../api/asset";

const props = defineProps<{
    forecast: WeatherForecast|AssetForecast,
    forecastType: string,
    asset?: Asset | null
}>();
const chartTitle = computed(() => {

    if (!props.asset) {
        return "Weather Forecast";
    }

    return `${props.asset.name} - ${props.forecastType} Forecast`;

});

function createTimestamp(
    slotIndex: number
): string {

    const start = new Date(
        props.forecast.forecast.forecast_run.start
    );

    const resolution =
        props.forecast.forecast.forecast_run.resolution_seconds;


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
        case "global_solar_irradiance":
        case "direct_normal_irradiance":
        case "diffuse_irradiance":
            return "W/m²";

        default:
            return "";

    }

}

const option = computed(() => {

    const chartSeries = [];

    props.forecast.forecast.series.forEach(series => {
        //For the time being filter only series relevant to pv asset prediction
        if(!['direct_normal_irradiance', 'diffuse_irradiance', 'active_power'].includes(series.metric)) {
            return
        }


        const lowerData = series.values.map(value => [
            createTimestamp(value.slot_index),
            value.p05,
            series.metric + ' p05'
        ]);
        const upperData = series.values.map(value => [
            createTimestamp(value.slot_index),
            value.p95,
            series.metric + ' p95'
        ]);
        const medianData = series.values.map(value => [
            createTimestamp(value.slot_index),
            value.p50,
            series.metric + ' p50'
        ]);

        const lowerBandData = series.values.map(value => [
            createTimestamp(value.slot_index),
            value.p50 - value.p05,
            series.metric
        ]);

        const upperBandData = series.values.map(value => [
            createTimestamp(value.slot_index),
            value.p95 -value.p50,
            series.metric
        ]);



        // p05
        chartSeries.push({
            name: `${metricLabel(series.metric)} uncertainty`,
            type: "line",
            data: lowerData,
            stack: `${series.metric}-band`,
            symbol: "none",
            lineStyle: {
                opacity: 0.3
            },
            areaStyle: {
                opacity: 0
            }
        });
        chartSeries.push({
            name: `${metricLabel(series.metric)} uncertainty`,
            type: "line",
            data: lowerBandData,
            stack: `${series.metric}-band`,
            symbol: "none",
            lineStyle: {
                opacity:0
            },
            areaStyle: {
                opacity: 0.15
            },
            tooltip: {
                show: false // This excludes this specific series from the tooltip
              }
        });
        chartSeries.push({
            name: `${metricLabel(series.metric)} uncertainty`,
            type: "line",
            data: upperBandData,
            stack: `${series.metric}-band`,
            symbol: "none",
            lineStyle: {
                opacity: 0
            },
            areaStyle: {
                opacity: 0.15
            },
            tooltip: {
                show: false // This excludes this specific series from the tooltip
              }
        });
        chartSeries.push({
            name: `${metricLabel(series.metric)} uncertainty`,
            type: "line",
            data: medianData,
            //stack: `${series.metric}-band`,
            symbol: "none",
            lineStyle: {
                opacity: 1
            },
            areaStyle: {
                opacity: 0
            }
        });

         chartSeries.push({
            name: `${metricLabel(series.metric)} uncertainty`,
            type: "line",
            data: upperData,
            //stack: `${series.metric}-band`,
            symbol: "none",
            lineStyle: {
                opacity: 0.3
            },
            areaStyle: {
                opacity: 0
            }
        });

        // p95


    });


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