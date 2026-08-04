<script setup lang="ts">

import { ref, onMounted } from "vue";

import { getAssets, type Asset } from "../api/asset";
import {
    getWeatherForecast,
    type WeatherForecast
} from "../api/forecast";


import AssetMap from "../components/AssetMap.vue";
import AssetDetails from "../components/AssetDetails.vue";
import ForecastChart from "../components/ForecastChart.vue";


const assets = ref<Asset[]>([]);

const selectedAsset = ref<Asset|null>(null);

const selectedForecast = ref<WeatherForecast|null>(null);



async function selectAsset(asset: Asset) {

    selectedAsset.value = asset;


    const forecasts =
        await getWeatherForecast(
            asset.latitude,
            asset.longitude
        );


    selectedForecast.value =
        forecasts[0] ?? null;

}


onMounted(async () => {

    assets.value =
        await getAssets();

});


</script>


<template>

<div class="dashboard">

    <header>
        <h1>
            Energy Management Dashboard
        </h1>
    </header>


    <main>


        <section class="map">

            <AssetMap
                :assets="assets"
                :selected-asset="selectedAsset"
                @select="selectAsset"
            />

        </section>



        <section class="content">


            <AssetDetails

                :asset="selectedAsset"

                :forecast="selectedForecast"

            />


            <ForecastChart
                v-if="selectedForecast"
                :forecast="selectedForecast"
                :asset="selectedAsset"

            />


        </section>


    </main>

</div>

</template>



<style scoped>

.dashboard {

    height: 100vh;

    display: flex;

    flex-direction: column;

}


header {

    padding: 1rem;

}


main {

    flex: 1;

    display: grid;

    grid-template-columns: 1fr 1fr;

    gap: 1rem;

    padding: 1rem;

}


.map {

    min-height: 600px;

}


.content {

    display: flex;

    flex-direction: column;

    gap: 1rem;

}


</style>