"""
Energy track and use, still in testing
"""

def calculate_energy_use(grid_import_kwh, solar_generation_kwh, grid_export_kwh, ev_energy_kwh, odometer_reading_km):
    true_consumption_kwh = grid_import_kwh + (solar_generation_kwh - grid_export_kwh)
    home_usage = true_consumption_kwh - ev_energy_kwh
    ev_share = (ev_energy_kwh / true_consumption_kwh) * 100
    self_consumption = (solar_generation_kwh - grid_export_kwh) / solar_generation_kwh * 100
    solar_coverage = (solar_generation_kwh / true_consumption_kwh) * 100
    ev_efficiency = (ev_energy_kwh * 1000) / odometer_reading_km

    output = f'True consumption: {round(true_consumption_kwh, 2)} kWh\n' + \
             f'Home usage: {round(home_usage, 2)} kWh\n' + \
             f'EV share: {round(ev_share, 2)}%\n' + \
             f'Self consumption: {round(self_consumption, 2)}%\n' + \
             f'Solar coverage: {round(solar_coverage, 2)}%\n' + \
             f'EV efficiency: {round(ev_efficiency, 2)} kWh/km\n'

    return output

if __name__ == '__main__':
    print(calculate_energy_use(650.4, 120.5, 5.2, 280.5, 45000))