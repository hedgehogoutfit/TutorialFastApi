"""add content column to posts table

Revision ID: 7dd3ef40abc1
Revises: b75d31de60ca
Create Date: 2024-02-22 18:11:17.855058

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7dd3ef40abc1'
down_revision: Union[str, None] = 'b75d31de60ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
