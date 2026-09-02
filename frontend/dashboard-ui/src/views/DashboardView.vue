<script setup lang="ts">

import { ref, onMounted } from "vue";

import { getAssets, getAssetsByPortfolio, type Asset } from "../api/asset";
import { getPortfolios, type Portfolio } from "../api/portfolio";
import {
    getWeatherForecast,
    type WeatherForecast,
    getAssetForecast,
    type AssetForecast
} from "../api/forecast";

import PortfolioTable from "../components/PortfolioTable.vue";
import AssetMap from "../components/AssetMap.vue";
import AssetDetails from "../components/AssetDetails.vue";
import ForecastChart from "../components/ForecastChart.vue";

const portfolios = ref<Portfolio[]>([]);
const selectedPortfolio = ref<Portfolio|null>(null);

const assets = ref<Asset[]>([]);

const selectedAsset = ref<Asset|null>(null);

const selectedForecast = ref<WeatherForecast|null>(null);
const selectedAssetForecast = ref<AssetForecast|null>(null);



async function selectAsset(asset: Asset) {

    selectedAsset.value = asset;


    const forecasts =
        await getWeatherForecast(
            asset.latitude,
            asset.longitude
        );
    const assetForecasts =
        await getAssetForecast(
            asset.id
        );

    selectedForecast.value =
        forecasts[0] ?? null;

    selectedAssetForecast.value =
        assetForecasts ?? null;

}

async function handlePortfolioSelect(portfolio: Portfolio) {
  console.log('Selected portfolio:', portfolio);

  if (!selectedPortfolio.value || selectedPortfolio.value.id !== portfolio.id) {
      selectedPortfolio.value = portfolio;
      assets.value = await getAssetsByPortfolio(portfolio.id)
      selectedAsset.value = null
      selectedForecast.value = null
      selectedAssetForecast.value = null
  }
}


onMounted(async () => {

    portfolios.value =
        await getPortfolios();

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
        <section class="portfolio-table-wrapper">
            <PortfolioTable
              :portfolios="portfolios"
              @select="handlePortfolioSelect"
              class="portfolio-table"
            />
        </section>

        <section class="map">
            <h3 v-html="selectedPortfolio ? selectedPortfolio.name : 'Bitte Portfolio wählen'"></h3>
            <AssetMap
                :assets="assets"
                :selected-asset="selectedAsset"
                @select="selectAsset"
            />

        </section>






            <AssetDetails

                :asset="selectedAsset"

                :forecast="selectedForecast"


            />


            <ForecastChart
                v-if="selectedForecast"
                :forecast="selectedForecast"
                :asset="selectedAsset"
                forecast-type="Weather"
            />
            <ForecastChart
                v-if="selectedAssetForecast"
                :forecast="selectedAssetForecast"
                :asset="selectedAsset"
                forecast-type="Asset"

            />





    </main>

</div>

</template>



<style scoped>

.dashboard {

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
.portfolio-table-wrapper {
    grid-column: span 2;
}


.content {

    display: flex;

    flex-direction: column;

    gap: 1rem;

}


</style>