"""Added likes table

Revision ID: 6ea135acfe94
Revises: 6962fe96b9d6
Create Date: 2024-04-23 10:33:20.145441

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ea135acfe94'
down_revision: Union[str, None] = '6962fe96b9d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('likes',
    sa.Column('sender_id', sa.Integer(), nullable=False),
    sa.Column('receiver_id', sa.String(), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('likes')
    # ### end Alembic commands ###
