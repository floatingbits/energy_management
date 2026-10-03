import axios from "axios";

const client = axios.create({
    baseURL: import.meta.env.VITE_API_FORECAST_BASE_URL
});

/**
 * Reused wire types: an energy market forecast is stored with the
 * same TimeSeriesGroup shape as the other forecasts.
 */
import type { Forecast as StoredForecast } from "./forecast";

export interface EnergyMarketForecastBasis {
    id: number;
    role: string;
    series_name: string;
    metadata: Record<string, unknown> | null;
    series: {
        metric: string;
        value_type_definition: string;
        values: {
            slot_index: number;
            values: (number | null)[];
        }[];
        time_series_time_base: {
            start: string;
            resolution_seconds: number;
            slots: number;
        } | null;
    };
}

export interface EnergyMarketForecast {
    id: number;
    market: string;
    variable: string;
    source: string;
    forecast: StoredForecast;
    basis: EnergyMarketForecastBasis[];
}

export async function getEnergyMarketForecasts(
    market?: string
): Promise<EnergyMarketForecast[]> {

    const response = await client.get("/energy-market-forecasts/", {
        params: market ? { market } : {}
    });

    return response.data;
}
