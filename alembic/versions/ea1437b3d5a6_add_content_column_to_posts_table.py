"""add content column to posts table

Revision ID: ea1437b3d5a6
Revises: e42c462f4f0f
Create Date: 2026-04-07 13:33:16.774914

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea1437b3d5a6'
down_revision: Union[str, Sequence[str], None] = 'e42c462f4f0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
