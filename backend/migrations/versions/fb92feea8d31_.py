"""empty message

Revision ID: fb92feea8d31
Revises: 
Create Date: 2022-08-27 23:15:11.731933

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb92feea8d31'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questions', sa.Column('rating', sa.Integer(), nullable=False, server_default='0'))
    op.drop_constraint('category', 'questions', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('category', 'questions', 'categories', ['category'], ['id'], onupdate='CASCADE', ondelete='SET NULL')
    op.drop_column('questions', 'rating')
    # ### end Alembic commands ###
