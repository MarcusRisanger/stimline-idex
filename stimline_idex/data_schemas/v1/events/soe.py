from pydantic import Field
from ..base import IDEX, IDEXAuditLite, DoubleNullableUomValue
from uuid import UUID
from datetime import datetime
from typing import Optional


class SoeSensorValues(IDEX):
    """Describes a sensor value for a given Job."""

    name: Optional[str]
    global_name: Optional[str]
    uom: Optional[str]
    start_value: Optional[float]
    end_value: Optional[float]
    max_value: Optional[float]
    min_value: Optional[float]
    avg_value: Optional[float]


class SoeActivity(IDEXAuditLite):
    """Describes an Activity in a SoeTask."""

    task_id: UUID
    name: Optional[str]
    type: Optional[str]
    start: Optional[datetime]
    end: Optional[datetime]
    duration: Optional[str]
    sensor_values: list[SoeSensorValues]
    comment: Optional[str]


class SoeTask(IDEXAuditLite):
    """Describes a SoeTask for a given Job."""

    job_id: UUID
    name: Optional[str]
    conveyance_type: Optional[str]
    activities_count: int
    sequence_number: int
    state: Optional[str]
    start: Optional[datetime]
    end: Optional[datetime]
    running_down_length: DoubleNullableUomValue
    running_up_length: DoubleNullableUomValue
    running_total_length: DoubleNullableUomValue
    max_depth: DoubleNullableUomValue
    wellbore_id: Optional[str] = Field(default=None)  # Not part of the payload - added separately


class SoeChemicalMeasurement(IDEX):
    """Describes a chemical measurement for an Activity."""

    id: UUID
    job_id: UUID
    date: datetime
    type: Optional[str]
    value: float
    uom: Optional[str]
    comment: Optional[str]


class SoeJob(IDEXAuditLite):
    """Describes a Sequence of Events (Soe) Job."""

    wellbore_id: UUID
    name: Optional[str]
    start: Optional[datetime]
    end: Optional[datetime]
    job_type_name: Optional[str]
