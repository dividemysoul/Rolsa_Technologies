from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, StringField, PasswordField, BooleanField, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Please use a different email address.')

class EnergyUseForm(FlaskForm):
    grid_import_kwh = FloatField('Grid Import (kWh)', validators=[DataRequired()])
    solar_generation_kwh = FloatField('Solar Generation (kWh)', validators=[DataRequired()])
    grid_export_kwh = FloatField('Grid Export (kWh)', validators=[DataRequired()])
    ev_energy_kwh = FloatField('EV Energy (kWh)', validators=[DataRequired()])
    odometer_reading_km = FloatField('Odometer Reading (km)', validators=[DataRequired()])
    submit = SubmitField('Calculate')

class BookingForm(FlaskForm):
    booking_type = SelectField('Consultation Type', choices=[
        ('Solar Panels', 'Solar Panels'),
        ('EV Charger', 'EV Charger'),
        ('Smart Home', 'Smart Home')
    ], validators=[DataRequired()])
    booking_date = DateField('Preferred Date', format='%Y-%m-%d', validators=[DataRequired()], render_kw={"type": "date"})
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Book Now')

from wtforms import SelectField, IntegerField, StringField, SelectMultipleField, widgets

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class CarbonFootprintForm(FlaskForm):
    # Food
    diet = SelectField('How would you best describe your diet?', choices=[
        ('Meat in every meal', 'Meat in every meal'),
        ('Meat in some meals', 'Meat in some meals'),
        ('No beef', 'No beef'),
        ('Meat very rarely', 'Meat very rarely'),
        ('Vegetarian', 'Vegetarian'),
        ('Vegan', 'Vegan')
    ], validators=[DataRequired()])
    
    food_spend = SelectField('In a week, how much do you spend on food from restaurants, canteens and takeaways?', choices=[
        ('£0', '£0'),
        ('£1 - £10', '£1 - £10'),
        ('£10 - £40', '£10 - £40'),
        ('More than £40', 'More than £40')
    ], validators=[DataRequired()])

    food_waste = SelectField('Of the food you buy how much is wasted and thrown away?', choices=[
        ('None', 'None'),
        ('0% - 10%', '0% - 10%'),
        ('10% - 30%', '10% - 30%'),
        ('More than 30%', 'More than 30%')
    ], validators=[DataRequired()])
    
    local_food = SelectField('How often do you buy locally produced food that is not imported to the UK?', choices=[
        ('A lot of the food I buy is locally sourced', 'A lot of the food I buy is locally sourced'),
        ('Some of the food I buy is locally sourced', 'Some of the food I buy is locally sourced'),
        ('I don\'t worry about where my food comes from', 'I don\'t worry about where my food comes from')
    ], validators=[DataRequired()])

    # Travel
    travel_mode = SelectField('What kind of vehicle do you travel in most often as driver or passenger? (if any)', choices=[
        ('Car', 'Car'),
        ('Motorbike', 'Motorbike'),
        ('Neither - I walk, cycle or use public transport for all my journeys', 'Neither - I walk, cycle or use public transport for all my journeys')
    ], validators=[DataRequired()])
    
    vehicle_type = SelectField('Which of these best describes the vehicle you use most?', choices=[
        ('Electric car', 'Electric car'),
        ('Plug-in hybrid car', 'Plug-in hybrid car'),
        ('Hybrid car', 'Hybrid car'),
        ('Small petrol or diesel car', 'Small petrol or diesel car'),
        ('Medium petrol or diesel car', 'Medium petrol or diesel car'),
        ('Large petrol or diesel car', 'Large petrol or diesel car')
    ], validators=[]) # Optional depending on previous answer

    car_hours = SelectField('How many hours a week do you spend in your car or on your motorbike for personal use including commuting?', choices=[
        ('Under 2 hours', 'Under 2 hours'),
        ('2 to 5 hours', '2 to 5 hours'),
        ('5 to 15 hours', '5 to 15 hours'),
        ('15 to 25 hours', '15 to 25 hours'),
        ('Over 25 hours', 'Over 25 hours')
    ], validators=[])

    train_hours = SelectField('How many hours a week do you spend on the train for personal use including commuting?', choices=[
        ('I don\'t travel by train', 'I don\'t travel by train'),
        ('Under 2 hours', 'Under 2 hours'),
        ('2 to 5 hours', '2 to 5 hours'),
        ('5 to 15 hours', '5 to 15 hours'),
        ('15 to 25 hours', '15 to 25 hours'),
        ('Over 25 hours', 'Over 25 hours')
    ], validators=[DataRequired()])

    bus_hours = SelectField('How many hours a week do you spend on the bus for personal use including commuting?', choices=[
        ('I don\'t travel by bus', 'I don\'t travel by bus'),
        ('Under 1 hour', 'Under 1 hour'),
        ('1 to 3 hours', '1 to 3 hours'),
        ('3 to 6 hours', '3 to 6 hours'),
        ('6 to 10 hours', '6 to 10 hours'),
        ('Over 10 hours', 'Over 10 hours')
    ], validators=[DataRequired()])

    flight_domestic = IntegerField('Domestic (UK / Ireland) return flights', validators=[])
    flight_europe = IntegerField('To/from Europe return flights', validators=[])
    flight_outside_europe = IntegerField('To/from outside Europe return flights', validators=[])
    
    flight_offset = SelectField('What percentage of your flights do you offset?', choices=[
        ('None of them', 'None of them'),
        ('25%', '25%'),
        ('50%', '50%'),
        ('75%', '75%'),
        ('All of them', 'All of them'),
        ('Not applicable', 'Not applicable')
    ], validators=[DataRequired()])

    # Home
    house_type = SelectField('What kind of house do you live in?', choices=[
        ('Detached', 'Detached'),
        ('Semi-detached', 'Semi-detached'),
        ('Terrace', 'Terrace'),
        ('Flat', 'Flat')
    ], validators=[DataRequired()])

    bedrooms = SelectField('How many bedrooms does your house have?', choices=[
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4 or more', '4 or more')
    ], validators=[DataRequired()])

    occupants = SelectField('How many people (aged 17 and over) live in your house?', choices=[
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5 or more', '5 or more')
    ], validators=[DataRequired()])

    heating_type = SelectField('How do you heat your home?', choices=[
        ('Gas', 'Gas'),
        ('Oil', 'Oil'),
        ('Electricity', 'Electricity'),
        ('Wood', 'Wood'),
        ('Heatpump', 'Heatpump')
    ], validators=[DataRequired()])

    green_tariff = SelectField('Is your electricity on a green tariff?', choices=[
        ('I don\'t know', 'I don\'t know'),
        ('No', 'No'),
        ('Yes but the tariff is less than 100% renewables', 'Yes but the tariff is less than 100% renewables'),
        ('Yes 100%', 'Yes 100%')
    ], validators=[DataRequired()])

    regular_turn_off = SelectField('Do you regularly turn off lights and not leave your appliances on standby?', choices=[
        ('Yes', 'Yes'),
        ('No', 'No')
    ], validators=[DataRequired()])

    winter_temp = SelectField('How warm do you keep your home in winter?', choices=[
        ('below 14°C', 'below 14°C'),
        ('14° - 17°C', '14° - 17°C'),
        ('18° - 21°C', '18° - 21°C'),
        ('Over 21°C', 'Over 21°C')
    ], validators=[DataRequired()])

    efficiency_improvements = MultiCheckboxField('Which of these home energy efficiency improvements are installed in your home?', choices=[
        ('Energy saving lightbulbs', 'Energy saving lightbulbs'),
        ('Loft insulation', 'Loft insulation'),
        ('Cavity or solid wall insulation', 'Cavity or solid wall insulation'),
        ('Condensing boiler', 'Condensing boiler'),
        ('Double glazing', 'Double glazing'),
        ('Low flow fittings to taps and showers', 'Low flow fittings to taps and showers'),
        ('Solar panels', 'Solar panels'),
        ('Solar water heater', 'Solar water heater')
    ])

    # Stuff
    new_household_items = MultiCheckboxField('In the last 12 months, have you bought any of these new household items?', choices=[
        ('TV, laptop or PC', 'TV, laptop or PC'),
        ('Large item of furniture', 'Large item of furniture'),
        ('Washing machine, dishwasher, tumble dryer or fridge freezer', 'Washing machine, dishwasher, tumble dryer or fridge freezer'),
        ('Mobile phone or tablet', 'Mobile phone or tablet')
    ])

    clothes_spend = SelectField('In a typical month, how much do you spend on clothes and footwear?', choices=[
        ('£0', '£0'),
        ('£1 - £40', '£1 - £40'),
        ('£40 - £100', '£40 - £100'),
        ('£100+', '£100+')
    ], validators=[DataRequired()])

    pet_spend = SelectField('In a typical month, how much do you spend on your pets and pet food?', choices=[
        ('I don\'t have a pet', 'I don\'t have a pet'),
        ('£1 - £10', '£1 - £10'),
        ('£10 - £35', '£10 - £35'),
        ('£35+', '£35+')
    ], validators=[DataRequired()])

    health_spend = SelectField('In a typical month, how much do you spend on health, beauty and grooming products?', choices=[
        ('£0 - £10', '£0 - £10'),
        ('£10 - £60', '£10 - £60'),
        ('£60+', '£60+')
    ], validators=[DataRequired()])

    contract_spend = SelectField('In a typical month, how much do you spend on phone, internet and TV contracts?', choices=[
        ('£0', '£0'),
        ('£1 - £35', '£1 - £35'),
        ('£35 - £70', '£35 - £70'),
        ('£70+', '£70+')
    ], validators=[DataRequired()])

    entertainment_spend = SelectField('In a typical month, how much do you spend on entertainment and hobbies?', choices=[
        ('£0 - £25', '£0 - £25'),
        ('£25 - £50', '£25 - £50'),
        ('£50 - £75', '£50 - £75'),
        ('£75+', '£75+')
    ], validators=[DataRequired()])

    recycling = MultiCheckboxField('Which of these types of waste do you recycle and/or compost?', choices=[
        ('Food', 'Food'),
        ('Paper', 'Paper'),
        ('Tin cans', 'Tin cans'),
        ('Plastic', 'Plastic'),
        ('Glass', 'Glass')
    ])

    # Personal
    location = SelectField('Where are you based?', choices=[
        ('I\'m in the UK', 'I\'m in the UK'),
        ('I\'m based outside of the UK', 'I\'m based outside of the UK')
    ], validators=[DataRequired()])

    postcode = StringField('First half of your postcode (e.g. SW1A)')

    age = SelectField('How old are you?', choices=[
        ('Under 13', 'Under 13'),
        ('13-17', '13-17'),
        ('18+', '18+')
    ], validators=[DataRequired()])

    submit_footprint = SubmitField('Calculate Footprint')