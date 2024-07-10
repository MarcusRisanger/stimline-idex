from datetime import datetime
from typing import Any, Optional

from pydantic import Field

from .base import IDEX, IDEXAudit


class Range(IDEX):
    """Describes a Range."""

    channel_id: str = Field(alias="id")
    start: datetime
    end: datetime


class TimeRange(IDEX):
    """Describes a Time Range."""

    start: datetime
    end: datetime


class DataPoint(IDEX):
    time: datetime
    value: Any


class ChannelDataResponse(IDEX):
    id: str
    points: Optional[list[DataPoint]]


class ChannelDataRequest(IDEX):
    ids: list[str]
    start: Optional[datetime]
    end: Optional[datetime]
    limit: int
    ignore_unknown_ids: bool
    include_outside_points: bool


class Channel(IDEXAudit):
    id: str
    name: Optional[str]
    global_name: Optional[str]
    description: Optional[str]
    uom: Optional[str]
    uom_class: Optional[str]
    data_type: Optional[str]
    index_type: Optional[str]
    status: Optional[str]
    range: TimeRange
    log_id: Optional[str] = Field(default=None)  # Added manually
    run_id: Optional[str] = Field(default=None)  # Added manually
