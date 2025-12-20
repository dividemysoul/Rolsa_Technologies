# Energy use algorithm

GRID_EMISSION_FACTOR = 0.14
ELECTRICITY_UNIT_RATE = 0.28

class EnergyUse:
    def __init__(self, grid_import_kwh, solar_generation_kwh, grid_export_kwh, ev_energy_kwh, odometer_reading_km):
        self.grid_import_kwh = grid_import_kwh
        self.solar_generation_kwh = solar_generation_kwh
        self.grid_export_kwh = grid_export_kwh
        self.ev_energy_kwh = ev_energy_kwh
        self.odometer_reading_km = odometer_reading_km

    def total_consumption(self):
        return self.grid_import_kwh + (self.solar_generation_kwh - self.grid_export_kwh)

    def home_consumption(self):
        return self.total_consumption() - self.ev_energy_kwh

    def ev_share(self):
        return (self.ev_energy_kwh / self.total_consumption()) * 100

    def self_consumption(self):
        return (self.solar_generation_kwh - self.grid_export_kwh) / self.solar_generation_kwh * 100

    def solar_coverage(self):
        return (self.solar_generation_kwh / self.total_consumption()) * 100

    def ev_efficiency(self):
        return (self.ev_energy_kwh * 1000) / self.odometer_reading_km

    def co2_saved(self):
        return self.solar_generation_kwh * GRID_EMISSION_FACTOR

    def cost_savings(self):
        return self.solar_generation_kwh * ELECTRICITY_UNIT_RATE

    def gather_data(self):
        return {

            "grid_import_kwh": self.grid_import_kwh,
            "solar_generation_kwh": self.solar_generation_kwh,
            "grid_export_kwh": self.grid_export_kwh,
            "ev_energy_kwh": self.ev_energy_kwh,
            "odometer_reading_km": self.odometer_reading_km,
            "total_consumption": round(self.total_consumption(), 2),
            "home_consumption": round(self.home_consumption(), 2),
            "ev_share": round(self.ev_share(), 2),
            "self_consumption": round(self.self_consumption(), 2),
            "solar_coverage": round(self.solar_coverage(), 2),
            "ev_efficiency": round(self.ev_efficiency(), 2),
            "co2_saved": round(self.co2_saved(), 2),
            "cost_savings": round(self.cost_savings(), 2)
        }

if __name__ == "__main__":

    # Create an instance of your class with that data
    energy_tester = EnergyUse(650.4, 120.5, 5.2, 280.5, 45000)

    # Use the gather_data method and print the result
    results = energy_tester.gather_data()
    print("\n--- Energy Use Results ---")
    for key, value in results.items():
        print(f"{key}: {value}")