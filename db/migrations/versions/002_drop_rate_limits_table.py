from alembic import op
import sqlalchemy as sa

revision = '002_drop_rate_limits'
down_revision = '001_init'
branch_labels = None
depends_on = None

def upgrade():
    # Only drop if exists for idempotency across environments
    conn = op.get_bind()
    res = conn.execute(sa.text(
        "SELECT to_regclass('public.rate_limits')"
    )).scalar()
    if res:
        op.drop_table('rate_limits')

def downgrade():
    op.create_table(
        'rate_limits',
        sa.Column('bucket', sa.Text, primary_key=True),
        sa.Column('reset_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('remaining', sa.Integer, nullable=False),
        sa.Column('limit', sa.Integer, nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
    )