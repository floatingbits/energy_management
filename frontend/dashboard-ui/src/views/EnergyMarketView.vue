<script setup lang="ts">

import { ref, computed, onMounted } from "vue";

import {
    getEnergyMarketForecasts,
    type EnergyMarketForecast,
    type EnergyMarketForecastBasis
} from "../api/energy-market";
import type { ChartEntry } from "../components/ForecastChart.vue";

import ForecastChart from "../components/ForecastChart.vue";

const markets = ref<string[]>(["DE-LU"]);
const selectedMarket = ref<string | null>(null);

const forecast = ref<EnergyMarketForecast | null>(null);
const selectedVariable = ref<string|null>(null);
const loading = ref(false);
const error = ref<string | null>(null);

/**
 * Extrapolated filler for missing recent observations is display-
 * trimmed: the line ends at the last value actually delivered.
 * v1 limitation; interpolation marker storage is a later step.
 */
function nonNullSlots(
    basis: EnergyMarketForecastBasis
): { slotIndex: number; value: number }[] {
    return basis.series.values
        .filter(value => value.values[0] !== null)
        .sort((a, b) => a.slot_index - b.slot_index)
        .map(value => ({ slotIndex: value.slot_index, value: value.values[0] as number }));
}

function timestamps(
    start: string,
    resolutionSeconds: number,
    slotIndexes: number[]
): string[] {
    const epochStart = new Date(start).getTime();
    return slotIndexes.map(slotIndex =>
        new Date(epochStart + slotIndex * resolutionSeconds * 1000).toLocaleString(
            "de-DE",
            { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" }
        )
    );
}

/** Observation data (the fit window) as a dashed segment. */
function dashedEntry(
    basis: EnergyMarketForecastBasis
): ChartEntry {
    const slots = nonNullSlots(basis);
    return {
        label: basis.series_name,
        metric: basis.series.metric,
        dashed: true,
        data: timestamps(
            basis.series.time_series_time_base!.start,
            basis.series.time_series_time_base!.resolution_seconds,
            slots.map(slot => slot.slotIndex)
        ).map((ts, i) => [ts, slots[i].value]),
    };
}

function solidEntry(
    basis: EnergyMarketForecastBasis
): ChartEntry {
    const slots = nonNullSlots(basis);
    return {
        label: basis.series_name,
        metric: basis.series.metric,
        data: timestamps(
            basis.series.time_series_time_base!.start,
            basis.series.time_series_time_base!.resolution_seconds,
            slots.map(slot => slot.slotIndex)
        ).map((ts, i) => [ts, slots[i].value]),
    };
}

/* ------------------------------------------------------------------
 * Price chart: endogenous observation before the forecast run,
 * marked by the dashed line style; x-axes are shared and aligned.
 */
const priceEntries = computed((): ChartEntry[] => {
    if (!forecast.value) {
        return [];
    }

    const run = forecast.value.forecast.time_series_time_base;

    const observed = forecast.value.basis.find(
        item => item.role === "endogenous"
    );
    const entries: ChartEntry[] = observed ? [dashedEntry(observed)] : [];

    const predicted = forecast.value.forecast.time_series[0];
    if (predicted) {
        const slots = predicted.values
            .map(value => ({ slotIndex: value.slot_index, value: value.values[0] as number }))
            .sort((a, b) => a.slotIndex - b.slotIndex);
        entries.push({
            label: str_metric(predicted.metric),
            metric: predicted.metric,
            data: timestamps(
                run.start,
                run.resolution_seconds,
                slots.map(slot => slot.slotIndex)
            ).map((ts, i) => [ts, slots[i].value]),
        });
    }
    return entries;
});

// De-DE formatted label maps for the exogenous variables.
function str_metric(metric: string): string {
    const labels = {
        wind_speed: "Windgeschwindigkeit",
        global_solar_irradiance: "Globalbestrahlungsstärke"
    };
    return labels[metric as keyof typeof labels] ?? metric;
}

/* ------------------------------------------------------------------
 * Exogenous charts: every configured location of the chosen
 * variable at once, dashed before `now` (fit data), solid after.
 */
const exogenousVariables = computed((): string[] => {
    if (!forecast.value) {
        return [];
    }
    const names = new Set<string>();
    forecast.value.basis
        .forEach(item => {
            if (item.role === "exogenous") {
                // name layout "<variable>-<index>" (loop index from the bootstrap)
                names.add(item.series_name.split("-")[0]);
            }
        });
    return [...names];
});

const variableEntries = computed((): ChartEntry[] => {
    if (!forecast.value || !selectedVariable.value) {
        return [];
    }
    const entries: ChartEntry[] = [];
    forecast.value.basis
        .filter(item =>
            item.role === "exogenous"
            && item.series_name.startsWith(selectedVariable.value!)
        )
        .forEach(item =>
            entries.push(
                item.metadata?.phase === "predict"
                    ? solidEntry(item)
                    : dashedEntry(item)
            )
        );
    return entries;
});

const variableTitle = computed((): string =>
    selectedVariable.value
        ? `${str_metric(selectedVariable.value)} ${selectedMarket.value}`
        : ""
);

/**
 * The one meaningful chart: the latest prediction run, fronted by
 * the observation data the prediction is based on.
 */
const priceTitle = computed((): string =>
    forecast.value
        ? `Day-Ahead-Preis ${forecast.value.market} (gestrichen: Beobachtung)`
        : ""
);

async function selectMarket(market: string) {

    if (selectedMarket.value === market) {
        return;
    }

    selectedMarket.value = market;
    forecast.value = null;
    selectedVariable.value = null;
    error.value = null;
    loading.value = true;

    try {
        // Endpoint returns forecasts newest first; we show the latest run.
        const forecasts = await getEnergyMarketForecasts(market);
        forecast.value = forecasts[0] ?? null;
        selectedVariable.value = exogenousVariables.value[0] ?? null;
    }
    catch (e) {
        error.value = "Keine Prognosen für diesen Markt abrufbar.";
        forecast.value = null;
    }
    finally {
        loading.value = false;
    }
}


onMounted(async () => {
    await selectMarket(markets.value[0]);
});

</script>


<template>

<div class="market-view">

    <section class="market-controls">
        <label for="market-select">Markt</label>
        <select
            id="market-select"
            :value="selectedMarket"
            @change="selectMarket(($event.target as HTMLSelectElement).value)"
        >
            <option
                v-for="market in markets"
                :key="market"
                :value="market"
            >
                {{ market }}
            </option>
        </select>

        <span
            v-if="loading"
            class="market-status"
        >
            Lade Prognosen…
        </span>
        <span
            v-else-if="error"
            class="market-status"
        >
            {{ error }}
        </span>
    </section>

    <section
        v-if="forecast"
        class="market-forecast"
    >
        <ForecastChart
            :entries="priceEntries"
            :title="priceTitle"
            forecast-type="Energy Price"
        />

        <section
            v-if="exogenousVariables.length"
            class="market-basis"
        >
            <label for="variable-select">Exogene Variable</label>
            <select
                id="variable-select"
                v-model="selectedVariable"
            >
                <option
                    v-for="variable in exogenousVariables"
                    :key="variable"
                    :value="variable"
                >
                    {{ str_metric(variable) }}
                </option>
            </select>

            <ForecastChart
                :entries="variableEntries"
                :title="variableTitle"
                forecast-type="Exogenous"
            />
        </section>
    </section>

    <section
        v-else-if="!loading"
        class="market-empty"
    >
        Keine Prognose vorhanden für Markt {{ selectedMarket }}.
    </section>

</div>

</template>


<style scoped>

.market-view {

    display: flex;

    flex-direction: column;

    gap: 1rem;

}


.market-controls {

    display: flex;

    align-items: center;

    gap: 0.75rem;

}


.market-controls select {

    padding: 0.25rem 0.5rem;

}


.market-status {

    color: #666;

    font-size: 0.9rem;

}


.market-empty {

    color: #666;

    padding: 2rem 0;

    text-align: center;

}

</style>
