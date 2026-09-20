"""add schedule week number

Revision ID: 6d1b78a43e2f
Revises: 823f4c5dc8b6
Create Date: 2026-09-20

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "6d1b78a43e2f"
down_revision: Union[str, Sequence[str], None] = "823f4c5dc8b6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "schedules",
        sa.Column("week_number", sa.Integer(), nullable=False, server_default=sa.text("1")),
    )
    op.create_check_constraint(
        "ck_schedule_week_number",
        "schedules",
        "week_number IN (1, 2)",
    )


def downgrade() -> None:
    op.drop_constraint("ck_schedule_week_number", "schedules", type_="check")
    op.drop_column("schedules", "week_number")
