"""Drop is_default column from rules table

Revision ID: 007_drop_is_default_column
Revises: 006_scanning_system
Create Date: 2025-02-14 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "007_drop_is_default_column"
down_revision = "006_scanning_system"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_index("ix_rules_is_default", table_name="rules")
    op.drop_column("rules", "is_default")


def downgrade():
    op.add_column(
        "rules",
        sa.Column("is_default", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.create_index("ix_rules_is_default", "rules", ["is_default"])
