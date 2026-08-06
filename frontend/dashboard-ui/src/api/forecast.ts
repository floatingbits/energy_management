import axios from "axios";

const client = axios.create({
    baseURL: "http://localhost:8001/api/v1"
});


export interface ForecastValue {
    slot_index: number;
    p05?: number;
    p50?: number;
    p95?: number;
}


export interface ForecastSeries {
    metric: string;
    values: ForecastValue[];
}
interface ForecastRun {
    start: string;
    resolution_seconds: number;
    slots: number;
}
interface Forecast {

    run: ForecastRun

    series: ForecastSeries[]
}

export interface WeatherForecast {
    id: number;
    latitude: number;
    longitude: number;
    forecast: Forecast
}

export interface AssetForecast {
    id: number;
    asset_id: number;
    forecast: Forecast
}


export async function getWeatherForecast(
    latitude: number,
    longitude: number
): Promise<WeatherForecast[]> {

    const response = await client.get("/weather-forecasts/", {
        params: {
            latitude,
            longitude,
            limit: 1
        }
    });

    return response.data;
}

export async function getAssetForecast(
    asset_id: number
): Promise<AssetForecast[]> {

    const response = await client.get(`/asset-forecasts/${asset_id}`, {});

    return response.data;
}