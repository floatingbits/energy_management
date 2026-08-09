import axios from "axios";

const client = axios.create({
    baseURL: import.meta.env.VITE_API_ASSET_BASE_URL
});

export interface Asset {
    id: number;
    name: string;
    latitude: number;
    longitude: number;
    asset_type: string;
    configuration: any
}
export enum AssetType {
    SOLAR = "solar",
    WIND = "wind",
    BATTERY = "battery"
}
export async function getAssets(): Promise<Asset[]> {
    const response = await client.get("/assets/");
    return response.data;
}