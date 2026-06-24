"""crear_tablas_iniciales

Revision ID: e83c7154353d
Revises: a4f0e099b8ce
Create Date: 2026-06-24 11:07:30.745728

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e83c7154353d'
down_revision: Union[str, Sequence[str], None] = 'a4f0e099b8ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
