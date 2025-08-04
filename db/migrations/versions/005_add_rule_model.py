from alembic import op
import sqlalchemy as sa

revision = '005_add_rule_model'
down_revision = '004_add_performance_indexes'
branch_labels = None
depends_on = None

def upgrade():
    # Create rules table
    op.create_table('rules',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('rule_type', sa.Text(), nullable=False),
        sa.Column('pattern', sa.Text(), nullable=False),
        sa.Column('weight', sa.Numeric(), nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=False, default=True),
        sa.Column('is_default', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for performance
    op.create_index('ix_rules_rule_type', 'rules', ['rule_type'])
    op.create_index('ix_rules_enabled', 'rules', ['enabled'])
    op.create_index('ix_rules_is_default', 'rules', ['is_default'])

def downgrade():
    # Drop indexes first
    op.drop_index('ix_rules_is_default', 'rules')
    op.drop_index('ix_rules_enabled', 'rules')
    op.drop_index('ix_rules_rule_type', 'rules')
    
    # Drop the table
    op.drop_table('rules')
