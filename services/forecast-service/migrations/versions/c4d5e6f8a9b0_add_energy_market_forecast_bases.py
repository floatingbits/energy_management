"""add energy_market_forecast_bases

Rename energy_price_forecasts to energy_market_forecasts (market
forecasts cover any market variable, not only prices) and add the
series-level basis references.

Revision ID: c4d5e6f8a9b0
Revises: f9a3d4e6c7b5
Create Date: 2026-10-02
"""
from alembic import op
import sqlalchemy as sa


revision = 'c4d5e6f8a9b0'
down_revision = 'f9a3d4e6c7b5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.rename_table('energy_price_forecasts', 'energy_market_forecasts')

    op.add_column(
        'energy_market_forecasts',
        sa.Column(
            'variable',
            sa.String(),
            nullable=False,
            server_default='day_ahead_electricity_price',
        ),
    )

    op.create_table(
        'energy_market_forecast_bases',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column(
            'energy_market_forecast_id',
            sa.Integer(),
            sa.ForeignKey('energy_market_forecasts.id'),
            nullable=False,
        ),
        sa.Column(
            'time_series_id',
            sa.Integer(),
            sa.ForeignKey('time_series.id'),
            nullable=False,
        ),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('series_name', sa.String(), nullable=False),
        sa.Column('metadata', sa.JSON(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('energy_market_forecast_bases')
    op.drop_column('energy_market_forecasts', 'variable')
    op.rename_table('energy_market_forecasts', 'energy_price_forecasts')
