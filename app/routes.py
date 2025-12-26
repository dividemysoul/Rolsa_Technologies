from flask import render_template, request
from app import app
from app.forms import EnergyUseForm

from app.services.energy_use import EnergyUse

@app.route('/')
def index():
    return 'Home'

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
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
        return render_template('calculate.html', form=form, submitted_data=submitted_data)
    return render_template('calculate.html', form=form)