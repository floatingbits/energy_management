import pandas as pd
import json

BR_PVGEN_DATA_PATH = '../data/real_pv/br-pvgen/'
METADATA_FILE_NAME = "metadata.csv"
MEASUREMENTS_FILE_NAME = "merged.parquet"
MULTI_LOCATION_WEATHER_FILE_NAME = "weather_forecasts_multi_location.parquet"
BEST_LOCATIONS_FILE_NAME = "best_locations.parquet"
FORECAST_LOCATIONS_JSON_FILE_NAME = "forecast_locations.json"

def get_metadata_df():
    metadata_df = pd.read_csv(BR_PVGEN_DATA_PATH + METADATA_FILE_NAME)
    metadata_df['ps_id'] = metadata_df['id']
    metadata_df = metadata_df.set_index(['ps_id'])
    return metadata_df

def get_measurements_df():
    # pre-processed data generated in 01_prepare_data.ipynb
    measurements_df = pd.read_parquet(BR_PVGEN_DATA_PATH + MEASUREMENTS_FILE_NAME)
    measurements_df['datetime'] = pd.to_datetime(measurements_df['datetime'])
    return measurements_df.set_index(['datetime', 'ps_id'])

def get_multi_location_forecast_df():
    return pd.read_parquet(BR_PVGEN_DATA_PATH + MULTI_LOCATION_WEATHER_FILE_NAME)

def get_best_locations_df():
    return pd.read_parquet(BR_PVGEN_DATA_PATH + BEST_LOCATIONS_FILE_NAME)


def load_forecast_locations():
    with open(BR_PVGEN_DATA_PATH + FORECAST_LOCATIONS_JSON_FILE_NAME) as data_file:
        data_loaded = json.load(data_file)
    return data_loaded

def save_forecast_locations(locations_data):
    serializable_locations = {}
    for ps_id, location_dict in locations_data.items():
        serializable_locations[ps_id] = {}
        for lid, location in location_dict.items():
            serializable_locations[ps_id][lid] = {
                "longitude": location.longitude,
                "latitude": location.latitude,
            }
    with open(BR_PVGEN_DATA_PATH + FORECAST_LOCATIONS_JSON_FILE_NAME, "w") as f:
        json.dump(serializable_locations, f)

def filter_for_ps_id(df, ps_id):
    return df[df.index.get_level_values("ps_id") == ps_id]




def filter_for_date(df, year, month=None, day=None):
    filter_mask = (df.index.get_level_values("datetime").year == year)
    if month is not None:
        filter_mask = filter_mask & (df.index.get_level_values("datetime").month == month)
    if day is not None:
        filter_mask = filter_mask & (df.index.get_level_values("datetime").day == day)
    return df[filter_mask]


# the metadata miss the actual panel size (only contain *module*-size and *panel* count)
# thus deriving panel size from nominal power and efficiency
def calc_area_m2(df, ps_id):
    df = df.loc[ps_id]
    # using standard units
    g_stc = 1000  # W/m2
    nominal_power_w = df['nominal_power_mw'] * 1000000
    efficiency = df['panel_efficiency_percentage'] / 100
    return nominal_power_w / (g_stc * efficiency)


# We only know the federal state of the asset. Define the state bounds for best location search
def get_bounding_rect_for_state(state):
    STATE_BOUNDS = {
        "SP": {
            "min_lat": -25.31,
            "max_lat": -19.78,
            "min_lon": -53.11,
            "max_lon": -44.16,
        },
        "RJ": {
            "min_lat": -23.37,
            "max_lat": -20.76,
            "min_lon": -44.89,
            "max_lon": -40.96,
        },
        "GO": {
            "min_lat": -19.50,
            "max_lat": -12.40,
            "min_lon": -53.25,
            "max_lon": -45.90,
        },
        "MG": {
            "min_lat": -22.92,
            "max_lat": -14.22,
            "min_lon": -51.05,
            "max_lon": -39.85,
        },
        "BA": {
            "min_lat": -18.35,
            "max_lat": -8.53,
            "min_lon": -46.62,
            "max_lon": -37.35,
        },
        "PR": {
            "min_lat": -26.72,
            "max_lat": -22.52,
            "min_lon": -54.62,
            "max_lon": -48.02,
        },
    }
    return STATE_BOUNDS[state]["min_lat"], STATE_BOUNDS[state]["max_lat"], STATE_BOUNDS[state]["min_lon"], \
    STATE_BOUNDS[state]["max_lon"]


def get_bounding_rect_for_ps_id(df, ps_id):
    df = filter_for_ps_id(df, ps_id)
    return get_bounding_rect_for_state(df['brazil_federative_unit'].iloc[0])