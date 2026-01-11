from flask import render_template, request, flash, redirect, url_for, session
from app import app, db
from app.forms import EnergyUseForm, LoginForm, RegistrationForm, BookingForm, ProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Booking
from urllib.parse import urlparse
import uuid

from app.services.energy_use import EnergyUse

@app.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    form = BookingForm()
    if form.validate_on_submit():
        booking_number = str(uuid.uuid4().hex[:8].upper())
        # Determine Booking Type and Metadata based on Category
        if form.service_category.data == 'Consultation':
            # Consultation: Type is the topic, also save info
            final_type = f"Consultation - {form.booking_type.data}"
            product_installed = None
            booking_time = None
            additional_info = form.additional_info.data
        else:
            # Installation: Type is Installation, product is separate
            final_type = "Installation"
            product_installed = form.installation_product.data
            booking_time = form.booking_time.data
            additional_info = None

        booking = Booking(
            user_id=current_user.id,
            booking_type=final_type,
            booking_date=form.booking_date.data,
            booking_time=booking_time,
            product_installed=product_installed,
            additional_info=additional_info,
            address=form.address.data,
            booking_number=booking_number
        )
        db.session.add(booking)
        db.session.commit()
        # flash(f'Booking confirmed! Your booking number is {booking_number}')
        # return redirect(url_for('index'))
        return render_template('book.html', title='Book Consultation', form=form, booking_number=booking_number)
    return render_template('book.html', title='Book Consultation', form=form)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Your Profile')

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.phone_number = form.phone_number.data
        current_user.address = form.address.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.full_name.data = current_user.full_name
        form.phone_number.data = current_user.phone_number
        form.address.data = current_user.address
    return render_template('edit_profile.html', title='Edit Profile', form=form)

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
        session['energy_data'] = submitted_data
        return render_template('energy-use.html', form=form, submitted_data=submitted_data)
    return render_template('energy-use.html', form=form)

@app.route('/dashboard')
def dashboard():
    data = session.get('energy_data')
    if not data:
        flash('Please calculate your energy use first.', 'info')
        return redirect(url_for('energy_use'))
    return render_template('dashboard.html', data=data)

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