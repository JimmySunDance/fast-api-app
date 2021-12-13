"""Add content column to posts table

Revision ID: 85c7a14070d1
Revises: 74b5105029b1
Create Date: 2021-12-07 10:08:52.826320

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "85c7a14070d1"
down_revision = "74b5105029b1"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
