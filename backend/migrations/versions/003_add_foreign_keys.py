from alembic import op

revision = '003_add_foreign_keys'
down_revision = '002_drop_rate_limits'
branch_labels = None
depends_on = None

def upgrade():
    op.create_foreign_key(
        'fk_analyses_mastodon_account_id',
        'analyses',
        'accounts',
        ['mastodon_account_id'],
        ['mastodon_account_id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'fk_reports_mastodon_account_id',
        'reports',
        'accounts',
        ['mastodon_account_id'],
        ['mastodon_account_id'],
        ondelete='CASCADE'
    )

def downgrade():
    op.drop_constraint('fk_reports_mastodon_account_id', 'reports', type_='foreignkey')
    op.drop_constraint('fk_analyses_mastodon_account_id', 'analyses', type_='foreignkey')
