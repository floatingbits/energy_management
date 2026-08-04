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

</script>

<template>

<LMap
    style="height: 500px"
    :zoom="5"
    :center="[51.1657,10.4515]"
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