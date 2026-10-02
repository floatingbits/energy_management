import axios from "axios";

const client = axios.create({
    baseURL: import.meta.env.VITE_API_FORECAST_BASE_URL
});

/**
 * Reused wire types: an energy price forecast is stored with the
 * same TimeSeriesGroup shape as the other forecasts.
 */
import type { Forecast as StoredForecast } from "./forecast";

export interface EnergyPriceForecast {
    id: number;
    market: string;
    source: string;
    forecast: StoredForecast;
}

export async function getEnergyPriceForecasts(
    market?: string
): Promise<EnergyPriceForecast[]> {

    const response = await client.get("/energy-price-forecasts/", {
        params: market ? { market } : {}
    });

    return response.data;
}
