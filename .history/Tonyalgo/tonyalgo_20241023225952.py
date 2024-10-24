import pandas as pd
import requests
from pyowm import OWM  # OpenWeatherMap API wrapper
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
from vertexai.preview.prompts import Prompt


# ---------- Step 1: Plant Filtering Script ----------
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
    plant_data['TEMP_TOLR_MIN'] = pd.to_numeric(plant_data['TEMP_TOLR_MIN'], errors='coerce')
    plant_data['TEMP_TOLR_MIN_RNG'] = pd.to_numeric(plant_data['TEMP_TOLR_MIN_RNG'], errors='coerce')
    plant_data['PRECIP_TOLR_MIN'] = pd.to_numeric(plant_data['PRECIP_TOLR_MIN'], errors='coerce')
    plant_data['PRECIP_TOLR_MAX'] = pd.to_numeric(plant_data['PRECIP_TOLR_MAX'], errors='coerce')
    plant_data.dropna(subset=['TEMP_TOLR_MIN', 'TEMP_TOLR_MIN_RNG', 'PRECIP_TOLR_MIN', 'PRECIP_TOLR_MAX'], inplace=True)
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

    weather_filtered_plants['Carbon_Sequestration_Tier'] = pd.Categorical(
        weather_filtered_plants['Carbon_Sequestration_Tier'],
        categories=['High', 'Medium', 'Low', 'Minimal'],
        ordered=True
    )
    prioritized_plants = weather_filtered_plants.sort_values('Carbon_Sequestration_Tier')
    return prioritized_plants


def prepare_for_vertex_ai(plant_data):
    plant_list = plant_data[['SCINAME', 'Carbon_Sequestration_Tier']].to_dict('records')
    return plant_list


# ---------- Step 2: Updated Generative AI Script ----------
def generate(gps_location, plants_list, land_size, requested_carbon_credits, time_frame):
    vertexai.init(project="tree-of-life-algo-439316", location="us-central1")

    # Ensure GPS location is a string format
    gps_location_str = f"{gps_location[0]}, {gps_location[1]}"

    # Convert other variables to strings if necessary
    land_size_str = str(land_size)
    plants_list_str = ", ".join([f"{plant['SCINAME']} ({plant['Carbon_Sequestration_Tier']})" for plant in plants_list])

    requested_carbon_credits_str = str(requested_carbon_credits)
    time_frame_str = str(time_frame)

    variables = [
        {
            "GpsLocation": gps_location_str,
            "PlantsListBasedOnWeather": plants_list_str,
            "SizeOfLand": land_size_str,
            "CarbonCreditsRequested": requested_carbon_credits_str,
            "TimeFrame": time_frame_str
        },
    ]

    prompt = Prompt(
        prompt_data=[text1],
        model_name="gemini-1.5-flash-002",
        variables=variables,
        generation_config=generation_config,
        safety_settings=safety_settings,
    )

    responses = prompt.generate_content(
        contents=prompt.assemble_contents(**prompt.variables[0]),
        stream=True,
    )

    for response in responses:
        print(response.text, end="")


text1 = """
You are an expert horticulturalist and environmental analyst tasked with maximizing carbon sequestration for a given land area.  You will receive the following information:

**GPS Location:** 
{GpsLocation}

**Plants List Based on Weather:** 
{PlantsListBasedOnWeather}

**Size of Land:** 
{SizeOfLand}

**Carbon Credits Requested:** 
{CarbonCreditsRequested}

**Desired Time Frame:** 
{TimeFrame}


Your task is to generate a planting plan that optimizes carbon sequestration while adhering to local regulations.

1. **Filter Plants:**  Review the provided `PlantsListBasedOnWeather` and cross-reference it with local regulations for the specified GPS location. Remove any invasive or prohibited plants from the list, and instead replace them with known plants that thrive and sequester the most carbon for the given area.

2. **Necessary Plant Quantity and Maturity:** Determine the number of filtered plants necessary plant and their maturity in order to sequester enough carbon to meet the value of `CarbonCreditsRequested` over the determined `TimeFrame`.
    * Quantity of plants must be able to successfully grow within `SizeOfLand` in acres. 
    * Please note 1 Carbon Credit is equivalent to 1 Ton of Carbon Sequestered. 
    * Also, prioritize younger plants although meeting the carbon credits is top priority.

3. **Carbon Sequestration Estimation:**
    * Calculate the total estimated carbon sequestered by the recommended plants over one year, assuming optimal planting and growth.
    * Estimate the current carbon sequestration of the area based on the provided information.

4. **Output:** Present your findings in the exact format seen below:
```
Plant | Quantity | Plant Maturity
------- | -------- | --------
Plant A | # | #
Plant B | # | #
...

Estimated Carbon Sequestration Per Year:
* With Recommended Plants: [estimated sequestration with recommended plants]
Yearly Carbon Sequestration (with recommended plants): [amount]

**Additional Considerations:**

* While aiming for optimal carbon sequestration, prioritize plant survival based on the known factors.
* Clearly state how many of each plant are recommended for the given land size.
* Note: The analysis may not encompass all possible conditions and site-analysis/professional assessment is not possible."""

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
]

def main(api_key):
     # Step 1: Plant filtering
    plant_data = pd.read_csv('Plants_Carbon_Sequestration_Data.csv')
    # lat, lon = 47.6061, -122.3328  # Seattle GPS coordinates
    # lat, lon = 27.6648, -81.5158  # Florida GPS coordinates
    # lat, lon = 41.8781, -87.6298  # Chicago GPS coordinates
    # lat, lon = 51.6044, -0.1067  # London GPS coordinates
    lat, lon = 41.7222, -93.6585  # Iowa GPS coordinates
    land_size = 3 # Land size in acres
    requested_carbon_credits = 10 # Estimated Carbon Credits Requested
    time_frame = 10 # Carbon Credits requested over X years

    # Get average annual precipitation using Open-Meteo API
    avg_annual_precipitation_in = get_average_annual_precipitation(lat, lon)

    # Get current weather data using OpenWeatherMap API and your API key
    temperature_c, humidity, _ = get_weather_data(lat, lon, api_key)

    # Filter plants based on weather conditions
    filtered_plants = filter_and_prioritize_plants(plant_data, temperature_c, avg_annual_precipitation_in)

    # Print the original list of filtered plants before passing to Vertex AI
    # print("Original list of filtered plants based on weather conditions and carbon sequestration priority:")
    # print(filtered_plants[['SCINAME', 'Carbon_Sequestration_Tier']].to_string(index=False))

    # Prepare the filtered plant data for Vertex AI
    plants_list_for_ai = prepare_for_vertex_ai(filtered_plants)

    # Step 2: Call the generative AI script with filtered plants
    result = generate(
        gps_location=[lat, lon],
        plants_list=plants_list_for_ai,
        land_size=land_size,
        requested_carbon_credits=requested_carbon_credits,
        time_frame=time_frame
    )

    return result

if __name__ == "__main__":
    main(api_key="067dd15b9d0807e3990e984320fc7a0b")

# ---------- Combined Execution ----------
# if __name__ == "__main__":
    # Insert your OpenWeatherMap API key here
    api_key = '067dd15b9d0807e3990e984320fc7a0b'

    # Step 1: Plant filtering
    plant_data = pd.read_csv('/Users/kayajones/projects/tolgrainger/Tonyalgo/Plants_Carbon_Sequestration_Data.csv')
    # lat, lon = 47.6061, -122.3328  # Seattle GPS coordinates
    # lat, lon = 27.6648, -81.5158  # Florida GPS coordinates
    # lat, lon = 41.8781, -87.6298  # Chicago GPS coordinates
    # lat, lon = 51.6044, -0.1067  # London GPS coordinates
    lat, lon = 41.7222, -93.6585  # Iowa GPS coordinates
    land_size = 3 # Land size in acres
    requested_carbon_credits = 10 # Estimated Carbon Credits Requested
    time_frame = 10 # Carbon Credits requested over X years

    # Get average annual precipitation using Open-Meteo API
    avg_annual_precipitation_in = get_average_annual_precipitation(lat, lon)

    # Get current weather data using OpenWeatherMap API and your API key
    temperature_c, humidity, _ = get_weather_data(lat, lon, api_key)

    # Filter plants based on weather conditions
    filtered_plants = filter_and_prioritize_plants(plant_data, temperature_c, avg_annual_precipitation_in)

    # Print the original list of filtered plants before passing to Vertex AI
    # print("Original list of filtered plants based on weather conditions and carbon sequestration priority:")
    # print(filtered_plants[['SCINAME', 'Carbon_Sequestration_Tier']].to_string(index=False))

    # Prepare the filtered plant data for Vertex AI
    plants_list_for_ai = prepare_for_vertex_ai(filtered_plants)

    # Step 2: Call the generative AI script with filtered plants
    generate(
        gps_location=[lat, lon],
        plants_list=plants_list_for_ai,
        land_size=land_size,
        requested_carbon_credits=requested_carbon_credits,
        time_frame=time_frame
    )