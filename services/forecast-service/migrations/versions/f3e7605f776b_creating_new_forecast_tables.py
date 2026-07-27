"""creating new forecast tables

Revision ID: f3e7605f776b
Revises: 0aafac9bc5dc
Create Date: 2026-07-27 09:00:17.164593

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3e7605f776b'
down_revision: Union[str, Sequence[str], None] = '0aafac9bc5dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
