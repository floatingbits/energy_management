"""retarget portfolio_forecasts.forecast_id to forecasts.id

Revision ID: a1f2c3d4e5f6
Revises: 844945f633ca
Create Date: 2026-09-09

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1f2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '844945f633ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # PortfolioForecasts hängen — wie AssetForecasts — über
    # forecast_id an Forecast (wo die Series/Values leben),
    # nicht direkt an ForecastRun.
    op.drop_constraint(
        'portfolio_forecasts_forecast_id_fkey',
        'portfolio_forecasts',
        type_='foreignkey',
    )
    op.create_foreign_key(
        None,
        'portfolio_forecasts',
        'forecasts',
        ['forecast_id'],
        ['id'],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        op.f('portfolio_forecasts_forecast_id_fkey'),
        'portfolio_forecasts',
        type_='foreignkey',
    )
    op.create_foreign_key(
        None,
        'portfolio_forecasts',
        'forecast_runs',
        ['forecast_id'],
        ['id'],
    )
