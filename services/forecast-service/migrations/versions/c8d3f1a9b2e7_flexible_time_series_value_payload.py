"""Flexible TimeSeriesValue payload structure

Revision ID: c8d3f1a9b2e7
Revises: b7c4d2e8f1a3
Create Date: 2026-09-16

- time_series_values: replace fixed quantile columns (p05/p50/p95)
  with a single `payload` string whose format is defined by the series'
  value_type_definition.
- time_series: add `value_type_definition` column describing the payload
  parsing strategy (e.g. {"type": "quantile", "quantiles": [5, 50, 95]}).

Existing values are NOT migrated; they are re-written by the regular
write paths (weather/asset/portfolio forecast jobs).
"""
from alembic import op
import sqlalchemy as sa

revision = 'c8d3f1a9b2e7'
down_revision = 'b7c4d2e8f1a3'
branch_labels = None
depends_on = None

QUANTILE_DEFINITION = '{"type": "quantile", "quantiles": [5, 50, 95]}'


def upgrade():
    op.add_column(
        'time_series',
        sa.Column(
            'value_type_definition',
            sa.String(),
            nullable=False,
            server_default=QUANTILE_DEFINITION,
        ),
    )
    op.add_column(
        'time_series_values',
        sa.Column(
            'payload',
            sa.String(),
            nullable=False,
            server_default='[]',
        ),
    )
    op.drop_column('time_series_values', 'p05')
    op.drop_column('time_series_values', 'p50')
    op.drop_column('time_series_values', 'p95')


def downgrade():
    op.add_column(
        'time_series_values',
        sa.Column('p05', sa.Float(), nullable=True),
    )
    op.add_column(
        'time_series_values',
        sa.Column('p50', sa.Float(), nullable=True),
    )
    op.add_column(
        'time_series_values',
        sa.Column('p95', sa.Float(), nullable=True),
    )
    op.drop_column('time_series_values', 'payload')
    op.drop_column('time_series', 'value_type_definition')
