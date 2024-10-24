import pandas as pd
import requests
from scipy.optimize import minimize
from pyowm import OWM  # OpenWeatherMap API wrapper
import vertexai
from vertexai.language_models import TextGenerationModel

# ---------- CONFIGURATION ----------
OWM_API_KEY = '067dd15b9d0807e3990e984320fc7a0b'
NASA_API_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
VERTEX_PROJECT = "tree-of-life-algo-439316"
VERTEX_LOCATION = "us-central1"

# ---------- Step 1: Climate and Weather Data ----------
def get_nasa_climate_data(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "start": "2023",  # Last year’s climate data
        "end": "2023",
        "parameters": "T2M,PRECTOTCORR",
        "format": "JSON"
    }
    response = requests.get(NASA_API_URL, params=params)
    data = response.json()

    if "properties" in data:
        temp_data = data["properties"]["parameter"]["T2M"]
        precip_data = data["properties"]["parameter"]["PRECTOTCORR"]

        avg_temp = sum(temp_data.values()) / len(temp_data)
        total_precip_mm = sum(precip_data.values())
        total_precip_in = total_precip_mm / 25.4

        return avg_temp, total_precip_in
    else:
        raise ValueError("Unable to fetch climate data from NASA API.")

def get_current_weather(lat, lon):
    owm = OWM(OWM_API_KEY)
    mgr = owm.weather_manager()
    weather = mgr.weather_at_coords(lat, lon).weather

    temp_c = weather.temperature('celsius')['temp']
    humidity = weather.humidity
    precipitation = weather.rain.get('1h', 0)

    return temp_c, humidity, precipitation

# ---------- Step 2: Plant Filtering and Scoring ----------
def weighted_plant_score(row, temp_f, avg_precip_in):
    temp_diff = abs(row['TEMP_TOLR_MIN'] - temp_f)
    precip_diff = abs(row['PRECIP_TOLR_MIN'] - avg_precip_in)

    survivability_score = max(0, 50 - (temp_diff + precip_diff))
    sequestration_score = {"High": 50, "Medium": 30, "Low": 10, "Minimal": 0}.get(
        row['Carbon_Sequestration_Tier'], 0
    )
    return survivability_score + sequestration_score

def filter_and_score_plants(plant_data, temp_c, avg_precip_in):
    temp_f = temp_c * 9 / 5 + 32  # Convert Celsius to Fahrenheit

    plant_data = plant_data.dropna(
        subset=['TEMP_TOLR_MIN', 'TEMP_TOLR_MIN_RNG', 'PRECIP_TOLR_MIN', 'PRECIP_TOLR_MAX']
    )
    plant_data['TEMP_TOL_MAX'] = plant_data['TEMP_TOLR_MIN'] + plant_data['TEMP_TOLR_MIN_RNG']
    plant_data['Score'] = plant_data.apply(
        weighted_plant_score, axis=1, args=(temp_f, avg_precip_in)
    )

    return plant_data[plant_data['Score'] > 50].sort_values('Score', ascending=False)

# ---------- Step 3: Optimization for Carbon Credits ----------
def optimize_tree_count(target_carbon, sequestration_rate_per_tree, max_trees):
    def objective(num_trees):
        return abs(target_carbon - (num_trees * sequestration_rate_per_tree))

    result = minimize(objective, x0=[1], bounds=[(1, max_trees)], method='SLSQP')
    return int(result.x[0]) if result.success else max_trees

# ---------- Step 4: Vertex AI Integration ----------
def generate_planting_plan(location, plants, land_size, carbon_credits, years):
    vertexai.init(project=VERTEX_PROJECT, location=VERTEX_LOCATION)
    model = TextGenerationModel.from_pretrained("text-bison@001")

    plant_summary = ", ".join([f"{p['SCINAME']} ({p['Carbon_Sequestration_Tier']})" for p in plants])

    prompt = f"""
    You are an expert tasked with creating a carbon-sequestering planting plan for:
    Location: {location}
    Land Size: {land_size} acres
    Required Carbon Credits: {carbon_credits}
    Time Frame: {years} years

    Recommended Plants:
    {plant_summary}

    1. Calculate the number of each plant required to meet the target carbon credits.
    2. Ensure the total number of plants fits within the given land area.
    3. Provide estimates of yearly carbon sequestration and maturity timelines.
    """

    response = model.predict(prompt, max_tokens=512)
    return response.text

# ---------- Step 5: Main Execution ----------
if __name__ == "__main__":
    # GPS Coordinates for testing
    lat, lon = 41.7215, -93.6577  # Example: Iowa, USA
    land_size = 47  # Acres
    target_carbon_credits = 10  # Carbon credits needed
    time_frame = 20  # Years

    # Load plant data
    plant_data = pd.read_csv('Plants_Carbon_Sequestration_Data.csv')

    # Fetch climate data
    avg_temp, avg_precip_in = get_nasa_climate_data(lat, lon)

    # Fetch current weather (optional, for more precision)
    temp_c, humidity, precip = get_current_weather(lat, lon)

    # Filter and prioritize plants
    filtered_plants = filter_and_score_plants(plant_data, temp_c, avg_precip_in)

    # Optimize tree count
    sequestration_rate_per_tree = 0.5  # Example rate: 0.5 tons of carbon per tree per year
    max_trees = 1000  # Upper bound for optimization

    optimal_tree_count = optimize_tree_count(
        target_carbon_credits, sequestration_rate_per_tree, max_trees
    )

    # Generate planting plan with AI
    planting_plan = generate_planting_plan(
        location=[lat, lon],
        plants=filtered_plants.to_dict('records'),
        land_size=land_size,
        carbon_credits=target_carbon_credits,
        years=time_frame
    )

    # Output the plan
    print("Optimal Planting Plan:")
    print(planting_plan)
