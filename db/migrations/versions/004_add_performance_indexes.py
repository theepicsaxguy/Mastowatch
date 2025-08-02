from alembic import op
import sqlalchemy as sa

revision = '004_add_performance_indexes'
down_revision = '003_add_foreign_keys'
branch_labels = None
depends_on = None

def upgrade():
    # Indexes for Analysis table
    op.create_index('ix_analyses_rule_key', 'analyses', ['rule_key'])
    op.create_index('ix_analyses_created_at', 'analyses', ['created_at'])
    op.create_index('ix_analyses_mastodon_account_id_created_at', 'analyses', ['mastodon_account_id', 'created_at'])
    
    # Indexes for Report table  
    op.create_index('ix_reports_created_at', 'reports', ['created_at'])
    op.create_index('ix_reports_mastodon_account_id_created_at', 'reports', ['mastodon_account_id', 'created_at'])
    
    # Indexes for Account table
    op.create_index('ix_accounts_domain', 'accounts', ['domain'])
    op.create_index('ix_accounts_last_checked_at', 'accounts', ['last_checked_at'])
    op.create_index('ix_accounts_acct', 'accounts', ['acct'])

def downgrade():
    # Drop indexes in reverse order
    op.drop_index('ix_accounts_acct', 'accounts')
    op.drop_index('ix_accounts_last_checked_at', 'accounts')
    op.drop_index('ix_accounts_domain', 'accounts')
    op.drop_index('ix_reports_mastodon_account_id_created_at', 'reports')
    op.drop_index('ix_reports_created_at', 'reports')
    op.drop_index('ix_analyses_mastodon_account_id_created_at', 'analyses')
    op.drop_index('ix_analyses_created_at', 'analyses')
    op.drop_index('ix_analyses_rule_key', 'analyses')
