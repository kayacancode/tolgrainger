import pandas as pd
import requests
from pyowm import OWM
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
from vertexai.preview.prompts import Prompt
import numpy as np
from scipy.optimize import linear_sum_assignment

def get_average_annual_precipitation(lat, lon):
    start_date = '2022-01-01'
    end_date = '2022-12-31'
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&daily=precipitation_sum&timezone=UTC"
    )
    response = requests.get(url)
    data = response.json()
    if 'daily' in data and 'precipitation_sum' in data['daily']:
        precipitation_list = data['daily']['precipitation_sum']
        total_precipitation_mm = sum(precipitation_list)
        total_precipitation_in = total_precipitation_mm / 25.4
        return total_precipitation_in
    else:
        return None

def get_weather_data(lat, lon, api_key):
    owm = OWM(api_key)
    mgr = owm.weather_manager()
    weather = mgr.weather_at_coords(lat, lon).weather
    temperature_c = weather.temperature('celsius')['temp']
    humidity = weather.humidity
    precipitation = weather.rain.get('1h', 0)
    return temperature_c, humidity, precipitation

def filter_and_prioritize_plants(plant_data, temperature_c, avg_annual_precipitation_in):
    temperature_f = temperature_c * 9 / 5 + 32
    plant_data = plant_data.copy()
    numeric_columns = ['TEMP_TOLR_MIN', 'TEMP_TOLR_MIN_RNG', 'PRECIP_TOLR_MIN', 'PRECIP_TOLR_MAX']
    plant_data[numeric_columns] = plant_data[numeric_columns].apply(pd.to_numeric, errors='coerce')
    plant_data.dropna(subset=numeric_columns, inplace=True)
    plant_data['TEMP_TOL_MAX'] = plant_data['TEMP_TOLR_MIN'] + plant_data['TEMP_TOLR_MIN_RNG']

    temperature_condition = (
        (plant_data['TEMP_TOLR_MIN'] <= temperature_f + 5) &
        (plant_data['TEMP_TOL_MAX'] >= temperature_f - 5)
    )
    precipitation_condition = (
        (plant_data['PRECIP_TOLR_MIN'] <= avg_annual_precipitation_in + 5) &
        (plant_data['PRECIP_TOLR_MAX'] >= avg_annual_precipitation_in - 5)
    )
    combined_condition = temperature_condition & precipitation_condition
    weather_filtered_plants = plant_data[combined_condition].copy()

    sequestration_order = ['High', 'Medium', 'Low', 'Minimal']
    weather_filtered_plants['Carbon_Sequestration_Tier'] = pd.Categorical(
        weather_filtered_plants['Carbon_Sequestration_Tier'],
        categories=sequestration_order,
        ordered=True
    )
    prioritized_plants = weather_filtered_plants.sort_values('Carbon_Sequestration_Tier')
    return prioritized_plants

def optimize_plant_selection(prioritized_plants, land_size, requested_carbon_credits, time_frame):
    # Assign numerical values to Carbon_Sequestration_Tier
    tier_values = {'High': 4, 'Medium': 3, 'Low': 2, 'Minimal': 1}
    prioritized_plants['Tier_Value'] = prioritized_plants['Carbon_Sequestration_Tier'].map(tier_values)
    
    # Calculate a score based on Carbon_Sequestration_Tier and growth rate
    prioritized_plants['Score'] = prioritized_plants['Tier_Value'] * prioritized_plants['Growth_Rate']
    
    # Sort plants by score in descending order
    sorted_plants = prioritized_plants.sort_values('Score', ascending=False)
    
    # Select top plants that fit within land size and meet carbon credit requirement
    selected_plants = []
    total_area = 0
    total_credits = 0
    
    for _, plant in sorted_plants.iterrows():
        if total_area < land_size and total_credits < requested_carbon_credits:
            plant_area = min(plant['Mature_Spread'] ** 2, land_size - total_area)
            num_plants = int(plant_area / (plant['Mature_Spread'] ** 2))
            if num_plants > 0:
                selected_plants.append({
                    'SCINAME': plant['SCINAME'],
                    'Quantity': num_plants,
                    'Maturity': 'Young',  # Assuming young plants for faster growth
                    'Area': plant_area
                })
                total_area += plant_area
                total_credits += num_plants * plant['Carbon_Sequestration_Rate'] * time_frame
        else:
            break
    
    return selected_plants, total_credits

def generate_planting_plan(gps_location, selected_plants, land_size, total_credits):
    plan = f"""
Recommended Planting Plan for GPS: {gps_location[0]}, {gps_location[1]}

Size of Land: {land_size} acres

Plant | Quantity | Plant Maturity
------|----------|---------------
"""
    for plant in selected_plants:
        plan += f"{plant['SCINAME']} | {plant['Quantity']} | {plant['Maturity']}\n"

    plan += f"""
Estimated Carbon Sequestration Per Year:
* With Recommended Plants: {total_credits / 20:.2f} tons

Yearly Carbon Sequestration (with recommended plants): {total_credits / 20:.2f} tons

Additional Considerations:
* This plan prioritizes plant survival based on known factors and optimizes for carbon sequestration.
* The analysis may not encompass all possible conditions, and professional assessment is recommended.
"""
    return plan

if __name__ == "__main__":
    api_key = '067dd15b9d0807e3990e984320fc7a0b'
    plant_data = pd.read_csv('Plants_Carbon_Sequestration_Data.csv')
    lat, lon = 41.7215, -93.6577  # Demo GPS coordinates
    land_size = 47  # Land size in acres
    requested_carbon_credits = 10  # Estimated Carbon Credits Requested
    time_frame = 20  # Carbon Credits requested over X years

    avg_annual_precipitation_in = get_average_annual_precipitation(lat, lon)
    temperature_c, humidity, _ = get_weather_data(lat, lon, api_key)
    filtered_plants = filter_and_prioritize_plants(plant_data, temperature_c, avg_annual_precipitation_in)
    
    selected_plants, total_credits = optimize_plant_selection(filtered_plants, land_size, requested_carbon_credits, time_frame)
    planting_plan = generate_planting_plan([lat, lon], selected_plants, land_size, total_credits)
    
    print(planting_plan)