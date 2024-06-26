"""user table  created

Revision ID: 0001
Revises:
Create Date: 2023-05-19 18:44:40.437467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(length=20), nullable=False),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('primary_email', sa.String(), nullable=False),
    sa.Column('primary_phone', sa.String(), nullable=False),
    sa.Column('country_code', sa.String(), nullable=True),
    sa.Column('pin', sa.String(), nullable=True),
    sa.Column('auth_token', sa.String(), nullable=True),
    sa.Column('last_login_at', sa.DateTime(), nullable=True),
    sa.Column('address', sa.Text(), nullable=True),
    sa.Column('zip_code', sa.String(), nullable=True),
    sa.Column('deactivated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.BigInteger(), nullable=True),
    sa.Column('updated_by', sa.BigInteger(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('primary_email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
