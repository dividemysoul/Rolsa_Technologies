from flask import render_template, request
from app import app
from app.forms import EnergyUseForm

from app.services.energy_use import EnergyUse

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/energy-use', methods=['GET', 'POST'])
def energy_use():
    form = EnergyUseForm()
    if form.validate_on_submit():
        energy_calc = EnergyUse(
            grid_import_kwh=form.grid_import_kwh.data,
            solar_generation_kwh=form.solar_generation_kwh.data,
            grid_export_kwh=form.grid_export_kwh.data,
            ev_energy_kwh=form.ev_energy_kwh.data,
            odometer_reading_km=form.odometer_reading_km.data
        )
        submitted_data = energy_calc.gather_data()
        return render_template('energy-use.html', form=form, submitted_data=submitted_data)
    return render_template('energy-use.html', form=form)

from app.forms import CarbonFootprintForm

from app.services.carbon_footprint import CarbonFootprintCalculator

@app.route('/carbon-footprint', methods=['GET', 'POST'])
def carbon_footprint():
    form = CarbonFootprintForm()
    if form.validate_on_submit():
        # Prepare data for calculator
        data = {
            "food": {
                "diet_type": form.diet.data,
                "eating_out_spend_per_week": form.food_spend.data,
                "waste_percentage": form.food_waste.data,
                "local_sourcing": form.local_food.data
            },
            "travel": {
                "general_vehicle": form.travel_mode.data,
                "specific_vehicle": form.vehicle_type.data,
                "car_hours_per_week": form.car_hours.data,
                "train_hours_per_week": form.train_hours.data,
                "bus_hours_per_week": form.bus_hours.data,
                "flights": {
                    "domestic": form.flight_domestic.data or 0,
                    "europe": form.flight_europe.data or 0,
                    "long_haul": form.flight_outside_europe.data or 0
                },
                "flight_offset_percentage": form.flight_offset.data
            },
            "home": {
                "house_type": form.house_type.data,
                "bedrooms": form.bedrooms.data,
                "people_count": form.occupants.data,
                "heating_source": form.heating_type.data,
                "green_tariff": form.green_tariff.data,
                "lights_off": form.regular_turn_off.data,
                "winter_temp": form.winter_temp.data,
                "improvements": form.efficiency_improvements.data
            },
            "stuff": {
                "purchases": form.new_household_items.data,
                "clothes_spend": form.clothes_spend.data,
                "pet_spend": form.pet_spend.data,
                "beauty_spend": form.health_spend.data,
                "contracts_spend": form.contract_spend.data,
                "hobbies_spend": form.entertainment_spend.data,
                "recycling": form.recycling.data
            }
        }

        # Calculate
        calculator = CarbonFootprintCalculator(data)
        footprint_results = calculator.calculate()

        submitted_data = form.data
        if 'Neither' in submitted_data.get('travel_mode', ''):
            submitted_data.pop('vehicle_type', None)
            submitted_data.pop('car_hours', None)
        submitted_data.pop('csrf_token', None)
        submitted_data.pop('submit_footprint', None)
        
        return render_template('carbon_footprint.html', form=form, submitted_data=submitted_data, footprint_results=footprint_results)
    return render_template('carbon_footprint.html', form=form)