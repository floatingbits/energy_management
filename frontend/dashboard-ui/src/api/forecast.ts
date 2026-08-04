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


export interface WeatherForecast {
    id: number;
    latitude: number;
    longitude: number;
    forecast: {
        run: {
            start: string;
            resolution: string;
            slots: number;
        },
        series: ForecastSeries[];
    }
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