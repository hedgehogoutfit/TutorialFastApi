"""add columns to posts

Revision ID: 15b9b84a2426
Revises: 14ce892681a6
Create Date: 2024-02-22 19:22:13.713158

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, Boolean


# revision identifiers, used by Alembic.
revision: str = '15b9b84a2426'
down_revision: Union[str, None] = '14ce892681a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', Column('published', Boolean, server_default='True', nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'published')
