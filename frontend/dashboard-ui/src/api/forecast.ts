import axios from "axios";

const client = axios.create({
    baseURL: import.meta.env.VITE_API_FORECAST_BASE_URL
});


/**
 * Raw time series value as delivered by the API.
 *
 * The `values` array is definition-agnostic on the wire:
 * its arity and semantics are defined by `value_type_definition`
 * on the parent time series (e.g. one entry per quantile level,
 * a single scalar value, ...).
 */
export interface TimeSeriesValue {
    slot_index: number;
    values: (number | null)[];
}


export interface TimeSeries {
    metric: string;
    /** JSON value_type_definition, e.g. '{"type": "quantile", "quantiles": [5, 50, 95]}'. */
    value_type_definition: string;
    values: TimeSeriesValue[];
}
interface TimeSeriesTimeBase {
    start: string;
    resolution_seconds: number;
    slots: number;
}
interface Forecast {

    time_series_time_base: TimeSeriesTimeBase

    time_series: TimeSeries[]
}

export interface WeatherForecast {
    id: number;
    latitude: number;
    longitude: number;
    forecast: Forecast;
    source: any;
}

export interface AssetForecast {
    id: number;
    asset_id: number;
    forecast: Forecast
}

export interface PortfolioForecast {
    id: number;
    portfolio_id: number;
    forecast: Forecast
}
function formatCoordinate(value: number): string {
    return value.toFixed(2);
}

export async function getWeatherForecast(
    latitude: number,
    longitude: number
): Promise<WeatherForecast[]> {

    const response = await client.get("/weather-forecasts/", {
        params: {
            latitude: formatCoordinate(latitude),
            longitude: formatCoordinate(longitude),
            limit: 1
        }
    });

    return response.data;
}



export async function getAssetForecast(
    asset_id: number
): Promise<AssetForecast> {

    const response = await client.get(`/asset-forecasts/${asset_id}`, {});

    return response.data;
}



export async function getPortfolioForecast(
    portfolio_id: number
): Promise<PortfolioForecast> {

    const response = await client.get(`/portfolio-forecasts/${portfolio_id}`, {});

    return response.data;
}