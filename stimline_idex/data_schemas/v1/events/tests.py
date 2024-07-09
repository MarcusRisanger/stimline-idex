from datetime import timedelta
from pydantic import Field
from ..base import IDEX
from typing import Optional


class _TestBase(IDEX):
    """Common fields for all tests."""

    wellbore: Optional[str]
    start_time: Optional[str]
    end_time: Optional[str]
    sensor_name: Optional[str]
    created_date: Optional[str]
    comment: Optional[str]
    result: Optional[str]
    user: Optional[str]


class _StartEndPressureTest(_TestBase):
    """Common fields for many pressure tests."""

    start_pressure_bar: Optional[float]
    end_pressure_bar: Optional[float]
    duration: timedelta


class _BuildUpTest(_StartEndPressureTest):
    result_percentage: Optional[float]
    result_bar: Optional[float]


class ApiBuildUpTest(_BuildUpTest): ...


class QtsTest(_BuildUpTest): ...


class InflowTest(_BuildUpTest):
    """Describes a flow test: InflowTest."""

    delta_bar: Optional[float]


class Inflow30MinTest(InflowTest): ...


class PressureTest(_TestBase):
    """Describes a pressure test."""

    lp_start_pressure_bar: Optional[float]
    lp_end_pressure_bar: Optional[float]
    lp_duration: timedelta
    lp_result_percentage: Optional[float]
    lp_result_bar: Optional[float]
    lp_reference_delta_p_bar: Optional[float]
    hp_start_pressure_bar: Optional[float]
    hp_end_pressure_bar: Optional[float]
    hp_duration: timedelta
    hp_result_percentage: Optional[float]
    hp_result_bar: Optional[float]


class _ApiLeakRateTest(_StartEndPressureTest):
    """Describes an API leak rate test."""

    volume_m3: Optional[float]
    temperature_c: Optional[float]
    fluid_type: Optional[str]
    leak_rate_lpm: Optional[float] = Field(alias="leakRateLperMin")
    criteria_lpm: Optional[float] = Field(alias="criteriaLperMin")


class XmtHmvApiLeakRateTest(_ApiLeakRateTest): ...


class XmtLmvApiLeakRateTest(_ApiLeakRateTest): ...


class SssvApiLeakRateTest(_ApiLeakRateTest):
    """Describes a SSSV API leak rate test."""

    sssv_depth_meter: Optional[float]


class AsvApiLeakRateTest(_ApiLeakRateTest):
    """Describe an ASV API leak rate test."""

    asv_depth_meter: Optional[float]
