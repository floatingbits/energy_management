<script setup lang="ts">

import { ref, onMounted } from "vue";

import {
    getEnergyPriceForecasts,
    type EnergyPriceForecast
} from "../api/energy-market";

import ForecastChart from "../components/ForecastChart.vue";

const markets = ref<string[]>(["DE-LU"]);
const selectedMarket = ref<string | null>(null);

const forecast = ref<EnergyPriceForecast | null>(null);
const loading = ref(false);
const error = ref<string | null>(null);


async function selectMarket(market: string) {

    if (selectedMarket.value === market) {
        return;
    }

    selectedMarket.value = market;
    forecast.value = null;
    error.value = null;
    loading.value = true;

    try {
        // Endpoint returns forecasts newest first; we show the latest run.
        const forecasts = await getEnergyPriceForecasts(market);
        forecast.value = forecasts[0] ?? null;
    }
    catch (e) {
        error.value = "Keine Preisprognose für diesen Markt abrufbar.";
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
        <label for="market-select">Markt:</label>
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
            :forecast="forecast"
            forecast-type="Energy Price"
            :metrics="['day_ahead_electricity_price']"
        />
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
