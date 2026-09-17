"""add energy_market_observations

Revision ID: e5f2b7c9d1a8
Revises: c8d3f1a9b2e7
Create Date: 2026-09-18

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e5f2b7c9d1a8'
down_revision: Union[str, Sequence[str], None] = 'c8d3f1a9b2e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'energy_market_observations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('time_series_group_id', sa.Integer(), nullable=False),
        sa.Column('location_key', sa.String(), nullable=False),
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
    op.drop_table('energy_market_observations')
