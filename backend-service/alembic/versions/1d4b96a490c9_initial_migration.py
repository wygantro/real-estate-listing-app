"""initial migration

Revision ID: 1d4b96a490c9
Revises: 
Create Date: 2023-12-22 15:48:13.985691

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d4b96a490c9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('daily_price_data', sa.Column('eth_daily_price_open', sa.Numeric(precision=15, scale=6), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('daily_price_data', 'eth_daily_price_open')
    # ### end Alembic commands ###
