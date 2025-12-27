# Emission Factor Suggestions for Footprint Calculator

Here are suggested emission factors for the questions in your carbon footprint calculator, based on available data, primarily from UK sources.

**Important Considerations:**

*   **Approximations:** These are estimations. Actual emissions can vary based on many factors, including specific brands, individual usage patterns, and the exact energy mix at any given time.
*   **Units:** Pay close attention to the units (e.g., per kg, per km, per kWh, per £). You'll need to multiply these factors by the user's input (e.g., distance traveled, energy consumed).
*   **Geographic Specificity:** These figures are primarily based on UK data, as requested.

---

## Food Category Emission Factors

1.  **How would you best describe your diet?**
    *   **Meat in every meal (High Meat):** ~10.2 kg CO₂e/day
    *   **Meat in some meals (Medium Meat):** ~5.6 kg CO₂e/day
    *   **No beef (Low Meat):** ~4.7 kg CO₂e/day
    *   **Vegetarian:** ~4.2 kg CO₂e/day
    *   **Vegan:** ~2.5 kg CO₂e/day
    *   *Note: These are approximations. To get an annual estimate, multiply the daily figure by 365.*

2.  **In a week, how much do you spend on food from restaurants, canteens and takeaways?**
    *   Use an emission factor of **0.234 kg CO₂e per £1 spent** for food and beverage serving services.
    *   **Calculation Example:** (Amount spent per week) \* 52 weeks \* 0.234 kg CO₂e/£

3.  **Of the food you buy how much is wasted and thrown away?**
    *   Assume an average UK food waste of ~70 kg per person per year.
    *   Use an emission factor for landfilled food waste: **1.38 kg CO₂e per kg of food waste**.
    *   **Calculation Example:** (Percentage of food wasted / 100) \* 70 kg/year \* 1.38 kg CO₂e/kg

4.  **How often do you buy locally produced food that is not imported to the UK?**
    *   This is generally a minor factor compared to diet type. You could apply a percentage reduction to overall food emissions.
    *   **A lot of the food I buy is locally sourced:** -5% reduction on total food emissions
    *   **Some of the food I buy is locally sourced:** -2% reduction on total food emissions
    *   **I don't worry about where my food comes from:** 0% reduction

---

## Travel Category Emission Factors

1.  **What kind of vehicle do you travel in most often as driver or passenger? (if any) & Which of these best describes the vehicle you use most?**
    *   **Small Petrol Car:** ~0.25 kg CO₂e/km
    *   **Medium Petrol Car:** ~0.27 kg CO₂e/km
    *   **Large Petrol Car:** ~0.31 kg CO₂e/km
    *   **Small Diesel Car:** ~0.26 kg CO₂e/km
    *   **Medium Diesel Car:** ~0.28 kg CO₂e/km
    *   **Large Diesel Car:** ~0.32 kg CO₂e/km
    *   **Electric Car:** ~0.06 kg CO₂e/km (based on average UK electricity grid emissions)
    *   **Plug-in Hybrid Car:** ~0.18 kg CO₂e/km
    *   **Hybrid Car:** ~0.18 kg CO₂e/km
    *   **Motorbike:** ~0.11 kg CO₂e/km
    *   **Neither (Walk/Cycle/Public Transport):** 0 kg CO₂e/km (for this question)

2.  **How many hours a week do you spend in your car or on your motorbike for personal use including commuting?**
    *   *You would need to convert hours to distance using an average speed (e.g., 30 km/h) and then multiply by the vehicle's kg CO₂e/km factor.*

3.  **How many hours a week do you spend on the train for personal use including commuting?**
    *   **National Rail (Average):** ~0.04 kg CO₂e/passenger-km
    *   *You would need to convert hours to distance using an average speed (e.g., 60 km/h for trains) and then multiply by the kg CO₂e/passenger-km factor.*

4.  **How many hours a week do you spend on the bus for personal use including commuting?**
    *   **Average Local Bus:** ~0.10 kg CO₂e/passenger-km
    *   *You would need to convert hours to distance using an average speed (e.g., 20 km/h for buses) and then multiply by the kg CO₂e/passenger-km factor.*

5.  **In the last year, how many return flights have you made in total to the following locations?**
    *   **Domestic (UK / Ireland):** ~0.27 kg CO₂e/passenger-km
    *   **To/from Europe (Short-haul):** ~0.16 kg CO₂e/passenger-km
    *   **To/from outside Europe (Long-haul):** ~0.15 kg CO₂e/passenger-km
    *   *Note: For each flight, you will need to estimate the distance. For example, average short-haul 1500km, long-haul 6000km.*

6.  **What percentage of your flights do you offset?**
    *   This is a direct reduction. If a user offsets X%, reduce their calculated flight emissions by X%.

---

## Home Category Emission Factors

1.  **What kind of house do you live in?**
    *   This question is best used as a multiplier for energy consumption (e.g., larger houses use more energy). You'd likely need average energy consumption data for each type in your calculator's backend.

2.  **How many bedrooms does your house have? & How many people (aged 17 and over) live in your house?**
    *   These factors can further refine baseline energy consumption estimates. More bedrooms and more occupants generally lead to higher energy use, but per-person emissions might decrease with more occupants due to shared spaces.

3.  **How do you heat your home?**
    *   **Gas (Natural Gas):** ~0.20 kg CO₂e/kWh
    *   **Oil (Heating Oil):** ~0.26 kg CO₂e/kWh
    *   **Electricity:** ~0.23 kg CO₂e/kWh (average UK grid)
    *   **Wood (e.g., pellets, sustainable source):** ~0.02 kg CO₂e/kWh
    *   **Heatpump:** This is highly efficient. Use the electricity factor (~0.23 kg CO₂e/kWh) divided by a typical Coefficient of Performance (COP) (e.g., 3-4). So, ~0.06 - 0.08 kg CO₂e/kWh.

4.  **Is your electricity on a green tariff?**
    *   **I don't know / No:** Use average UK grid electricity factor (~0.23 kg CO₂e/kWh)
    *   **Yes but the tariff is less than 100% renewables:** Apply a partial reduction, e.g., 50% of the grid factor.
    *   **Yes 100%:** 0 kg CO₂e/kWh

5.  **Do you regularly turn off lights and not leave your appliances on standby?**
    *   **Yes:** Apply a small reduction to electricity consumption (e.g., -5%).
    *   **No:** No reduction.

6.  **How warm do you keep your home in winter?**
    *   This impacts heating energy use. Use a baseline (e.g., 18-21°C = 0% adjustment). Each 1°C change can alter energy use by ~10%.
    *   **Below 14°C:** -20% on heating energy
    *   **14° - 17°C:** -10% on heating energy
    *   **18° - 21°C:** Baseline heating energy
    *   **Over 21°C:** +10% on heating energy

7.  **Which of these home energy efficiency improvements are installed in your home?**
    *   These offer percentage reductions on relevant energy consumption (mostly heating).
    *   **Energy saving lightbulbs:** Modern standard; negligible additional reduction.
    *   **Loft insulation:** -15% on heating energy
    *   **Cavity or solid wall insulation:** -15% on heating energy
    *   **Condensing boiler:** If upgrading from old, -20% on gas heating emissions.
    *   **Double glazing:** -10% on heating energy
    *   **Low flow fittings to taps and showers:** Small reduction on hot water heating.
    *   **Solar panels / Solar water heater:** These significantly reduce grid electricity/gas. Requires specific calculator logic based on system size and output.

---

## Stuff Category Emission Factors

This category often relies on expenditure-based factors due to the diversity of products.

1.  **In the last 12 months, have you bought any of these new household items?**
    *   These are lifetime emissions, which need to be annualized for a yearly footprint. Very rough annual estimates:
    *   **TV, laptop or PC:** ~100-170 kg CO₂e/year (annualized)
    *   **Large item of furniture:** ~30-100 kg CO₂e/year (annualized)
    *   **Washing machine, dishwasher, tumble dryer or fridge freezer:** ~100-200 kg CO₂e/year (annualized)
    *   **Mobile phone or tablet:** ~15-25 kg CO₂e/year (annualized)

2.  **In a typical month, how much do you spend on clothes and footwear?**
    *   **Expenditure-based factor:** ~0.5 kg CO₂e per £1 spent.

3.  **In a typical month, how much do you spend on your pets and pet food?**
    *   **Expenditure-based factor:** ~1.5 kg CO₂e per £1 spent (highly variable).

4.  **In a typical month, how much do you spend on health, beauty and grooming products?**
    *   **Expenditure-based factor:** ~0.4 kg CO₂e per £1 spent.

5.  **In a typical month, how much do you spend on phone, internet and TV contracts?**
    *   This is for services. A flat annual estimate is often used: ~50-100 kg CO₂e/year.

6.  **In a typical month, how much do you spend on entertainment and hobbies?**
    *   Highly variable. A general consumer goods expenditure factor (e.g., ~0.4-0.5 kg CO₂e per £1 spent) can be used as a proxy if more specific data is unavailable.

7.  **Which of these types of waste do you recycle and/or compost?**
    *   Recycling can reduce emissions compared to landfill. For a simplified approach, you could apply a small reduction for each item recycled. For food waste, if composted, use ~0.11 kg CO₂e/kg instead of 1.38 kg CO₂e/kg (for landfilled).

---

## Personalisation / Other

These questions are for demographic or location context and do not directly map to emission factors but help refine other calculations or personalize results.

*   **Where are you based?** (UK/Outside UK/Postcode) - Used for regional emission factors (e.g., electricity grid mix).
*   **How old are you?** - Demographic data for analysis or tailored advice.
