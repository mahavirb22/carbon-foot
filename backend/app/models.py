"""Pydantic schemas — the validated contract between the API and its clients.

These models serve dual duty: they validate and bound every incoming field
(rejecting impossible or nonsensical values before any computation takes place)
and they generate the OpenAPI documentation surface. Bounded inputs are a
deliberate security measure — clients cannot submit unbounded or negative
quantities.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from app.carbon.factors import CarFuel, DietType

# Generous-but-finite upper bounds that prevent abuse without rejecting real users.
_MAX_KM_WEEK = 20_000.0
_MAX_KWH_MONTH = 100_000.0
_MAX_FLIGHTS = 200
_MAX_USD_MONTH = 1_000_000.0
_MAX_WASTE_WEEK = 1_000.0


class TransportInput(BaseModel):
    """Weekly travel habits and yearly flight counts."""

    car_km_per_week: float = Field(0, ge=0, le=_MAX_KM_WEEK)
    car_fuel: CarFuel = CarFuel.PETROL
    public_transit_km_per_week: float = Field(0, ge=0, le=_MAX_KM_WEEK)
    short_haul_flights_per_year: int = Field(0, ge=0, le=_MAX_FLIGHTS)
    long_haul_flights_per_year: int = Field(0, ge=0, le=_MAX_FLIGHTS)


class HomeInput(BaseModel):
    """Monthly household energy consumption, shared across household members."""

    electricity_kwh_per_month: float = Field(0, ge=0, le=_MAX_KWH_MONTH)
    natural_gas_kwh_per_month: float = Field(0, ge=0, le=_MAX_KWH_MONTH)
    household_size: int = Field(1, ge=1, le=50)


class ConsumptionInput(BaseModel):
    """Consumer goods spending and landfill waste generation."""

    goods_spend_usd_per_month: float = Field(0, ge=0, le=_MAX_USD_MONTH)
    waste_kg_per_week: float = Field(0, ge=0, le=_MAX_WASTE_WEEK)


class CarbonInput(BaseModel):
    """Complete set of lifestyle inputs for a footprint estimate."""

    transport: TransportInput = Field(default_factory=TransportInput)
    home: HomeInput = Field(default_factory=HomeInput)
    diet: DietType = DietType.MEDIUM_MEAT
    consumption: ConsumptionInput = Field(default_factory=ConsumptionInput)


class Comparison(BaseModel):
    """Contextualises the user's total against reference benchmarks."""

    global_average_annual_kg: float
    sustainable_target_annual_kg: float
    ratio_to_global_average: float
    ratio_to_sustainable_target: float


class FootprintResult(BaseModel):
    """Per-category annual emission breakdown (kg CO2e), totals, and context."""

    breakdown_kg: dict[str, float]
    total_annual_kg: float
    total_annual_tonnes: float
    comparison: Comparison


# ── Insights ──────────────────────────────────────────────────────────
class Recommendation(BaseModel):
    """A single concrete reduction action with an estimated annual saving."""

    category: str
    action: str
    estimated_annual_savings_kg: float


class InsightsResponse(BaseModel):
    """Personalized advice: a summary plus ranked reduction recommendations."""

    summary: str
    recommendations: list[Recommendation]
    source: Literal["gemini", "rules", "cache"]


# ── Entries (tracking history) ────────────────────────────────────────
class EntryCreate(BaseModel):
    """Request body for saving a footprint snapshot to an anonymous device."""

    device_id: str = Field(min_length=8, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")
    input: CarbonInput
    result: FootprintResult


class Entry(EntryCreate):
    """A persisted footprint snapshot, as returned by the API."""

    id: str
    created_at: str  # ISO-8601 UTC
