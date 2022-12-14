"""empty message

Revision ID: dae40fbe086f
Revises: 5c40267f0e3d
Create Date: 2022-11-16 22:51:59.974187

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dae40fbe086f'
down_revision = '5c40267f0e3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('book_name', sa.String(length=150), nullable=False),
    sa.Column('author', sa.String(length=150), nullable=False),
    sa.Column('content', sa.String(length=400), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('author')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('books')
    # ### end Alembic commands ###
