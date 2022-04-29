"""testing alembic

Revision ID: 0365aa43dc5f
Revises: 77c1612ce64d
Create Date: 2022-04-29 08:17:11.852318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0365aa43dc5f'
down_revision = '77c1612ce64d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('games', sa.Column('mlem', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('games', 'mlem')
    # ### end Alembic commands ###