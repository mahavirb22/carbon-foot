"""Emission factors for estimating personal carbon footprints.

Every constant is documented with its source so the numbers are transparent
and auditable rather than opaque magic values. All factors are expressed in
**kilograms of CO2-equivalent (kg CO2e)** and represent rounded averages
suitable for awareness and education — not certified carbon accounting.

Sources referenced throughout:
  * UK DEFRA / DESNZ 2023 Greenhouse Gas Conversion Factors
    https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2023
  * US EPA — Greenhouse Gas Emissions from a Typical Passenger Vehicle
    https://www.epa.gov/greenvehicles
  * IPCC AR6 and Our World in Data — food & energy emission intensities
    https://ourworldindata.org/food-choice-vs-eating-local

The platform reports estimates in metric kg / tonnes CO2e per year.
"""

from __future__ import annotations

from enum import Enum

# ─────────────────────── Time conversion constants ──────────────────────
# Used to annualise weekly and monthly user inputs.
WEEKS_PER_YEAR: int = 52
MONTHS_PER_YEAR: int = 12

# ──────────────────────────── Transport ─────────────────────────────────
# Per-kilometre factors for different personal travel modes.


class CarFuel(str, Enum):
    """Car drivetrain type, determining the per-km CO2e emission factor."""

    PETROL = "petrol"
    DIESEL = "diesel"
    HYBRID = "hybrid"
    ELECTRIC = "electric"


# kg CO2e per km driven (single occupant, average vehicle). Source: DEFRA 2023.
CAR_FACTORS_PER_KM: dict[CarFuel, float] = {
    CarFuel.PETROL: 0.170,
    CarFuel.DIESEL: 0.171,
    CarFuel.HYBRID: 0.120,
    CarFuel.ELECTRIC: 0.047,  # accounts for grid-average generation emissions
}

# kg CO2e per passenger-km on public transport. Source: DEFRA 2023 bus/rail avg.
PUBLIC_TRANSIT_PER_KM: float = 0.060

# kg CO2e per passenger-km for aviation (includes radiative forcing uplift).
# Short-haul flights are more carbon-intensive per km. Source: DEFRA 2023.
FLIGHT_SHORT_HAUL_PER_KM: float = 0.158
FLIGHT_LONG_HAUL_PER_KM: float = 0.150
# Representative one-way distances to convert flight counts into km flown.
SHORT_HAUL_TRIP_KM: float = 1100.0
LONG_HAUL_TRIP_KM: float = 6500.0

# ──────────────────────────── Home energy ───────────────────────────────
# kg CO2e per kWh of grid electricity (approximate world average).
# Source: IEA / Our World in Data, ~2022 global generation mix.
ELECTRICITY_PER_KWH: float = 0.450
# kg CO2e per kWh of natural gas (for heating). Source: DEFRA 2023.
NATURAL_GAS_PER_KWH: float = 0.183

# ──────────────────────────────── Diet ──────────────────────────────────
# Annual kg CO2e attributable to food production by diet type.
# Source: Scarborough et al. 2014 / Our World in Data dietary footprint data.


class DietType(str, Enum):
    """Dietary profile, each mapped to an annual food-production carbon footprint."""

    HEAVY_MEAT = "heavy_meat"
    MEDIUM_MEAT = "medium_meat"
    LOW_MEAT = "low_meat"
    PESCATARIAN = "pescatarian"
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"


DIET_ANNUAL_KG: dict[DietType, float] = {
    DietType.HEAVY_MEAT: 3300.0,
    DietType.MEDIUM_MEAT: 2500.0,
    DietType.LOW_MEAT: 1900.0,
    DietType.PESCATARIAN: 1700.0,
    DietType.VEGETARIAN: 1500.0,
    DietType.VEGAN: 1050.0,
}

# ───────────────────────── Goods, services & waste ──────────────────────
# kg CO2e per USD spent on consumer goods (EEIO-style spend intensity).
# Source: derived from EXIOBASE / consumer-spend emission intensity studies.
GOODS_PER_USD_MONTHLY: float = 0.40
# kg CO2e per kg of household waste sent to landfill (methane-weighted).
# Source: EPA WARM model.
WASTE_PER_KG: float = 0.580

# ──────────────────────────── Reference values ──────────────────────────
# Annual per-capita emissions for contextual comparison (in kg CO2e).
# Source: Our World in Data, 2022 consumption-based per-capita figures.
GLOBAL_AVG_ANNUAL_KG: float = 4800.0
# Paris-aligned ~2030 per-capita target.
SUSTAINABLE_TARGET_ANNUAL_KG: float = 2000.0
