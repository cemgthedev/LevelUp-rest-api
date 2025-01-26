"""alterando campo url para banner_url e adicionando campo course url

Revision ID: f2d538797d01
Revises: bf7806095fd8
Create Date: 2025-01-26 16:12:57.168023

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'f2d538797d01'
down_revision: Union[str, None] = 'bf7806095fd8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('courses', sa.Column('banner_url', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.add_column('courses', sa.Column('course_url', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.drop_column('courses', 'url')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('courses', sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('courses', 'course_url')
    op.drop_column('courses', 'banner_url')
    # ### end Alembic commands ###
