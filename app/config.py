"""
Configuration file for Energy Dashboard
This contains all the business rules, rates, and constants
"""

# === ENERGY RATES ===
# How much you pay/save per kWh
GRID_RATE = 0.15  # £/kWh - Cost to buy electricity from grid
EXPORT_RATE = 0.15  # £/kWh - Money earned selling back to grid

# === ENVIRONMENTAL FACTORS ===
# How much CO2 is offset per kWh of solar energy
CO2_OFFSET_FACTOR = 0.7  # kg CO2 per kWh
# Note: This means every kWh of solar saves ~0.7kg of CO2 emissions

# === SOLAR PANEL SPECS ===
MAX_SOLAR_CAPACITY = 10  # kW - Maximum solar panel output
# Solar production varies by time of day (we'll simulate this)

# === EV CHARGING ===
EV_BATTERY_SIZE = 60  # kWh - Total battery capacity
EV_CHARGING_POWER = 7.2  # kW - Charging rate
# Calculation: Time to charge = Battery Size / Charging Power

# === HOUSEHOLD CONSUMPTION ===
# Average consumption varies by time and usage
BASE_CONSUMPTION = 0.5  # kW - Minimum always-on consumption
PEAK_CONSUMPTION = 3.0  # kW - Maximum during peak usage

# === TIME WINDOWS ===
# When are peak energy usage times?
PEAK_HOURS_START = 18  # 6 PM
PEAK_HOURS_END = 22    # 10 PM

# === COST SAVINGS CARD ===
# Your cost savings card shows: Grid Rate × Grid Import - Export
# But we simplify: (Solar Production × Grid Rate) = Money NOT spent on grid
# This is the "Cost Savings" metric

# === DATA GENERATION ===
HISTORICAL_DAYS = 30  # How many days of historical data to generate
