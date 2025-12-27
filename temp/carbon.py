import json

EMISSION_FACTORS = { 'food': {
        'diet': {
            'Meat in every meal': 10.2 * 365,  # Daily to yearly
            'Meat in some meals': 5.6 * 365,
            'No beef': 4.7 * 365,
            'Vegetarian': 4.2 * 365,
            'Vegan': 2.5 * 365
        },
        'restaurants': {
            'factor': 0.234,  # Per £
            'ranges': {
                '£0': 0,
                '£1 - £10': 5 * 52,
                '£10 - £40': 25 * 52,
                'More than £40': 60 * 52
            }
        },
        'food_waste': {
            'factor': 1.38,  # kg CO2e per kg of food
            'avg_person_waste_kg': 70,
            'percentages': {
                'None': 0,
                '0% - 10%': 0.05,
                '10% - 30%': 0.20,
                'More than 30%': 0.40
            }
        },
        'local_food_reduction': {
            'A lot of the food I buy is locally sourced': 0.95,  # 5% reduction
            'Some of the food I buy is locally sourced': 0.98,   # 2% reduction
            'I don\'t worry about where my food comes from': 1.0
        }
    },
    'travel': {
        'car_type': {
            'Small petrol or diesel car': 0.255,  # kg CO2e/km
            'Medium petrol or diesel car': 0.275,
            'Large petrol or diesel car': 0.315,
            'Electric car': 0.06,
            'Plug-in hybrid car': 0.18,
            'Hybrid car': 0.18
        },
        'motorbike': 0.11,  # kg CO2e/km
        'bus': 0.10,        # kg CO2e/passenger-km
        'train': 0.04,      # kg CO2e/passenger-km
        'flight_domestic': 0.27,  # kg CO2e/passenger-km
        'flight_europe': 0.16,    # kg CO2e/passenger-km
        'flight_international': 0.15 # kg CO2e/passenger-km
    },
    'home': {
        'electricity_grid_factor': 0.23,  # kg CO2e/kWh
        'heating_fuel_factors': {
            'Gas': 0.20,
            'Oil': 0.26,
            'Electricity': 0.23,
            'Wood': 0.02,
            'Heatpump': 0.07  # (0.23 / 3.5 COP)
        },
        'energy_efficiency_reductions': {
            'Loft insulation': 0.15,
            'Cavity wall insulation': 0.15,
            'Double glazing': 0.10
        },
        'temperature_adjustment': {
            'below 14°C': 0.8,
            '14-17°C': 0.9,
            '18-21°C': 1.0,
            'Over 21°C': 1.1
        },
        'avg_household_energy_consumption_kwh': {  # Sample values
            'Flat': 10000,
            'Semi-detached': 15000,
            'Detached': 20000
        }
    },
    'consumption': {
        'clothing_footwear': 0.5,  # kg CO2e/£
        'pets': 1.5,  # kg CO2e/£
        'health_beauty': 0.4,  # kg CO2e/£
        'telecom_internet': 75, # Annual estimate
        'entertainment_hobbies': 0.45, # kg CO2e/£
        'appliances': {
            'TV, laptop or PC': 135,
            'Large item of furniture': 165,
            'Washing machine, dishwasher, tumble dryer or fridge freezer': 180,
            'Mobile phone or tablet': 20
        }
    }
}

def calculate_food_footprint(answers):
    """Calculates the carbon footprint from food consumption."""
    diet_emissions = EMISSION_FACTORS['food']['diet'].get(answers.get('diet'), 0)
    
    restaurant_spend_range = answers.get('food_expenditure', '£0')
    restaurant_spend = EMISSION_FACTORS['food']['restaurants']['ranges'].get(restaurant_spend_range, 0)
    restaurant_emissions = restaurant_spend * EMISSION_FACTORS['food']['restaurants']['factor']
    
    waste_percentage = EMISSION_FACTORS['food']['food_waste']['percentages'].get(answers.get('food_waste'), 0)
    waste_emissions = waste_percentage * EMISSION_FACTORS['food']['food_waste']['avg_person_waste_kg'] * EMISSION_FACTORS['food']['food_waste']['factor']
    
    local_food_multiplier = EMISSION_FACTORS['food']['local_food_reduction'].get(answers.get('local_food'), 1.0)

    total_food_emissions = (diet_emissions + restaurant_emissions + waste_emissions) * local_food_multiplier
    return total_food_emissions

def calculate_travel_footprint(answers):
    """Calculates the carbon footprint from travel."""
    total_travel_emissions = 0
    
    # Car
    car_hours = answers.get('car_hours', 0)
    car_type = answers.get('car_type')
    if car_type and car_hours > 0:
        avg_speed_kph = 40  # Assume average speed of 40 km/h
        distance_km = car_hours * 52 * avg_speed_kph
        car_factor = EMISSION_FACTORS['travel']['car_type'].get(car_type, 0)
        total_travel_emissions += distance_km * car_factor
        
    # Motorbike
    motorbike_hours = answers.get('motorbike_hours', 0)
    if motorbike_hours > 0:
        avg_speed_kph = 40
        distance_km = motorbike_hours * 52 * avg_speed_kph
        total_travel_emissions += distance_km * EMISSION_FACTORS['travel']['motorbike']

    # Public Transport
    bus_hours = answers.get('bus_hours', 0)
    train_hours = answers.get('train_hours', 0)
    
    bus_distance = bus_hours * 52 * 20  # Assume average speed of 20 km/h
    train_distance = train_hours * 52 * 60 # Assume average speed of 60 km/h
    
    total_travel_emissions += bus_distance * EMISSION_FACTORS['travel']['bus']
    total_travel_emissions += train_distance * EMISSION_FACTORS['travel']['train']

    # Flights
    # Simplified: Assuming average distances
    # Domestic: 500 km, Europe: 1500 km, International: 7000 km (one-way)
    total_flight_emissions = 0
    total_flight_emissions += answers.get('flights_domestic', 0) * 500 * 2 * EMISSION_FACTORS['travel']['flight_domestic']
    total_flight_emissions += answers.get('flights_europe', 0) * 1500 * 2 * EMISSION_FACTORS['travel']['flight_europe']
    total_flight_emissions += answers.get('flights_international', 0) * 7000 * 2 * EMISSION_FACTORS['travel']['flight_international']
    
    offset_percentage = answers.get('flight_offset_percentage', 0) / 100.0
    total_travel_emissions += total_flight_emissions * (1 - offset_percentage)

    return total_travel_emissions

def calculate_home_footprint(answers):
    """Calculates the carbon footprint from home energy usage."""
    # A more detailed model would need actual energy bills. 
    # This is a simplified estimation.
    
    # Base electricity consumption (e.g., from appliances, lighting)
    # A simple assumption: 3000 kWh per year for a 1-person household.
    num_people = answers.get('household_size', 1)
    base_electricity_consumption = (1500 + (num_people * 500))  # A rough estimate
    
    # Heating
    heating_fuel = answers.get('heating_fuel', 'Gas')
    heating_factor = EMISSION_FACTORS['home']['heating_fuel_factors'][heating_fuel]
    # Assume heating is a major part of energy use, e.g., 12000 kWh for a medium house
    heating_consumption = 12000 
    
    # Adjust for home size
    home_type = answers.get('home_type', 'Semi-detached') # e.g., 'Apartment', 'Semi-detached', 'Detached'
    if home_type == 'Apartment':
        heating_consumption *= 0.7
    elif home_type == 'Detached':
        heating_consumption *= 1.5

    # Adjust for thermostat settings
    temp_factor = EMISSION_FACTORS['home']['temperature_adjustment'].get(answers.get('thermostat_setting', '18-21°C'), 1.0)
    heating_consumption *= temp_factor
    
    # Apply insulation benefits
    insulation_reduction = 0
    if 'Loft insulation' in answers.get('home_improvements', []):
        insulation_reduction += 0.15
    if 'Cavity wall insulation' in answers.get('home_improvements', []):
        insulation_reduction += 0.15
    if 'Double glazing' in answers.get('home_improvements', []):
        insulation_reduction += 0.10
        
    heating_emissions = heating_consumption * (1 - insulation_reduction) * heating_factor
    
    # Electricity for non-heating appliances
    electricity_factor = EMISSION_FACTORS['home']['electricity_grid_factor']
    if answers.get('green_tariff') == 'Yes 100%':
        electricity_factor = 0
    
    # Standby reduction
    standby_reduction = 1.0
    if answers.get('standby_habits') == 'Yes':
        standby_reduction = 0.95
        
    electricity_emissions = base_electricity_consumption * electricity_factor * standby_reduction
    
    total_home_emissions = (heating_emissions + electricity_emissions) / num_people # Per person
    
    return total_home_emissions

def calculate_goods_and_services_footprint(answers):
    """Calculates the carbon footprint from consumption of goods and services."""
    total_consumption_emissions = 0

    # Monthly spending converted to yearly
    total_consumption_emissions += answers.get('clothing_spend_monthly', 0) * 12 * EMISSION_FACTORS['consumption']['clothing_footwear']
    total_consumption_emissions += answers.get('pets_spend_monthly', 0) * 12 * EMISSION_FACTORS['consumption']['pets']
    total_consumption_emissions += answers.get('health_beauty_spend_monthly', 0) * 12 * EMISSION_FACTORS['consumption']['health_beauty']
    total_consumption_emissions += answers.get('entertainment_spend_monthly', 0) * 12 * EMISSION_FACTORS['consumption']['entertainment_hobbies']
    
    # One-off purchases (annualized)
    for item in answers.get('new_purchases', []):
        total_consumption_emissions += EMISSION_FACTORS['consumption']['appliances'].get(item, 0)

    # Telecom and Internet
    total_consumption_emissions += EMISSION_FACTORS['consumption']['telecom_internet']

    return total_consumption_emissions


def calculate_total_footprint(answers):
    """
    Calculates the total carbon footprint based on a dictionary of answers.
    """
    food_fp = calculate_food_footprint(answers)
    travel_fp = calculate_travel_footprint(answers)
    home_fp = calculate_home_footprint(answers)
    goods_fp = calculate_goods_and_services_footprint(answers)
    
    total_footprint = food_fp + travel_fp + home_fp + goods_fp
    
    return {
        'food': food_fp,
        'travel': travel_fp,
        'home': home_fp,
        'goods_and_services': goods_fp,
        'total': total_footprint
    }

if __name__ == '__main__':
    # Example usage with sample answers
    example_answers = {
        # Food
        'diet': 'Meat in some meals',
        'food_expenditure': '£10 - £40',
        'food_waste': '10% - 30%',
        'local_food': 'Some of the food I buy is locally sourced',

        # Travel
        'car_type': 'Medium petrol or diesel car',
        'car_hours': 5, # hours per week
        'bus_hours': 2,
        'train_hours': 1,
        'flights_domestic': 1,
        'flights_europe': 1,
        'flights_international': 0,
        'flight_offset_percentage': 0,

        # Home
        'home_type': 'Semi-detached',
        'household_size': 2,
        'heating_fuel': 'Gas',
        'green_tariff': 'No',
        'standby_habits': 'Yes',
        'thermostat_setting': '18-21°C',
        'home_improvements': ['Double glazing'],
        
        # Goods and Services
        'new_purchases': ['TV, laptop or PC'],
        'clothing_spend_monthly': 50,
        'pets_spend_monthly': 20,
        'health_beauty_spend_monthly': 30,
        'entertainment_spend_monthly': 40,
    }
    
    footprint = calculate_total_footprint(example_answers)
    
    print("--- Carbon Footprint Report ---")
    for category, value in footprint.items():
        print(f"{category.replace('_', ' ').title()}: {value:.2f} kg CO2e/year")
    print("---------------------------------")
    print(f"Total Annual Footprint: {footprint['total']:.2f} kg CO2e/year")
    
    # Convert to tonnes for better readability
    total_tonnes = footprint['total'] / 1000
    print(f"Which is equivalent to {total_tonnes:.2f} tonnes of CO2e per year.")
