"""Mapping between our resolution system (timedelta) and SMARD resolution names."""
from datetime import timedelta


SMARD_RESOLUTIONS = {
    "quarterhour": timedelta(minutes=15),
    "hour": timedelta(hours=1),
    "day": timedelta(days=1),
    "week": timedelta(weeks=1),
    "month": timedelta(days=30),
    "year": timedelta(days=365),
}
