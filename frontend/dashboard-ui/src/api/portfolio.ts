import axios from "axios";

const client = axios.create({
    baseURL: import.meta.env.VITE_API_ASSET_BASE_URL
});

export interface Portfolio {
    id: number;
    name: string;
    description: string;
}

export async function getPortfolios(): Promise<Portfolio[]> {
    const response = await client.get("/portfolios/");
    return response.data;
}