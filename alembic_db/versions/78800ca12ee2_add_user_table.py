"""Add user table

Revision ID: 78800ca12ee2
Revises: 85c7a14070d1
Create Date: 2021-12-07 10:13:57.754624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "78800ca12ee2"
down_revision = "85c7a14070d1"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    pass


def downgrade():
    op.drop_table("users")
    pass
