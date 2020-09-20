"""Initial migration

Revision ID: 2a3f240d31ae
Revises:
Create Date: 2020-09-19 23:19:50.441982

"""
from alembic import op
import sqlalchemy as sa


revision = '2a3f240d31ae'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'company',
        sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('railway_id', sa.SmallInteger(), nullable=False),
        sa.Column('common_name', sa.String(length=256), nullable=False),
        sa.Column('kana_name', sa.String(length=256), nullable=True),
        sa.Column('official_name', sa.String(length=256), nullable=True),
        sa.Column('short_name', sa.String(length=256), nullable=True),
        sa.Column('url', sa.String(length=512), nullable=True),
        sa.Column('category', sa.SmallInteger(), nullable=True),
        sa.Column('status', sa.SmallInteger(), nullable=True),
        sa.Column('sort_code', sa.SmallInteger(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'prefecture',
        sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('name', sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table(
        'line',
        sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.Column('common_name', sa.String(length=256), nullable=False),
        sa.Column('kana_name', sa.String(length=256), nullable=True),
        sa.Column('official_name', sa.String(length=256), nullable=True),
        sa.Column('color_code', sa.String(length=8), nullable=True),
        sa.Column('color_name', sa.String(length=32), nullable=True),
        sa.Column('category', sa.SmallInteger(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('zoom_size', sa.SmallInteger(), nullable=True),
        sa.Column('status', sa.SmallInteger(), nullable=True),
        sa.Column('sort_code', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'station',
        sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('group_id', sa.Integer(), nullable=False),
        sa.Column('common_name', sa.String(length=256), nullable=False),
        sa.Column('kana_name', sa.String(length=256), nullable=True),
        sa.Column('romaji_name', sa.String(length=256), nullable=True),
        sa.Column('line_id', sa.Integer(), nullable=False),
        sa.Column('prefecture_id', sa.SmallInteger(), nullable=True),
        sa.Column('post_code', sa.String(length=32), nullable=True),
        sa.Column('address', sa.String(length=1024), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('open_date', sa.DateTime(), nullable=True),
        sa.Column('close_date', sa.DateTime(), nullable=True),
        sa.Column('status', sa.SmallInteger(), nullable=True),
        sa.Column('sort_code', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['line_id'], ['line.id'], ),
        sa.ForeignKeyConstraint(['prefecture_id'], ['prefecture.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'connecting_station',
        sa.Column(
            'line_id',
            sa.Integer(),
            autoincrement=False,
            nullable=False
        ),
        sa.Column(
            'station_id_1',
            sa.Integer(),
            autoincrement=False,
            nullable=False
        ),
        sa.Column(
            'station_id_2',
            sa.Integer(),
            autoincrement=False,
            nullable=False
        ),
        sa.ForeignKeyConstraint(['line_id'], ['line.id'], ),
        sa.ForeignKeyConstraint(['station_id_1'], ['station.id'], ),
        sa.ForeignKeyConstraint(['station_id_2'], ['station.id'], ),
        sa.PrimaryKeyConstraint('line_id', 'station_id_1', 'station_id_2')
    )

    op.create_index(
        op.f('ix_company_railway_id'),
        'company',
        ['railway_id'],
        unique=False
    )
    op.create_index(
        op.f('ix_line_company_id'),
        'line',
        ['company_id'],
        unique=False
    )
    op.create_index(
        op.f('ix_station_group_id'),
        'station',
        ['group_id'],
        unique=False
    )
    op.create_index(
        op.f('ix_station_line_id'),
        'station',
        ['line_id'],
        unique=False
    )
    op.create_index(
        op.f('ix_station_prefecture_id'),
        'station',
        ['prefecture_id'],
        unique=False
    )


def downgrade():
    op.drop_table('connecting_station')
    op.drop_table('station')
    op.drop_table('line')
    op.drop_table('prefecture')
    op.drop_table('company')

    op.drop_index(op.f('ix_station_prefecture_id'), table_name='station')
    op.drop_index(op.f('ix_station_line_id'), table_name='station')
    op.drop_index(op.f('ix_station_group_id'), table_name='station')
    op.drop_index(op.f('ix_line_company_id'), table_name='line')
    op.drop_index(op.f('ix_company_railway_id'), table_name='company')
