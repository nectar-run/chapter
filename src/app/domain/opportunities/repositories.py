from __future__ import annotations

from typing import TYPE_CHECKING, Any
from uuid import UUID  # noqa: TCH003

from advanced_alchemy.repository import SQLAlchemyAsyncSlugRepository
from sqlalchemy import ColumnElement, select
from sqlalchemy.orm import joinedload, InstrumentedAttribute

from app.db.models import Opportunity, OpportunityAuditLog

if TYPE_CHECKING:
    from advanced_alchemy.filters import FilterTypes
    from advanced_alchemy.repository._util import LoadSpec

__all__ = (
    "OpportunityRepository",
    "OpportunityAuditLogRepository"
)


class OpportunityRepository(SQLAlchemyAsyncSlugRepository[Opportunity]):
    """Opportunity Repository."""

    model_type = Opportunity

    async def get_opportunities(
        self,
        *filters: FilterTypes | ColumnElement[bool],
        tenant_id: UUID,
        auto_expunge: bool | None = None,
        force_basic_query_mode: bool | None = None,
        **kwargs: Any,
    ) -> tuple[list[Opportunity], int]:
        """Get paginated list and total count of opportunities that a tenant can access."""

        return await self.list_and_count(
            *filters,
            statement=select(Opportunity)
            .where(Opportunity.tenant_id == tenant_id),
            #.order_by(Opportunity.score.desc(), Opportunity.created_at.desc())
            auto_expunge=auto_expunge,
            force_basic_query_mode=force_basic_query_mode,
            **kwargs,
        )

    async def get_opportunity(
        self,
        opportunity_id: UUID,
        tenant_id: UUID,
        *,
        id_attribute: str | InstrumentedAttribute[Any] | None = None,
        load: LoadSpec | None = None,
        execution_options: dict[str, Any] | None = None,
        auto_expunge: bool | None = None,
    ) -> Opportunity:
        """Get an opportunity along with it's associated details."""
        return await self.repository.get_one(
            item_id=opportunity_id,
            auto_expunge=auto_expunge,
            statement=select(Opportunity)
            .where((Opportunity.id == opportunity_id) & (Opportunity.tenant_id == tenant_id))
            #.order_by(Opportunity.score.desc(), Opportunity.created_at.desc())
            .options(
                joinedload(Opportunity.contacts, innerjoin=False),
                joinedload(Opportunity.job_posts, innerjoin=False),
                joinedload(Opportunity.logs, innerjoin=False),
            ),
            id_attribute=id_attribute,
            load=load,
            execution_options=execution_options,
        )

class OpportunityAuditLogRepository(SQLAlchemyAsyncSlugRepository[OpportunityAuditLog]):
    """OpportunityAuditLog Repository."""

    model_type = OpportunityAuditLog
