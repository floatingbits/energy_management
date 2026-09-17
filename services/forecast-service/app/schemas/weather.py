from datetime import datetime

from pydantic import BaseModel


class WeatherVariableValue(BaseModel):
    """
    Eine Wettervariable für einen Zeitpunkt: das geordnete Zahlenarray
    des Payloads (bezogen auf die Definitions-Pyramide der Serie).
    """

    variable: str

    values: list[float | None]


class WeatherForecastPoint(BaseModel):
    """
    Wetterdaten für eine Location und ein Zeitintervall.
    """

    latitude: float
    longitude: float

    period_start: datetime
    period_end: datetime

    variables: list[WeatherVariableValue]


class WeatherForecastResult(BaseModel):
    """
    Ergebnis eines Provider-Aufrufs.
    Noch ohne Datenbankbezug.
    """

    provider: str
    model: str

    forecasts: list[WeatherForecastPoint]