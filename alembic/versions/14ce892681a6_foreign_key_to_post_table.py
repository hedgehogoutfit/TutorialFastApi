"""foreign key to post table

Revision ID: 14ce892681a6
Revises: 6af8eea3667e
Create Date: 2024-02-22 19:04:16.125494

"""
from typing import Sequence, Union

from alembic import op

from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ForeignKey

# revision identifiers, used by Alembic.
revision: str = '14ce892681a6'
down_revision: Union[str, None] = '6af8eea3667e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  Column('created_at', TIMESTAMP(timezone=True), nullable=False,
                         server_default=text('now()')))

    op.add_column('posts',
                  Column('owner_id', Integer, ForeignKey("users.id", ondelete="CASCADE")
                         , nullable=False))
    op.create_foreign_key('post_users-fk', source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    op.drop_column('posts', 'created_at')
