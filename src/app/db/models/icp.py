from __future__ import annotations

from uuid import UUID

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import String, ForeignKey, Index, UniqueConstraint, asc
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.lib.schema import CompanyCriteria, ToolCriteria, PersonCriteria, ProcessCriteria
from .custom_types import CompanyCriteriaType, ToolCriteriaType, PersonCriteriaType, ProcessCriteriaType


class ICP(UUIDAuditBase):
    """ICP criteria."""

    __tablename__ = "icp"
    __table_args__ = (
        Index("ix_icp_id", "id"),
        Index("idx_icp_tenant_id_created_at", "tenant_id", asc("created_at")),
        UniqueConstraint("name", "tenant_id", name="uix_name_tenant_id"),
    )
    name: Mapped[str] = mapped_column(nullable=False)
    company: Mapped[CompanyCriteria] = mapped_column(CompanyCriteriaType, nullable=True)
    tool: Mapped[ToolCriteria] = mapped_column(ToolCriteriaType, nullable=True)
    process: Mapped[ProcessCriteria] = mapped_column(ProcessCriteriaType, nullable=True)
    person: Mapped[PersonCriteria] = mapped_column(PersonCriteriaType, nullable=True, default="identified", index=True)
    tenant_id: Mapped[UUID] = mapped_column(ForeignKey("tenant.id"), nullable=False, index=True)
    pitch: Mapped[str | None] = mapped_column(String(length=500), nullable=True, default=None)
