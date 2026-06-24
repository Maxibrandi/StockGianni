"""crear_tablas_iniciales

Revision ID: 39566432c3f8
Revises: 2cb754496682
Create Date: 2026-06-24 11:09:28.719972

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39566432c3f8'
down_revision: Union[str, Sequence[str], None] = '2cb754496682'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
