from pydantic import BaseModel, ConfigDict


class PvConfigurationResponse(BaseModel):

    panel_area_m2: float

    efficiency: float

    tilt_deg: float

    azimuth_deg: float

    model_config = ConfigDict(
        from_attributes=True
    )


class WindConfigurationResponse(BaseModel):

    hub_height_m: float

    rotor_diameter_m: float

    model_config = ConfigDict(
        from_attributes=True
    )


class BatteryConfigurationResponse(BaseModel):

    capacity_kwh: float

    max_charge_kw: float

    max_discharge_kw: float

    model_config = ConfigDict(
        from_attributes=True
    )


class PvConfigurationCreate(BaseModel):

    panel_area_m2: float

    efficiency: float

    tilt_deg: float

    azimuth_deg: float


class WindConfigurationCreate(BaseModel):

    hub_height_m: float

    rotor_diameter_m: float


class BatteryConfigurationCreate(BaseModel):

    capacity_kwh: float

    max_charge_kw: float

    max_discharge_kw: float