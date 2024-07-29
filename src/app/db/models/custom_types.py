from __future__ import annotations

import json
from dataclasses import dataclass, asdict

from sqlalchemy.types import TypeDecorator, TEXT
from sqlalchemy.dialects.postgresql import JSONB

from app.lib.schema import Location, Funding


class JSONBType(TypeDecorator):
    impl = JSONB  # Use the PostgreSQL JSONB type as base

    def process_bind_param(self, value, dialect):
        """Convert Python object to JSON format before storing it in the database."""
        if isinstance(value, dict):
            return value
        elif hasattr(value, 'to_dict'):
            return value.to_dict()
        return value

    def process_result_value(self, value, dialect):
        """Convert JSON format to Python object when reading from the database."""
        if value:
            return json.loads(value)
        return None


class LocationType(JSONBType):
    def process_result_value(self, value, dialect):
        """Convert JSON format to Python object when reading from the database."""
        if value and isinstance(value, dict):
            return Location.from_dict(value)
        return None


class FundingType(JSONBType):
    def process_result_value(self, value, dialect):
        """Convert JSON format to Python object when reading from the database."""
        if value and isinstance(value, dict):
            return Funding.from_dict(value)
        return None
