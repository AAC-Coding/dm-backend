"""add state to user table

Revision ID: 69412f00cd89
Revises: c5a082134b40
Create Date: 2024-01-09 14:18:47.726860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69412f00cd89'
down_revision = 'c5a082134b40'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('state', sa.String(length=10), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('state')

    # ### end Alembic commands ###
