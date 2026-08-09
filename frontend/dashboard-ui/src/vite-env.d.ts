interface ImportMetaEnv {
  readonly VITE_API_FORECAST_BASE_URL: string
  readonly VITE_API_ASSET_BASE_URL: string

}

interface ImportMeta {
  readonly env: ImportMetaEnv
}