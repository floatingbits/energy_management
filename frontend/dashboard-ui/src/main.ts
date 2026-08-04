import { use } from "echarts/core";
import { TitleComponent } from 'echarts/components';

import {
    LineChart
} from "echarts/charts";

import {
    GridComponent,
    TooltipComponent,
    LegendComponent
} from "echarts/components";

import {
    CanvasRenderer
} from "echarts/renderers";



import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'

import './style.css'

const app = createApp(App)

app.use(createPinia())

use([
    TitleComponent,
    LineChart,
    GridComponent,
    TooltipComponent,
    LegendComponent,
    CanvasRenderer
]);

app.mount('#app')