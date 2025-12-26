from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired

class EnergyUseForm(FlaskForm):
    grid_import_kwh = FloatField('Grid Import (kWh)', validators=[DataRequired()])
    solar_generation_kwh = FloatField('Solar Generation (kWh)', validators=[DataRequired()])
    grid_export_kwh = FloatField('Grid Export (kWh)', validators=[DataRequired()])
    ev_energy_kwh = FloatField('EV Energy (kWh)', validators=[DataRequired()])
    odometer_reading_km = FloatField('Odometer Reading (km)', validators=[DataRequired()])
    submit = SubmitField('Calculate')
