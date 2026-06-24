"""crear_tablas_iniciales

Revision ID: 2cb754496682
Revises: e83c7154353d
Create Date: 2026-06-24 11:08:30.737789

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2cb754496682'
down_revision: Union[str, Sequence[str], None] = 'e83c7154353d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
