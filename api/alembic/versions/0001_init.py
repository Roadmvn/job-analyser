"""init schema

Revision ID: 0001_init
Revises: 
Create Date: 2025-08-18 00:00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'companies',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False, unique=True),
    )
    op.create_table(
        'sources',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False, unique=True),
    )
    op.create_table(
        'jobs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('source_id', sa.Integer(), sa.ForeignKey('sources.id'), nullable=True),
        sa.Column('external_id', sa.String(length=255), nullable=True),
        sa.Column('company', sa.String(length=255), nullable=True),
        sa.Column('title', sa.String(length=512), nullable=False),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('sector', sa.String(length=255), nullable=True),
        sa.Column('contract_type', sa.String(length=100), nullable=True),
        sa.Column('salary_min', sa.Integer(), nullable=True),
        sa.Column('salary_max', sa.Integer(), nullable=True),
        sa.Column('currency', sa.String(length=10), nullable=True),
        sa.Column('url', sa.String(length=1024), nullable=False),
        sa.Column('posted_at', sa.DateTime(), nullable=True),
        sa.Column('raw_description', sa.Text(), nullable=False),
        sa.Column('hash', sa.String(length=64), nullable=False, unique=True),
    )
    op.create_index('ix_jobs_title', 'jobs', ['title'])
    op.create_index('ix_jobs_location', 'jobs', ['location'])
    op.create_index('ix_jobs_sector', 'jobs', ['sector'])
    op.create_index('ix_jobs_contract_type', 'jobs', ['contract_type'])
    op.create_index('ix_jobs_posted_at', 'jobs', ['posted_at'])
    # FULLTEXT index in MySQL
    op.execute('CREATE FULLTEXT INDEX ix_jobs_fulltext_title_desc ON jobs (title, raw_description)')

    op.create_table(
        'skills',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False, unique=True),
    )
    op.create_table(
        'job_skills',
        sa.Column('job_id', sa.Integer(), sa.ForeignKey('jobs.id'), primary_key=True),
        sa.Column('skill_id', sa.Integer(), sa.ForeignKey('skills.id'), primary_key=True),
    )
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('plan', sa.String(length=20), nullable=False, server_default='free'),
    )
    op.create_table(
        'resumes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )
    op.create_table(
        'feedback',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('resume_id', sa.Integer(), sa.ForeignKey('resumes.id'), nullable=False),
        sa.Column('notes', sa.Text(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('feedback')
    op.drop_table('resumes')
    op.drop_table('users')
    op.drop_table('job_skills')
    op.drop_table('skills')
    op.drop_index('ix_jobs_posted_at', table_name='jobs')
    op.drop_index('ix_jobs_contract_type', table_name='jobs')
    op.drop_index('ix_jobs_sector', table_name='jobs')
    op.drop_index('ix_jobs_location', table_name='jobs')
    op.drop_index('ix_jobs_title', table_name='jobs')
    op.execute('DROP INDEX ix_jobs_fulltext_title_desc ON jobs')
    op.drop_table('jobs')
    op.drop_table('sources')
    op.drop_table('companies')


