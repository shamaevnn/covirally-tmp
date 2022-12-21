"""add username field

Revision ID: 717fee8b8b8b
Revises: 6c10fa7873ff
Create Date: 2022-12-21 11:17:44.143733

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '717fee8b8b8b'
down_revision = '6c10fa7873ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=32), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('username')

    # ### end Alembic commands ###
