<script setup lang="ts">

import type { Asset } from "../api/asset";
import type { WeatherForecast } from "../api/forecast";


defineProps<{
    asset: Asset | null,
    forecast: WeatherForecast | null
}>();

</script>


<template>

<div class="panel">

    <h2>
        Asset Details
    </h2>


    <template v-if="asset">

        <h3>
            {{ asset.name }}
        </h3>


        <p>
            Position:
            <br>
            {{ asset.latitude }},
            {{ asset.longitude }}
        </p>

        <p>
            Konfiguration:
            <br>
            {{ asset.configuration }}
        </p>



        <template v-if="forecast">

            <hr>
            <h4>Forecast</h4>

            <p>
                Provider:
                {{ forecast.source.provider }}
            </p>


            <p>
                Modell:
                {{ forecast.source.model }}
            </p>


            <p>
                Start:
                <br>
                {{ forecast.forecast.time_series_time_base.start }}
            </p>


            <p>
                Raster:
                {{ forecast.forecast.time_series_time_base.resolution_seconds / 60 }}
                Minuten
            </p>


            <p>
                Slots:
                {{ forecast.forecast.time_series_time_base.slots }}
            </p>


        </template>

    </template>


    <p v-else>
        Bitte Asset auswählen
    </p>


</div>

</template>


<style scoped>

.panel {

    padding: 1rem;
    background: #f5f5f5;
    border-radius: 8px;

}

</style>