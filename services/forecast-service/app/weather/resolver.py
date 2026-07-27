from app.weather.value_objects import WeatherLocation


class WeatherLocationResolver:



    def __init__(self, grid_size = 0.1):
        self.grid_size = grid_size

    def resolve(
        self,
        latitude: float,
        longitude: float
    ) -> WeatherLocation:

        return WeatherLocation(
            latitude=round(
                latitude / self.grid_size
            ) * self.grid_size,

            longitude=round(
                longitude / self.grid_size
            ) * self.grid_size
        )