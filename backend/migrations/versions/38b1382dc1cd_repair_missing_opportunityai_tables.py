"""Repair missing OpportunityAI tables.

Revision ID: 38b1382dc1cd
Revises: 4cb38e74f440

The required tables are already created by the preceding migrations.
This revision is retained to preserve the existing migration history.
"""

# Revision identifiers, used by Alembic.
revision = '38b1382dc1cd'
down_revision = '4cb38e74f440'
branch_labels = None
depends_on = None


def upgrade():
    """No operation: preceding migrations create the required tables."""
    pass


def downgrade():
    """No operation: preserve tables managed by preceding migrations."""
    pass