"""empty message

Revision ID: 2d10ed5de194
Revises: 9f8be1094455
Create Date: 2021-05-15 05:58:42.822218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d10ed5de194'
down_revision = '9f8be1094455'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_<class 'application.models.DTM'>_index", table_name="<class 'application.models.DTM'>")
    op.drop_table("<class 'application.models.DTM'>")
    op.add_column('dtm', sa.Column('author', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dtm', 'author')
    op.create_table("<class 'application.models.DTM'>",
    sa.Column('index', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('65276', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('A History of Sculpture', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('Short, Ernest Henry', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column("['en']", sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('"https://www.gutenberg.org/files/65276/65276-h/65276-h.htm"', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('f', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('https://www.gutenberg.org/ebooks/65276', sa.TEXT(), autoincrement=False, nullable=True)
    )
    op.create_index("ix_<class 'application.models.DTM'>_index", "<class 'application.models.DTM'>", ['index'], unique=False)
    # ### end Alembic commands ###
