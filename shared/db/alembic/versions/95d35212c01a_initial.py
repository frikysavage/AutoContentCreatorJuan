"""initial

Revision ID: 95d35212c01a
Revises: 
Create Date: 2026-09-17 16:34:09.363119

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95d35212c01a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'accounts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(), nullable=True),
        sa.Column('categoria_default', sa.String(), nullable=True),
        sa.Column('idioma_default', sa.String(), nullable=True),
        sa.Column('duracion_default', sa.Integer(), nullable=True),
        sa.Column('formato_default', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_accounts_id'), 'accounts', ['id'], unique=False)
    op.create_index(op.f('ix_accounts_nombre'), 'accounts', ['nombre'], unique=False)

    op.create_table(
        'character_sheets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=True),
        sa.Column('estilo', sa.String(), nullable=True),
        sa.Column('rasgos_fijos', sa.String(), nullable=True),
        sa.Column('paleta', sa.String(), nullable=True),
        sa.Column('vestuario_base', sa.String(), nullable=True),
        sa.Column('creado_en', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_character_sheets_id'), 'character_sheets', ['id'], unique=False)

    op.create_table(
        'video_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=True),
        sa.Column('resumen_para_historial', sa.String(), nullable=True),
        sa.Column('creado_en', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_video_history_id'), 'video_history', ['id'], unique=False)

    op.create_table(
        'video_jobs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=True),
        sa.Column('tema', sa.String(), nullable=True),
        sa.Column('guion', sa.String(), nullable=True),
        sa.Column('titulo_seo', sa.String(), nullable=True),
        sa.Column('resumen_para_historial', sa.String(), nullable=True),
        sa.Column('duracion_segundos', sa.Integer(), nullable=True),
        sa.Column('musica', sa.String(), nullable=True),
        sa.Column('subtitulos', sa.Boolean(), nullable=True),
        sa.Column('synthetic_content', sa.Boolean(), nullable=True),
        sa.Column('video_id_youtube', sa.String(), nullable=True),
        sa.Column('review_token', sa.String(), nullable=True),
        sa.Column('estado', sa.String(), nullable=True),
        sa.Column('creado_en', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_video_jobs_id'), 'video_jobs', ['id'], unique=False)
    op.create_index(op.f('ix_video_jobs_review_token'), 'video_jobs', ['review_token'], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_video_jobs_review_token'), table_name='video_jobs')
    op.drop_index(op.f('ix_video_jobs_id'), table_name='video_jobs')
    op.drop_table('video_jobs')
    op.drop_index(op.f('ix_video_history_id'), table_name='video_history')
    op.drop_table('video_history')
    op.drop_index(op.f('ix_character_sheets_id'), table_name='character_sheets')
    op.drop_table('character_sheets')
    op.drop_index(op.f('ix_accounts_nombre'), table_name='accounts')
    op.drop_index(op.f('ix_accounts_id'), table_name='accounts')
    op.drop_table('accounts')
