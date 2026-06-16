"""Pure carbon footprint calculation engine.

Stateless, deterministic, side-effect-free functions that compute an annual
carbon footprint from lifestyle inputs. The same inputs always produce the
same output — no I/O, no database, no network calls — making the engine
trivially testable and suitable for real-time API use.

All intermediate quantities are normalised to **annual kg CO2e** before
aggregation into the final breakdown.
"""

from __future__ import annotations

from app.carbon import factors
from app.models import (
    CarbonInput,
    Comparison,
    ConsumptionInput,
    FootprintResult,
    HomeInput,
    TransportInput,
)


def _transport_annual_kg(t: TransportInput) -> float:
    """Compute annual transport emissions from car, transit and flights."""
    car = t.car_km_per_week * factors.WEEKS_PER_YEAR * factors.CAR_FACTORS_PER_KM[t.car_fuel]
    transit = t.public_transit_km_per_week * factors.WEEKS_PER_YEAR * factors.PUBLIC_TRANSIT_PER_KM
    flights = (
        t.short_haul_flights_per_year
        * factors.SHORT_HAUL_TRIP_KM
        * factors.FLIGHT_SHORT_HAUL_PER_KM
        + t.long_haul_flights_per_year * factors.LONG_HAUL_TRIP_KM * factors.FLIGHT_LONG_HAUL_PER_KM
    )
    return car + transit + flights


def _home_annual_kg(h: HomeInput) -> float:
    """Compute annual home energy emissions, split across household members."""
    electricity = (
        h.electricity_kwh_per_month * factors.MONTHS_PER_YEAR * factors.ELECTRICITY_PER_KWH
    )
    gas = h.natural_gas_kwh_per_month * factors.MONTHS_PER_YEAR * factors.NATURAL_GAS_PER_KWH
    # Energy is a shared resource — attribute a per-person portion.
    return (electricity + gas) / h.household_size


def _consumption_annual_kg(c: ConsumptionInput) -> float:
    """Compute annual goods and waste emissions."""
    goods = c.goods_spend_usd_per_month * factors.MONTHS_PER_YEAR * factors.GOODS_PER_USD_MONTHLY
    waste = c.waste_kg_per_week * factors.WEEKS_PER_YEAR * factors.WASTE_PER_KG
    return goods + waste


def calculate_footprint(data: CarbonInput) -> FootprintResult:
    """Compute the annual carbon footprint breakdown for a set of lifestyle inputs."""
    breakdown = {
        "transport": round(_transport_annual_kg(data.transport), 2),
        "home": round(_home_annual_kg(data.home), 2),
        "diet": round(factors.DIET_ANNUAL_KG[data.diet], 2),
        "consumption": round(_consumption_annual_kg(data.consumption), 2),
    }
    total = round(sum(breakdown.values()), 2)

    comparison = Comparison(
        global_average_annual_kg=factors.GLOBAL_AVG_ANNUAL_KG,
        sustainable_target_annual_kg=factors.SUSTAINABLE_TARGET_ANNUAL_KG,
        ratio_to_global_average=round(total / factors.GLOBAL_AVG_ANNUAL_KG, 3),
        ratio_to_sustainable_target=round(total / factors.SUSTAINABLE_TARGET_ANNUAL_KG, 3),
    )

    return FootprintResult(
        breakdown_kg=breakdown,
        total_annual_kg=total,
        total_annual_tonnes=round(total / 1000, 3),
        comparison=comparison,
    )
