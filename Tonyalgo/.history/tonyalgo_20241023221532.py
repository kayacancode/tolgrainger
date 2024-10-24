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


text1 = """kayacancode
kayacancode
Invisible

Plu — 10/21/2022 12:08 PM
I HAVE ZELLE
LETS GO
kayacancode — 10/21/2022 12:08 PM
Yay
Ok cool
I’m about to leave
Plu — 10/21/2022 12:10 PM
LETS GOO
Just make sure you say yes to a plastic bag for them cause those mfers nasty and look at me funny
Yes on Roosevelt btw
kayacancode — 03/29/2023 10:10 AM
my friends in 485 has pressured me into downloading league of legends
Plu — 03/29/2023 11:03 AM
Oh god
Don’t do it
It’s not worth it kaya 😭😭😭
kayacancode — 03/29/2023 11:07 AM
bro i dont see the CME scholarship under the scholarships tab in the scholarship america hub 
Plu — 03/29/2023 11:09 AM
https://learnmore.scholarsapply.org/cme-scholars/
CME Group Foundation Scholars Program
You did this link?
I am only on mobile right now so I cant check
kayacancode — 03/29/2023 11:09 AM
wait yea it shows now. At first it didn't show. Thank youuu
LOL wtf
Image
not currently
Plu — 03/29/2023 11:13 AM
Just say yea
Fuck it
kayacancode — 03/29/2023 11:13 AM
bettt
Plu — 03/29/2023 11:13 AM
You doing coterm now
kayacancode — 03/29/2023 11:13 AM
LMAOOOO
i think i have to apply like next sem
kayacancode — 03/29/2023 2:15 PM
i added a minor
ngl not tryna do 5 years
LMAO
Plu — 03/29/2023 2:15 PM
LMFAOOOOOOOO
real asf
Plu — Today at 6:48 PM
import pandas as pd
import requests
from pyowm import OWM  # OpenWeatherMap API wrapper
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
from vertexai.preview.prompts import Prompt
Expand
message.txt
10 KB
no idea how accurate that shit is
kayacancode — Today at 7:58 PM
LMAO
let me see
u couldnt drag the python file
Plu — Today at 8:12 PM
SYMBOL,SCINAME,ALEPTH_IND,ANERB_TOLR_CD,BLOAT_POT_CD,BLOOM_PRD_CD,CACO3_TOLR_CD,C_N_RATIO_CD,XMAS_TREE_SUIT_IND,COLD_STRAT_IND,COPPICE_POT_IND,DRGHT_TOLR_CD,FALL_CSPC_IND,FERT_RQMT_CD,FIRE_RESIST_IND,FIRE_TOLR_CD,FLWR_COLOR_CD,FLWR_CSPC_IND,FODDR_SUIT_IND,FOLG_COLOR_CD,FOLG_PRSTY_SUMR_CD,FOLG_PRSTY_WNTR_CD,FOLG_TXT_CD,FROST_FREE_DAY_MIN,FROST_FREE_DAY_MIN_RNG,FRUT_BODY_SUIT_IND,FRUT_SEED_ABUND_CD,FRUT_SEED_COLOR_CD,FRUT_SEED_CSPC_IND,FRUT_SEED_END_CD,FRUT_SEED_PRST_IND,FRUT_SEED_START_CD,FUEL_WOOD_SUIT_CD,GRAS_LOW_GRW_IND,GRWTH_FORM_CD,GRWTH_HABIT_CD,GRWTH_PRD_ACTV_CD,GRWTH_RATE_CD,HEDG_TOLR_CD,HT_AT_MTRTY,HT_AT_MTRTY_RNG,HT_MAX_BASE_AGE,HT_MAX_BASE_AGE_RNG,LEAF_RETNT_IND,LFSPN_CD,LMBR_SUIT_IND,MOIST_USE_CD,NAVL_STOR_SUIT_IND,N_FIX_POT_CD,NURS_STK_SUIT_IND,PALAT_HUMAN_IND,PALAT_ANIML_BRS_CD,PALAT_ANIML_GRZ_CD,PLNT_CLTVR_SEL_IND,PLNT_DEN_HIGH,PLNT_DEN_HIGH_RNG,PLNT_DEN_LOW,PLNT_DEN_LOW_RNG,PLYWD_VNR_SUIT_IND,POST_SUIT_IND,PRECIP_TOLR_MAX,PRECIP_TOLR_MAX_RNG,PRECIP_TOLR_MIN,PRECIP_TOLR_MIN_RNG,PRPG_BARE_ROOT_IND,PRPG_BULB_IND,PRPG_CORM_IND,PRPG_CUT_IND,PRPG_SEED_IND,PRPG_SOD_IND,PRPG_SPRIG_IND,PRPG_TUBR_IND,PRPG_CTNR_IND,PROTEIN_POT_CD,PLPWD_SUIT_IND,RGRWTH_RATE_CD,RSPRT_ABLE_IND,ROOT_DPTH_MIN,ROOT_DPTH_MIN_RNG,SLIN_TOLR_CD,SEED_SPRD_RATE_CD,SEEDLING_VGOR_CD,SEED_PER_LB,SEED_PER_LB_RNG,SHADE_TOLR_CD,SM_GRAIN_IND,SOIL_ADP_C_TXT_IND,SOIL_ADP_F_TXT_IND,SOIL_ADP_M_TXT_IND,SOIL_PH_TOLR_MAX,SOIL_PH_TOLR_MAX_RNG,SOIL_PH_TOLR_MIN,SOIL_PH_TOLR_MIN_RNG,TEMP_TOLR_MIN,TEMP_TOLR_MIN_RNG,TOX_CD,VEG_SPRD_RATE_CD,VS_COMM_AVAIL,Carbon_Sequestration_Tier
ABAM,Abies amabilis,No,None,None,Late Spring,Low,High,Yes,Yes,No,Low,Yes,Low,No,None,Yellow,No,No,Gray-Green,Dense,Dense,Medium,90,82,No,Low,Brown,No,Fall,No,Summer,Low,No,Erect,Single Stem,Spring and Summer,Slow,None,165,150,20,20,Yes,Long,Yes,Medium,No,None,No,No,Low,,,700,500,300,300,Yes,No,260,60,38,30,Yes,No,No,No,Yes,No,No,No,Yes,,Yes,,No,36,36,None,Slow,Low,11280,10,Tolerant,No,Yes,Yes,Yes,6,5.9,3.3,3.3,-28,-32,None,None,Routinely Available,High
ABBA,Abies balsamea,No,None,None,Mid Summer,Low,High,Yes,Yes,No,Low,No,Medium,No,Low,Yellow,No,No,Green,Dense,Dense,Medium,80,67,No,Medium,Brown,No,Fall,No,Fall,Low,No,Conical,Single Stem,Spring and Summer,Slow,Low,60,60,18,15,Yes,Short,Yes,Medium,Yes,None,Yes,No,Medium,,,1200,1000,300,300,Yes,No,60,60,13,10,Yes,No,No,No,Yes,No,No,No,Yes,Low,Yes,,No,20,18,None,Slow,Low,59840,10,Tolerant,No,Yes,Yes,Yes,6,5.9,4,3.9,-43,-47,None,None,Routinely Available,High
ABCO,Abies concolor,No,None,None,Late Spring,Low,High,Yes,Yes,No,Medium,No,Medium,No,Medium,Red,No,No,Green,Dense,Dense,Medium,80,67,No,Medium,Brown,No,Fall,No,Summer,Low,No,Conical,Single Stem,Spring and Summer,Slow,Low,120,100,20,20,Yes,Long,Yes,Medium,No,None,Yes,No,Low,,,1200,1000,300,300,Yes,No,80,60,18,15,Yes,No,No,Yes,Yes,No,No,No,Yes,Low,Yes,,No,40,39,None,Moderate,Medium,15920,10,Intermediate,No,Yes,No,Yes,7.8,7.7,5.5,5.5,-38,-42,None,None,Routinely Available,High
ABFR,Abies fraseri,No,Low,None,Mid Spring,Low,High,Yes,No,No,Low,No,Low,No,Low,Purple,No,No,Dark Green,Moderate,Moderate,Medium,90,82,No,Medium,Brown,Yes,Fall,Yes,Spring,Low,No,Erect,Single Stem,Spring and Summer,Moderate,Low,55,40,20,20,Yes,Moderate,No,Medium,No,None,Yes,No,Low,,,1200,1000,435,300,Yes,No,100,60,45,40,Yes,No,No,Yes,Yes,No,No,No,Yes,Low,Yes,,Yes,6,6,Low,Slow,Medium,60800,10,Tolerant,No,Yes,No,Yes,5.5,5.5,3.5,3.5,-23,-27,None,None,Routinely Available,High
ABGR,Abies grandis,No,Low,None,Late Spring,Low,High,Yes,Yes,No,Medium,No,Medium,Yes,High,,No,No,Green,Dense,Dense,Medium,60,52,No,Medium,Brown,No,Fall,No,Summer,Low,No,Conical,Single Stem,Spring and Summer,Moderate,Low,150,150,25,25,Yes,Long,Yes,Medium,No,None,Yes,No,Low,,,1200,1000,300,300,Yes,No,100,60,11,10,Yes,No,No,No,Yes,No,No,No,Yes,Low,Yes,,No,20,18,None,Slow,Low,23200,10,Tolerant,No,Yes,No,Yes,7.5,7.5,4.5,4.5,-33,-37,None,None,Field Collections Only,High... (2 MB left)
Expand
Plants_Carbon_Sequestration_Data.csv
2 MB
import pandas as pd
import requests
from pyowm import OWM  # OpenWeatherMap API wrapper
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
from vertexai.preview.prompts import Prompt
Expand
vertex_ai_prep_algo.py
10 KB
kayacancode — Today at 8:14 PM
too late i already transferred it voer
and thanks
Plu — Today at 10:00 PM
kaya
kayacancode — Today at 7:58 PM
u couldnt drag the python file
had to send a txt file
kayacancode — Today at 10:00 PM
hi
Plu — Today at 10:01 PM
change text 1 to this:
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

1. **Filter Plants:**  Review the provided `PlantsListBasedOnWeather` and cross-reference it with local regulations for the specified GPS location. Remove any invasive or prohibited plants from the list.

2. **Necessary Plant Quantity and Maturity:** Determine the number of filtered plants necessary plant and their maturity in order to sequester enough carbon to meet the value of `CarbonCreditsRequested` over the determined `TimeFrame`.
    * Quantity of plants must be able to successfully grow within `SizeOfLand` in acres. 
    * Please note 1 Carbon Credit is equivalent to 1 Ton of Carbon Sequestered. 
    * Also, prioritize younger plants although meeting the carbon credits is top priority.

3. **Carbon Sequestration Estimation:**
    * Calculate the total estimated carbon sequestered by the recommended plants over one year, assuming optimal planting and growth.
    * Estimate the current carbon sequestration of the area based on the provided information.

4. **Output:** Present your findings in the following format:

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
like the variable
kayacancode — Today at 10:01 PM
kk
Plu — Today at 10:01 PM
around line 118
kayacancode — Today at 10:01 PM
changed 🫡
do u want me to try again
Plu — Today at 10:02 PM
yeah
for me iowa still says pinus
but all others change accordingly
like they make sense
so maybe iowa somehow is pinus (although google saying otherwise)
kayacancode — Today at 10:03 PM
i get pinus as well
ok so we are just gonna say it works then..
let me try another coordinate
Plu — Today at 10:05 PM
i wonder if that is the only plant that can meet that desired output of carbon credits in that location for that size? 
kayacancode — Today at 10:05 PM
thats a good question
Plu — Today at 10:05 PM
I changed this slightly too
1. **Filter Plants:**  Review the provided `PlantsListBasedOnWeather` and cross-reference it with local regulations for the specified GPS location. Remove any invasive or prohibited plants from the list, and instead replace them with known plants that thrive and sequester the most carbon for the given area.
shit i aint a botanist
kayacancode — Today at 10:05 PM
LMAO
"refer to a botanist"
cooked
Plu — Today at 10:06 PM
when i saw that...
kayacancode — Today at 10:06 PM
LMAO
Plu — Today at 10:06 PM
kayacancode — Today at 10:06 PM
wait let me edit the land size and such with the new coordinates
no fr
Plu — Today at 10:06 PM
wallah i think we are good again
kayacancode — Today at 10:07 PM
LFG
Plu — Today at 10:07 PM
we good?
kayacancode — Today at 10:07 PM
i haven't tried yet
one sec
Plu — Today at 10:07 PM
kayacancode — Today at 10:07 PM
i still haven't even added in the new coordinates
LMAO
Image
this is the coordinates he gave me
does that look similar
Plu — Today at 10:11 PM
nearly identical
that small ass land
Plant | Quantity | Plant Maturity
------- | -------- | --------
Pinus strobus | 20 | Young (1-3 years old)
Quercus alba | 5  | Young (1-3 years old)
lfg
different
kayacancode — Today at 10:13 PM
u put in the new land size?
Plu — Today at 10:13 PM
Image
Image
Image
Image
Image
yes
kayacancode — Today at 10:13 PM
OKAYYYYY
PERIOD
ok bc i just ran it
Plu — Today at 10:13 PM
Image
me rn
kayacancode — Today at 10:13 PM
Image
LMAO
Plu — Today at 10:14 PM
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

# ---------- Combined Execution ----------
if __name__ == "__main__":
    # Insert your OpenWeatherMap API key here
    api_key = '067dd15b9d0807e3990e984320fc7a0b'

    # Step 1: Plant filtering
    plant_data = pd.read_csv('C:\\Users\\Anthony Banuelos\\Downloads\\Plants_Carbon_Sequestration_Data.csv')
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
... (14 lines left)
Collapse
message.txt
6 KB
do this for the variable of text1 to the end of file
﻿
Plu
misterplu
He/Him
 
 
 
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

# ---------- Combined Execution ----------
if __name__ == "__main__":
    # Insert your OpenWeatherMap API key here
    api_key = '067dd15b9d0807e3990e984320fc7a0b'

    # Step 1: Plant filtering
    plant_data = pd.read_csv('C:\\Users\\Anthony Banuelos\\Downloads\\Plants_Carbon_Sequestration_Data.csv')
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
