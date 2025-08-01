from alembic import op
import sqlalchemy as sa

revision = '001_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'accounts',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('mastodon_account_id', sa.Text, nullable=False, unique=True),
        sa.Column('acct', sa.Text, nullable=False),
        sa.Column('domain', sa.Text, nullable=False),
        sa.Column('last_checked_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('last_status_seen_id', sa.Text)
    )
    op.create_table(
        'analyses',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('mastodon_account_id', sa.Text, nullable=False),
        sa.Column('status_id', sa.Text),
        sa.Column('rule_key', sa.Text, nullable=False),
        sa.Column('score', sa.Numeric, nullable=False),
        sa.Column('evidence', sa.JSON, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
    )
    op.create_index('idx_analyses_account', 'analyses', ['mastodon_account_id'])
    op.create_index('idx_analyses_created', 'analyses', ['created_at'])
    op.create_table(
        'reports',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('mastodon_account_id', sa.Text, nullable=False),
        sa.Column('status_id', sa.Text),
        sa.Column('mastodon_report_id', sa.Text),
        sa.Column('dedupe_key', sa.Text, nullable=False, unique=True),
        sa.Column('comment', sa.Text, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
    )
    op.create_table(
        'cursors',
        sa.Column('name', sa.Text, primary_key=True),
        sa.Column('position', sa.Text, nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
    )
    op.create_table(
        'rate_limits',
        sa.Column('bucket', sa.Text, primary_key=True),
        sa.Column('reset_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('remaining', sa.Integer, nullable=False),
        sa.Column('limit', sa.Integer, nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
    )
    op.create_table(
        'config',
        sa.Column('key', sa.Text, primary_key=True),
        sa.Column('value', sa.JSON, nullable=False),
        sa.Column('updated_by', sa.Text),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
    )

def downgrade():
    op.drop_table('config')
    op.drop_table('rate_limits')
    op.drop_table('cursors')
    op.drop_table('reports')
    op.drop_index('idx_analyses_created', table_name='analyses')
    op.drop_index('idx_analyses_account', table_name='analyses')
    op.drop_table('analyses')
    op.drop_table('accounts')
