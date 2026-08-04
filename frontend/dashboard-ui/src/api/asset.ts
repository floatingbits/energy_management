import axios from "axios";

const client = axios.create({
    baseURL: "http://localhost:8000/api/v1"
});

export interface Asset {
    id: number;
    name: string;
    latitude: number;
    longitude: number;
    asset_type: string;
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