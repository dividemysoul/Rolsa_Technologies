"""
Data Models for Energy Dashboard
These define the structure of our data
"""

from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict

@dataclass
class EnergyReading:
    """
    A single energy reading at a point in time
    Think of this like a row in a database table
    """
    timestamp: datetime  # When was this reading taken?
    solar_production: float  # kW - How much solar energy being produced
    consumption: float  # kW - How much energy being consumed
    grid_import: float  # kW - Energy bought from grid (when solar isn't enough)
    grid_export: float  # kW - Energy sold back to grid (when solar excess)
    
    def to_dict(self):
        """Convert to dictionary for JSON responses"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'solar_production': round(self.solar_production, 2),
            'consumption': round(self.consumption, 2),
            'grid_import': round(self.grid_import, 2),
            'grid_export': round(self.grid_export, 2),
        }


@dataclass
class DashboardMetrics:
    """
    The main metrics shown on the dashboard cards
    These are calculated from EnergyReadings
    """
    total_consumption: float  # kWh - Total energy used
    solar_production: float  # kWh - Total solar generated
    cost_savings: float  # £ - Money saved by using solar
    co2_offset: float  # kg - CO2 emissions prevented
    grid_import: float  # kWh - Energy bought from grid
    grid_export: float  # kWh - Energy sold back
    
    def to_dict(self):
        """Convert to dictionary for JSON"""
        return asdict(self)


@dataclass
class ConsumptionBreakdown:
    """
    Breakdown of energy consumption by category
    These percentages should add up to 100%
    """
    ev_charging: float  # % - Percentage used for EV
    hvac: float  # % - Heating/Cooling
    appliances: float  # % - Kitchen appliances, etc.
    lighting: float  # % - Lights
    
    def to_dict(self):
        """Convert to dictionary for JSON"""
        return asdict(self)
    
    def validate(self):
        """Ensure percentages add up to 100%"""
        total = self.ev_charging + self.hvac + self.appliances + self.lighting
        if not (99 <= total <= 101):  # Allow small rounding errors
            raise ValueError(f"Percentages must add up to 100%, got {total}%")


@dataclass
class EVChargingStatus:
    """
    Electric Vehicle charging information
    """
    current_charge_level: float  # kWh - Current battery level
    target_charge: float  # kWh - Target battery level
    charging_power: float  # kW - Current charging rate
    time_to_complete: float  # hours - Time to reach target
    cost_estimate: float  # £ - Estimated cost to full charge
    
    def to_dict(self):
        """Convert to dictionary for JSON"""
        return asdict(self)
    
    def get_percentage(self) -> int:
        """Calculate charge level as percentage"""
        from config import EV_BATTERY_SIZE
        return int((self.current_charge_level / EV_BATTERY_SIZE) * 100)
