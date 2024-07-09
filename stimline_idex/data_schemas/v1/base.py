from datetime import datetime, timedelta
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


def to_camel(string: str) -> str:
    """Convert snake_case string to camelCase."""
    string_split = string.split("_")
    return string_split[0] + "".join(word.capitalize() for word in string_split[1:])


class IDEX(BaseModel):
    """Base class for all IDEX data models."""

    model_config = ConfigDict(alias_generator=to_camel)

    ...


class IDEXAuditLite(IDEX):
    """For subclasses with API audit fields."""

    id: UUID
    created_date: Optional[datetime] = Field(default=None)
    modified_date: Optional[datetime] = Field(default=None)


class IDEXAudit(IDEXAuditLite):
    """For subclasses with API audit fields incl. deleted date."""

    deleted_date: Optional[datetime] = Field(default=None)


class Range(IDEX):
    """Describes a Range."""

    id: str
    start: datetime
    end: datetime


class TimeRange(IDEX):
    """Describes a Time Range."""

    start: datetime
    end: datetime


class TimeDuration(IDEX):
    """Describes a Time Duration."""

    type: Optional[str]
    duration: timedelta


class DoubleNullableUomValue(IDEX):
    """Describes a nullable value with unit."""

    value: Optional[float]
    uom: Optional[str]


class Approval(IDEX):
    """Describes an Approval."""

    name: Optional[str]
    approved: bool


class Change(IDEX):
    """Describes a Change in Changelog."""

    id: Optional[str]
    anchor: int
    type: Optional[str]
    source: Optional[str]
    created_date: datetime
