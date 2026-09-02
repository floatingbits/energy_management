<script setup lang="ts">
import L from "leaflet";
import {
    LMap,
    LTileLayer,
    LMarker
} from "@vue-leaflet/vue-leaflet";

import "leaflet/dist/leaflet.css";


import type { Asset } from "../api/asset";
import { AssetType } from "../api/asset";

import { computed } from "vue";
const props = defineProps<{
    assets: Asset[],
    selectedAsset?: Asset | null
}>();
const emit = defineEmits<{
    select: [asset: Asset]
}>()


function iconForAsset(asset: Asset) {

    const selected =
        props.selectedAsset?.id === asset.id;


    let symbol = "⚡";


    switch(asset.asset_type) {

        case AssetType.SOLAR:
            symbol = "☀️";
            break;

        case AssetType.WIND:
            symbol = "🌬️";
            break;

        case AssetType.BATTERY:
            symbol = "🔋";
            break;

    }


    return L.divIcon({

        html: `
            <div class="${selected ? "selected" : ""}">
                ${symbol}
            </div>
        `,

        className: "asset-marker"

    });

}
function getAssetsCenter(assets: Asset[]): [number, number] {
  if (assets.length === 0) {
    return [51.1657, 10.4515]; // Fallback Deutschland
  }

  const latitudes = assets.map(asset => asset.latitude);
  const longitudes = assets.map(asset => asset.longitude);

  const minLat = Math.min(...latitudes);
  const maxLat = Math.max(...latitudes);
  const minLng = Math.min(...longitudes);
  const maxLng = Math.max(...longitudes);

  return [
    (minLat + maxLat) / 2,
    (minLng + maxLng) / 2,
  ];
}
const center = computed(() => {
    return getAssetsCenter(props.assets)
})

</script>

<template>

<LMap
    style="height: 767px"
    :zoom="5"
    :center="center"
>

    <LTileLayer
        url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    />

    <LMarker

        v-for="asset in assets"

        :key="asset.id"

        :lat-lng="[asset.latitude, asset.longitude]"

        :icon="iconForAsset(asset)"

        @click="emit('select', asset)"

    />

</LMap>

</template>

<style scoped>

:global(.asset-marker) {

    background: transparent;

    border: none;

}


:global(.asset-marker div) {

    font-size: 28px;

    transition: transform 0.2s;

}


:global(.asset-marker .selected) {

    transform: scale(1.4);

    filter: drop-shadow(0 0 8px blue);

}

</style>