"""Contains Schemas for Physical assets."""

from datetime import datetime
from typing import Optional

from pydantic import Field as PField

from .base import IDEX, DoubleNullableUomValue, IDEXAudit, IDEXAuditLite


class Wellbore(IDEXAudit):
    id: str
    name: str
    well_id: Optional[str]
    item_state: Optional[str]


class Well(IDEXAudit):
    id: str
    name: Optional[str] = PField(default=None)
    facility: Optional[str] = PField(default=None)
    field: Optional[str] = PField(default=None)
    installation: Optional[str] = PField(default=None)
    item_state: Optional[str] = PField(default=None)
    latitude: Optional[float] = PField(default=None)
    longitude: Optional[float] = PField(default=None)
    operator: Optional[str] = PField(default=None)
    region: Optional[str] = PField(default=None)
    time_zone: Optional[str] = PField(default=None)
    well_number: Optional[str] = PField(default=None)
    reference_point: Optional[str] = PField(default=None)
    operator_id: Optional[str] = PField(default=None)
    field_id: Optional[str] = PField(default=None)
    installation_id: Optional[str] = PField(default=None)
    reference_point_elevation: Optional[DoubleNullableUomValue] = PField(default=None)


class WellboreLiveStatus(IDEXAudit):
    id: str
    wellbore_id: str
    is_live: bool
    is_live_last_changed: datetime
    is_depth_live: bool
    is_depth_live_last_changed: datetime
    created_by: Optional[str]
    modified_by: Optional[str]
    deleted_by: Optional[str]


class Unit(IDEX):
    id: str
    name: str
    type: str


class Equipment(IDEXAuditLite):
    id: str
    manufacturer: Optional[str]
    manufactured_date: Optional[datetime]
    next_maintenance_type: Optional[str]
    next_maintenance_alarm_type: Optional[str]
    next_maintenance_date: Optional[datetime]
    next_maintenance_days_left: DoubleNullableUomValue
    next_maintenance_meterage_left: DoubleNullableUomValue
    total_dhrm: DoubleNullableUomValue = PField(alias="totalDHRM")


class Reel(Equipment):
    core_diameter: DoubleNullableUomValue
    outer_diameter: DoubleNullableUomValue
    coiled_tubing_string: Optional[str]
    assigned_to: Optional[str]
    width: DoubleNullableUomValue
    coil_avg_life_consumption_percentage: DoubleNullableUomValue
    coil_max_life_consumption_percentage: DoubleNullableUomValue
    coil_max_life_consumption_position: DoubleNullableUomValue


class InjectorHead(Equipment):
    type: Optional[str]
    max_lifting_capacity: DoubleNullableUomValue
    total_assembled_weight: DoubleNullableUomValue
    calculate_dhrm_from_date: Optional[datetime] = PField(alias="calculateDHRMFromDate")
    initial_dhrm: DoubleNullableUomValue = PField(alias="initialDHRM")
    added_dhrm: DoubleNullableUomValue = PField(alias="addedDHRM")
    status: Optional[str]
    serial_number: Optional[str]
    gooseneck_radius: DoubleNullableUomValue
    assigned_to: Optional[str]
    district: Optional[str]


class Field(IDEXAudit):
    id: str
    name: Optional[str]


class Customer(IDEXAudit):
    id: str
    name: Optional[str]
    street_address: Optional[str]


class _Tangible(IDEX):
    type: Optional[str]
    od: DoubleNullableUomValue
    id: DoubleNullableUomValue
    weight_per_length: DoubleNullableUomValue = PField(alias="weightPrLength")
    md_top: DoubleNullableUomValue
    md_bottom: DoubleNullableUomValue
    abs_roughness: DoubleNullableUomValue
    comment: Optional[str]


class Casing(_Tangible): ...


class Completion(_Tangible):
    drift: DoubleNullableUomValue


class Deposit(IDEX):
    type: Optional[str]
    md_top: DoubleNullableUomValue
    md_bottom: DoubleNullableUomValue
    inner_diameter: DoubleNullableUomValue
    comment: Optional[str]
    label: Optional[str]
    relative_roughness: DoubleNullableUomValue


class Fish(IDEX):
    type: Optional[str]
    other_text: Optional[str]
    cable_type: Optional[str]
    bha_id: Optional[str]
    md_top: DoubleNullableUomValue
    outer_diameter: DoubleNullableUomValue
    inner_diameter: DoubleNullableUomValue = PField(alias="innerDiameters")
    weight: DoubleNullableUomValue
    comment: Optional[str]
    label: Optional[str]


class OpenHole(IDEX):
    hole_diameter: DoubleNullableUomValue
    md_top: DoubleNullableUomValue
    md_bottom: DoubleNullableUomValue
    abs_roughness: DoubleNullableUomValue
    comment: Optional[str]
