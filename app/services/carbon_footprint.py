import json

class CarbonFootprintCalculator:

    # Emission Factors (approximations based on UK data)
    _EMISSION_FACTORS = {
        "food": {
            "diet": {
                "Meat in every meal": 12.5, # Updated from 10.2 to 12.5 reflect high ruminant impact
                "Meat in some meals": 5.6,
                "No beef": 4.7,
                "Meat very rarely": 4.5,
                "Vegetarian": 4.2,
                "Vegan": 2.5
            },
            "spend_factor": 0.234,  # kg CO2e/£ for restaurants
            "waste_landfill_factor": 1.38, # kg CO2e/kg waste
            "avg_waste_per_person": 70, # kg/year
            "local_sourcing_reduction": {
                "A lot of the food I buy is locally sourced": 0.05,
                "Some of the food I buy is locally sourced": 0.02,
                "I don't worry about where my food comes from": 0.0
            }
        },
        "travel": {
            "vehicle_per_km": {
                "Electric car": 0.06,
                "Plug-in hybrid car": 0.18,
                "Hybrid car": 0.18,
                "Small petrol or diesel car": 0.255,
                "Medium petrol or diesel car": 0.275,
                "Large petrol or diesel car": 0.315,
                "Motorbike": 0.11,
                "Bus": 0.10,
                "Train": 0.04
            },
            "speeds": {
                "Car": 35, # Updated to 35 km/h
                "Motorbike": 45, # Updated to 45 km/h
                "Bus": 20,
                "Train": 60
            },
            "flights": {
                "Domestic": {"factor": 0.27, "distance": 400},
                "Europe": {"factor": 0.16, "distance": 1500},
                "LongHaul": {"factor": 0.15, "distance": 6000}
            }
        },
        "home": {
            "heating_factor": { # kg CO2e/kWh
                "Gas": 0.20,
                "Oil": 0.26,
                "Electricity": 0.23,
                "Wood": 0.02,
                "Heatpump": 0.07
            },
            # REMOVED static baseline_heating_kwh: Replaced by dynamic bedroom logic
            "electricity_factor": 0.18, # Updated from 0.23
            # REMOVED static baseline_electricity_kwh: Replaced by dynamic bedroom logic
            "temp_adjustment": {
                "below 14°C": -0.20,
                "14° - 17°C": -0.10,
                "18° - 21°C": 0.0,
                "Over 21°C": 0.10
            },
            "improvements_reduction": { # Maps partial string matches or exact
                "Loft insulation": 0.15,
                "Cavity or solid wall insulation": 0.15,
                "Condensing boiler": 0.20,
                "Double glazing": 0.10,
                "Solar panels": 0.30
            },
            "lights_reduction": 0.05
        },
        "stuff": {
            "items_annualised": { # Map exact item string to kg CO2e/year
                "TV, laptop or PC": 135,
                "Large item of furniture": 65,
                "Washing machine, dishwasher, tumble dryer or fridge freezer": 150,
                "Mobile phone or tablet": 20
            },
            "spend_factors": { # kg CO2e/£
                "clothes": 0.5,
                "pets": 1.5,
                "health_beauty": 0.4,
                "entertainment": 0.45 
            },
            "services_annual": 75 
        }
    }

    # Input Value Mappings (converting string ranges to numbers)
    _INPUT_MAPPINGS = {
        "spend_ranges": {
            "£0": 0,
            "£0 - £10": 5,
            "£0 - £25": 12.5,
            "£1 - £10": 5.5,
            "£1 - £35": 17.5,
            "£1 - £40": 20.5,
            "£10 - £35": 22.5,
            "£10 - £40": 25,
            "£10 - £60": 35,
            "£25 - £50": 37.5,
            "£35 - £70": 52.5,
            "£35+": 45, # Estimate
            "£40 - £100": 70,
            "£50 - £75": 62.5,
            "£60+": 80, # Estimate
            "£70+": 90, # Estimate
            "£75+": 100, # Estimate
            "£100+": 150, # Estimate
            "More than £40": 60, # Estimate
            "I don't have a pet": 0
        },
        "waste_ranges": {
            "None": 0,
            "0% - 10%": 5,
            "10% - 30%": 20,
            "More than 30%": 40
        },
        "time_ranges": {
            "I don't travel by train": 0,
            "I don't travel by bus": 0,
            "Under 1 hour": 0.5,
            "Under 2 hours": 1,
            "1 to 3 hours": 2,
            "2 to 5 hours": 3.5,
            "3 to 6 hours": 4.5,
            "5 to 15 hours": 10,
            "6 to 10 hours": 8,
            "15 to 25 hours": 20,
            "Over 10 hours": 15,
            "Over 25 hours": 30
        },
        "offset_percentage": {
            "None of them": 0,
            "25%": 25,
            "50%": 50,
            "75%": 75,
            "All of them": 100,
            "Not applicable": 0
        },
        "house_size": { # Bedrooms
            "1": 1, "2": 2, "3": 3, "4 or more": 4.5
        },
        "people_count": {
            "1": 1, "2": 2, "3": 3, "4": 4, "5 or more": 5.5
        }
    }

    def __init__(self, data: dict):
        self._data = data
        self._results = {}
        self._validate_inputs()

    def _validate_inputs(self):
        """Ensures people_count and bedrooms are converted to floats to prevent TypeError."""
        # Validate Home Inputs
        home_inputs = self._data.get("home", {})
        
        # Bedrooms
        bedrooms_str = home_inputs.get("bedrooms", "3")
        try:
            # Check if it's mapped
            if bedrooms_str in self._INPUT_MAPPINGS["house_size"]:
                pass # it will be converted later via _get_mapped_value or we can pre-convert if needed
            else:
                 # If somehow a direct number string came in
                 float(bedrooms_str)
        except ValueError:
            pass # Keep strict string mapping assumption or log warning

        # People Count
        people_str = home_inputs.get("people_count", "1")
        # Ensure it has a mapping or default
        if people_str not in self._INPUT_MAPPINGS["people_count"]:
            # Fallback or log? For now we trust strict mapping or defaults.
            pass

    def calculate(self) -> dict:
        food = self._calculate_food()
        travel = self._calculate_travel()
        home = self._calculate_home()
        stuff = self._calculate_stuff()

        total = food + travel + home + stuff

        self._results = {
            "breakdown": {
                "food": round(food, 2),
                "travel": round(travel, 2),
                "home": round(home, 2),
                "stuff": round(stuff, 2)
            },
            "total": round(total, 2)
        }
        return self._results

    def _get_mapped_value(self, category: str, key: str, default=0.0):
        """Helper to get numerical value from string inputs."""
        return self._INPUT_MAPPINGS.get(category, {}).get(key, default)

    def _calculate_food(self) -> float:
        emissions = 0.0
        factors = self._EMISSION_FACTORS["food"]
        inputs = self._data.get("food", {})

        # 1. Diet
        diet_type = inputs.get("diet_type", "")
        # Default to vegetarian if missing for safety, but typically should match
        daily_factor = factors["diet"].get(diet_type, factors["diet"]["Meat in some meals"])
        emissions += daily_factor * 365

        # 2. Eating out
        spend_str = inputs.get("eating_out_spend_per_week", "£0")
        spend_val = self._get_mapped_value("spend_ranges", spend_str)
        emissions += spend_val * 52 * factors["spend_factor"]

        # 3. Waste
        waste_str = inputs.get("waste_percentage", "10% - 30%")
        waste_pct = self._get_mapped_value("waste_ranges", waste_str)
        
        # Dynamic Waste Scaling
        waste_scale = 1.0
        if diet_type == "Meat in every meal":
            waste_scale = 1.2
        elif diet_type in ["Vegetarian", "Vegan"]:
            waste_scale = 0.8
            
        annual_waste_kg = (waste_pct / 100.0) * factors["avg_waste_per_person"] * waste_scale
        emissions += annual_waste_kg * factors["waste_landfill_factor"]

        # 4. Local sourcing
        sourcing = inputs.get("local_sourcing", "I don't worry about where my food comes from")
        reduction_pct = factors["local_sourcing_reduction"].get(sourcing, 0.0)
        emissions = emissions * (1.0 - reduction_pct)

        return round(emissions, 4)

    def _calculate_travel(self) -> float:
        emissions = 0.0
        factors = self._EMISSION_FACTORS["travel"]
        inputs = self._data.get("travel", {})

        # 1. Car/Motorbike
        general_vehicle = inputs.get("general_vehicle", "Car")
        if "Neither" in general_vehicle:
            vehicle_factor = 0.0
            hours_str = "Under 2 hours"
        else:
            specific_vehicle = inputs.get("specific_vehicle", "Medium petrol or diesel car")
            vehicle_factor = factors["vehicle_per_km"].get(specific_vehicle, 0.275)
            hours_str = inputs.get("car_hours_per_week", "Under 2 hours")

        if vehicle_factor > 0:
            hours = self._get_mapped_value("time_ranges", hours_str)
            
            # Dynamic Speed
            if "Motorbike" in general_vehicle:
                speed = factors["speeds"]["Motorbike"]
            else:
                speed = factors["speeds"]["Car"]
            
            distance_km = hours * speed * 52
            emissions += distance_km * vehicle_factor

        # 2. Train
        train_str = inputs.get("train_hours_per_week", "I don't travel by train")
        train_hours = self._get_mapped_value("time_ranges", train_str)
        if train_hours > 0:
             train_km = train_hours * factors["speeds"]["Train"] * 52
             emissions += train_km * factors["vehicle_per_km"]["Train"]

        # 3. Bus
        bus_str = inputs.get("bus_hours_per_week", "I don't travel by bus")
        bus_hours = self._get_mapped_value("time_ranges", bus_str)
        if bus_hours > 0:
            bus_km = bus_hours * factors["speeds"]["Bus"] * 52
            emissions += bus_km * factors["vehicle_per_km"]["Bus"]

        # 4. Flights
        flights = inputs.get("flights", {})
        dom_trips = float(flights.get("domestic", 0))
        eur_trips = float(flights.get("europe", 0))
        long_trips = float(flights.get("long_haul", 0))

        # Aviation Logic: RF multiplier (1.9x) + Distance Uplift (1.1x)
        rf_multiplier = 1.9
        dist_uplift = 1.1

        flight_emissions = (
            (dom_trips * (factors["flights"]["Domestic"]["distance"] * dist_uplift) * factors["flights"]["Domestic"]["factor"]) +
            (eur_trips * (factors["flights"]["Europe"]["distance"] * dist_uplift) * factors["flights"]["Europe"]["factor"]) +
            (long_trips * (factors["flights"]["LongHaul"]["distance"] * dist_uplift) * factors["flights"]["LongHaul"]["factor"])
        )
        
        # Apply RF
        flight_emissions *= rf_multiplier

        # 5. Offset
        offset_str = inputs.get("flight_offset_percentage", "None of them")
        offset_pct = self._get_mapped_value("offset_percentage", offset_str)
        
        # Add net emissions
        emissions += flight_emissions * (1.0 - (offset_pct / 100.0))

        return round(emissions, 4)

    def _calculate_home(self) -> float:
        emissions = 0.0
        factors = self._EMISSION_FACTORS["home"]
        inputs = self._data.get("home", {})

        # People & Bedrooms
        people_str = inputs.get("people_count", "1")
        people = self._get_mapped_value("people_count", people_str, default=1)
        
        bedrooms_str = inputs.get("bedrooms", "1")
        bedrooms = self._get_mapped_value("house_size", bedrooms_str, default=1)

        # Dynamic Baselines
        base_gas = 7000 + (2000 * bedrooms)
        base_elec = 1500 + (500 * bedrooms)

        # 1. Heating
        heat_source = inputs.get("heating_source", "Gas")
        heat_factor = factors["heating_factor"].get(heat_source, 0.20)
        
        temp_str = inputs.get("winter_temp", "18° - 21°C")
        temp_adj = factors["temp_adjustment"].get(temp_str, 0.0)
        
        improvements = inputs.get("improvements", [])
        imp_reduction_sum = 0.0
        for imp in improvements:
            imp_reduction_sum += factors["improvements_reduction"].get(imp, 0.0)
        
        imp_reduction_sum = min(imp_reduction_sum, 0.8)

        adjusted_heating_kwh = base_gas * (1.0 + temp_adj) * (1.0 - imp_reduction_sum)
        heating_emissions = adjusted_heating_kwh * heat_factor

        # 2. Electricity
        green_tariff = inputs.get("green_tariff", "No")
        elec_factor = factors["electricity_factor"]
        
        if "100%" in green_tariff:
            elec_factor = 0.0
        elif "less than 100%" in green_tariff:
            elec_factor *= 0.5
        
        lights = inputs.get("lights_off", "No")
        elec_usage = base_elec * (0.95 if lights == "Yes" else 1.0)
        elec_emissions = elec_usage * elec_factor

        total_home_emissions = heating_emissions + elec_emissions

        # Shared Responsibility Model:
        # 40% fixed (building base load) + 60% variable (divided by people)
        emissions = (total_home_emissions * 0.4) + ((total_home_emissions * 0.6) / people)

        return round(emissions, 4)

    def _calculate_stuff(self) -> float:
        emissions = 0.0
        factors = self._EMISSION_FACTORS["stuff"]
        inputs = self._data.get("stuff", {})

        # 1. New items
        purchases = inputs.get("purchases", [])
        for item in purchases:
            emissions += factors["items_annualised"].get(item, 0)

        # 2. Monthly Spends
        def get_spend(key):
            s = inputs.get(key, "£0")
            return self._get_mapped_value("spend_ranges", s)

        emissions += get_spend("clothes_spend") * 12 * factors["spend_factors"]["clothes"]
        emissions += get_spend("pet_spend") * 12 * factors["spend_factors"]["pets"]
        emissions += get_spend("beauty_spend") * 12 * factors["spend_factors"]["health_beauty"]
        emissions += get_spend("hobbies_spend") * 12 * factors["spend_factors"]["entertainment"]

        # 3. Services
        contracts_str = inputs.get("contracts_spend", "£0")
        if contracts_str != "£0":
             emissions += factors["services_annual"]

        # 4. Recycling
        recycled_items = inputs.get("recycling", [])
        if recycled_items:
            reduction_pct = min(len(recycled_items) * 0.01, 0.05)
            emissions = emissions * (1.0 - reduction_pct)

        return round(emissions, 4)


class MockDataProvider:
    """Provides mock data using strict string inputs matching the questionnaire."""
    
    @staticmethod
    def get_mock_data():
        return {
            "food": {
                "diet_type": "Meat in some meals",
                "eating_out_spend_per_week": "£10 - £40",
                "waste_percentage": "0% - 10%",
                "local_sourcing": "Some of the food I buy is locally sourced"
            },
            "travel": {
                "general_vehicle": "Car",
                "specific_vehicle": "Medium petrol or diesel car",
                "car_hours_per_week": "5 to 15 hours",
                "train_hours_per_week": "Under 2 hours",
                "bus_hours_per_week": "1 to 3 hours",
                "flights": {
                    "domestic": 1,
                    "europe": 1,
                    "long_haul": 0
                },
                "flight_offset_percentage": "None of them"
            },
            "home": {
                "house_type": "Semi-detached",
                "bedrooms": "3",
                "people_count": "2",
                "heating_source": "Gas",
                "green_tariff": "No",
                "lights_off": "Yes",
                "winter_temp": "18° - 21°C",
                "improvements": ["Energy saving lightbulbs", "Loft insulation", "Double glazing"]
            },
            "stuff": {
                "purchases": ["Mobile phone or tablet"],
                "clothes_spend": "£40 - £100",
                "pet_spend": "I don't have a pet",
                "beauty_spend": "£10 - £60",
                "contracts_spend": "£35 - £70",
                "hobbies_spend": "£25 - £50",
                "recycling": ["Paper", "Tin cans", "Plastic", "Glass"]
            }
        }