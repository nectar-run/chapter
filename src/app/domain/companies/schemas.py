from __future__ import annotations

from uuid import UUID  # noqa: TCH003

import msgspec

from app.db.models.company import Company
from app.lib.schema import CamelizedBaseStruct, Location, Funding


class Company(CamelizedBaseStruct):
    """A company."""
    id: UUID
    slug: str
    name: str
    description: str | None = None
    type: str | None = None
    industry: str | None = None
    headcount: int | None = None
    founded_year: int | None = None
    url: str | None = None
    profile_pic_url: str | None = None
    linkedin_profile_url: str | None = None
    hq_location: Location | None = None
    last_funding: Funding | None = None


class CompanyCreate(CamelizedBaseStruct):
    """A company create schema."""
    name: str
    description: str | None = None
    type: str | None = None
    industry: str | None = None
    headcount: int | None = None
    founded_year: int | None = None
    url: str | None = None
    profile_pic_url: str | None = None
    linkedin_profile_url: str | None = None
    hq_location: Location | None = None
    last_funding: Funding | None = None


class CompanyUpdate(CamelizedBaseStruct, omit_defaults=True):
    """A company update schema."""
    id: UUID
    name: str | None | msgspec.UnsetType = msgspec.UNSET
    description: str | None | msgspec.UnsetType = msgspec.UNSET
    type: str | None | msgspec.UnsetType = msgspec.UNSET
    industry: str | None | msgspec.UnsetType = msgspec.UNSET
    headcount: int | None | msgspec.UnsetType = msgspec.UNSET
    founded_year: int | None | msgspec.UnsetType = msgspec.UNSET
    url: str | None | msgspec.UnsetType = msgspec.UNSET
    profile_pic_url: str | None | msgspec.UnsetType = msgspec.UNSET
    linkedin_profile_url: str | None | msgspec.UnsetType = msgspec.UNSET
    hq_location: Location | None | msgspec.UnsetType = msgspec.UNSET
    last_funding: Funding | None | msgspec.UnsetType = msgspec.UNSET
