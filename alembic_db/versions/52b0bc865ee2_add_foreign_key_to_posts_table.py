"""Add foreign-key to posts table

Revision ID: 52b0bc865ee2
Revises: 78800ca12ee2
Create Date: 2021-12-07 10:31:57.404794

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "52b0bc865ee2"
down_revision = "78800ca12ee2"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade():
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
