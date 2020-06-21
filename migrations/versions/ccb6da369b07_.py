"""empty message

Revision ID: ccb6da369b07
Revises: d3936f9df8ee
Create Date: 2020-06-17 18:01:47.051028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccb6da369b07'
down_revision = 'd3936f9df8ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Actor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('gender', sa.String(length=1), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('Movie',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=False),
    sa.Column('release_year', sa.String(length=4), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('Related',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('actor_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['actor_id'], ['Actor.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['movie_id'], ['Movie.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('movie_actor_table')
    op.drop_table('actors_table')
    op.drop_table('movies_table')
    # op.create_foreign_key(None, 'movie_actor_table', 'Movie', ['movie_id'],
    # ['id'], ondelete="CASCADE")
    # op.create_foreign_key(None, 'movie_actor_table', 'Actor', ['actor_id'],
    # ['id'], ondelete="CASCADE")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'movie_actor_table', type_='foreignkey')
    op.drop_constraint(None, 'movie_actor_table', type_='foreignkey')
    op.create_foreign_key('movie_actor_table_movie_id_fkey', 'movie_actor_table', 'movies_table', ['movie_id'], ['id'])
    op.create_foreign_key('movie_actor_table_actor_id_fkey', 'movie_actor_table', 'actors_table', ['actor_id'], ['id'])
    op.create_table('movies_table',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('movies_table_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=256), autoincrement=False, nullable=False),
    sa.Column('release_year', sa.VARCHAR(length=4), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='movies_table_pkey'),
    sa.UniqueConstraint('title', name='movies_table_title_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('actors_table',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('age', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('gender', sa.VARCHAR(length=1), autoincrement=False, nullable=False),
    sa.Column('movie_list', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['movie_list'], ['movies_table.id'], name='actors_table_movies_fkey'),
    sa.PrimaryKeyConstraint('id', name='actors_table_pkey'),
    sa.UniqueConstraint('name', name='actors_table_name_key')
    )
    op.drop_table('Related')
    op.drop_table('Movie')
    op.drop_table('Actor')
    # ### end Alembic commands ###
