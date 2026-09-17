"""rename aggregate models to time_series naming

Forecast / ForecastRun / ForecastSeries / ForecastValue
→ TimeSeriesGroup / TimeSeriesTimeBase / TimeSeries / TimeSeriesValue.

Revision ID: b7c4d2e8f1a3
Revises: a1f2c3d4e5f6
Create Date: 2026-09-09

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'b7c4d2e8f1a3'
down_revision: Union[str, Sequence[str], None] = 'a1f2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Tabellen
    op.rename_table('forecast_values', 'time_series_values')
    op.rename_table('forecast_series', 'time_series')
    op.rename_table('forecast_runs', 'time_series_time_bases')
    op.rename_table('forecasts', 'time_series_groups')

    # Spalten innerhalb der umbenannten Tabellen.
    # Postgres passt die FK-Referenzen der kontextübergreifenden
    # Tabellen (asset_forecasts.forecast_id etc.) beim Umbenennen
    # der Zieltabelle automatisch an.
    op.alter_column(
        'time_series_groups',
        'forecast_run_id',
        new_column_name='time_series_time_base_id',
    )
    op.alter_column(
        'time_series',
        'forecast_id',
        new_column_name='time_series_group_id',
    )
    op.alter_column(
        'time_series_values',
        'series_id',
        new_column_name='time_series_id',
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'time_series_values',
        'time_series_id',
        new_column_name='series_id',
    )
    op.alter_column(
        'time_series',
        'time_series_group_id',
        new_column_name='forecast_id',
    )
    op.alter_column(
        'time_series_groups',
        'time_series_time_base_id',
        new_column_name='forecast_run_id',
    )

    op.rename_table('time_series_groups', 'forecasts')
    op.rename_table('time_series_time_bases', 'forecast_runs')
    op.rename_table('time_series', 'forecast_series')
    op.rename_table('time_series_values', 'forecast_values')
