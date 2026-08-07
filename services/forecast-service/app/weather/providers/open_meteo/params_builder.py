from datetime import datetime

class ParamsBuilder:

    VARIABLES_15_MINUTELY = [
        "temperature_2m",
        "wind_speed_10m",
        "shortwave_radiation",
        "direct_radiation",
        "diffuse_radiation",
        "direct_normal_irradiance",
        "global_tilted_irradiance",
        "global_tilted_irradiance_instant"
    ]
    VARIABLES_HOURLY = [
        "cloud_cover"
    ]
    VARIABLES_DAILY = [
        "temperature_2m_mean"
    ]

    def build_request_params(self,
                             locations: list[dict[str,float]],
                             variables: list[str],
                             start_date: datetime,
                             end_date: datetime,
                             
                             models:list[str]|None=None
                             ):
        params = {}
        if models is not None:
            params['models'] = models
        params['latitude'] = [location['latitude'] for location in locations]
        params['longitude'] = [location['longitude'] for location in locations]
        params['start_date'] = start_date.strftime("%Y-%m-%d")
        params['end_date'] = end_date.strftime("%Y-%m-%d")
        variables_daily =[]
        variables_hourly = []
        variables_minutely_15 = []

        unknown_variables = []
        for variable in variables:
            if variable in self.VARIABLES_15_MINUTELY:
                variables_minutely_15.append(variable)
            elif variable in self.VARIABLES_HOURLY:
                variables_hourly.append(variable)
            elif variable in self.VARIABLES_DAILY:
                variables_daily.append(variable)
            else:
                unknown_variables.append(variable)

        if len(unknown_variables):
            raise ValueError('Unknown variables: {}'.format(unknown_variables))

        params['hourly'] = variables_hourly
        params['minutely_15'] = variables_minutely_15
        params['daily'] = variables_daily

        return params