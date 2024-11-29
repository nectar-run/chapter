# type: ignore
"""Make opportunity_audit_log.user_id nullable and opportunity.company_id unique

Revision ID: 7d7f3e31dfbe
Revises: db999dc8a9fd
Create Date: 2024-09-03 10:33:11.676562+00:00

"""
from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op
from advanced_alchemy.types import EncryptedString, EncryptedText, GUID, ORA_JSONB, DateTimeUTC
from sqlalchemy import Text  # noqa: F401

if TYPE_CHECKING:
    from collections.abc import Sequence

__all__ = ["downgrade", "upgrade", "schema_upgrades", "schema_downgrades", "data_upgrades", "data_downgrades"]

sa.GUID = GUID
sa.DateTimeUTC = DateTimeUTC
sa.ORA_JSONB = ORA_JSONB
sa.EncryptedString = EncryptedString
sa.EncryptedText = EncryptedText

# revision identifiers, used by Alembic.
revision = "7d7f3e31dfbe"
down_revision = "db999dc8a9fd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        with op.get_context().autocommit_block():
            schema_upgrades()
            data_upgrades()


def downgrade() -> None:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        with op.get_context().autocommit_block():
            data_downgrades()
            schema_downgrades()


def schema_upgrades() -> None:
    """schema upgrade migrations go here."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("opportunity", schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f("uq_opportunity_company_id"), ["company_id"])

    with op.batch_alter_table("opportunity_audit_log", schema=None) as batch_op:
        batch_op.alter_column("user_id", existing_type=sa.UUID(), nullable=True)

    # ### end Alembic commands ###


def schema_downgrades() -> None:
    """schema downgrade migrations go here."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("opportunity_audit_log", schema=None) as batch_op:
        batch_op.alter_column("user_id", existing_type=sa.UUID(), nullable=False)

    with op.batch_alter_table("opportunity", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("uq_opportunity_company_id"), type_="unique")

    # ### end Alembic commands ###


def data_upgrades() -> None:
    """Add any optional data upgrade migrations here!"""


def data_downgrades() -> None:
    """Add any optional data downgrade migrations here!"""
