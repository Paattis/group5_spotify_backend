"""empty message

Revision ID: 210be4862f1e
Revises: 81434b048bea
Create Date: 2022-04-08 17:10:53.127695

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '210be4862f1e'
down_revision = '81434b048bea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('locationsong',
    sa.Column('song_id', sa.Integer(), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['location_id'], ['Location.id'], ),
    sa.ForeignKeyConstraint(['song_id'], ['Song.id'], ),
    sa.PrimaryKeyConstraint('song_id', 'location_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('locationsong')
    # ### end Alembic commands ###
