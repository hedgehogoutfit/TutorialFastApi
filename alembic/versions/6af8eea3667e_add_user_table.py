"""Add user table

Revision ID: 6af8eea3667e
Revises: 7dd3ef40abc1
Create Date: 2024-02-22 18:25:38.618819

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, Integer, String, TIMESTAMP, text


# revision identifiers, used by Alembic.
revision: str = '6af8eea3667e'
down_revision: Union[str, None] = '7dd3ef40abc1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    Column('id', Integer, primary_key=True, nullable=False),
                    Column('email', String, nullable=False, unique=True),
                    Column('password ', String, nullable=False),
                    Column('created_at', TIMESTAMP(timezone=True), nullable=False,
                           server_default=text('now()'))
                    )


def downgrade() -> None:
    op.drop_table('users')
