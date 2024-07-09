from pydantic import Field

from .base import IDEX


class UomInfo(IDEX):
    id: str


class UnitType(IDEX):
    id: str
    name: str
    member_uoms: list[UomInfo]


class ConversionRequest(IDEX):
    include_source_values_in_response: bool = Field(default=False)
    source_uom_id: str
    target_uom_id: str
    values: list[float]


class ConversionResponse(IDEX):
    source_uom_id: str
    target_uom_id: str
    converted_values: list[float]
    source_values: list[float]
