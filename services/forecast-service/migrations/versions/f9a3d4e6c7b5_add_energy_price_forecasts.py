"""add energy_price_forecasts

Revision ID: f9a3d4e6c7b5
Revises: e5f2b7c9d1a8
Create Date: 2026-12-04

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'f9a3d4e6c7b5'
down_revision: Union[str, Sequence[str], None] = 'e5f2b7c9d1a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'energy_price_forecasts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('time_series_group_id', sa.Integer(), nullable=False),
        sa.Column('market', sa.String(), nullable=False),
        sa.Column('source', sa.String(), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(
            ['time_series_group_id'],
            ['time_series_groups.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('energy_price_forecasts')
