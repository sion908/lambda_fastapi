""""CreateUsertable"

Revision ID: 65d138a8bfb0
Revises:
Create Date: 2023-08-21 19:33:39.183756+09:00

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql
from sqlalchemy_utils.types import ChoiceType, PasswordType, UUIDType

from models import SexType

# revision identifiers, used by Alembic.
revision: str = '65d138a8bfb0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'user',
        sa.Column('id', UUIDType(binary=False), nullable=False),
        sa.Column('username', sa.String(length=255, collation='utf8mb4_bin'), nullable=True),
        sa.Column('password', PasswordType(), nullable=True),
        sa.Column('sex', ChoiceType(choices=SexType, impl=mysql.TINYINT()), nullable=True),
        sa.Column('age', mysql.TINYINT(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=False, comment='更新日時'),
        sa.Column('created_at', sa.DateTime(), nullable=False, comment='作成日時'),
        sa.PrimaryKeyConstraint('id'),
        comment='ユーザー',
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_bin'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
