import { createRouter, createWebHistory } from "vue-router";

import EnergyMarketView from "./views/EnergyMarketView.vue";
import DashboardView from "./views/DashboardView.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/",
            name: "dashboard",
            component: DashboardView
        },
        {
            path: "/market",
            name: "market",
            component: EnergyMarketView
        }
    ]
});

export default router;
