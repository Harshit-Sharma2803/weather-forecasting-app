import requests
from plyer import notification

# ==========================================
# WEATHER FORECASTING PROJECT
# Basic Weather + Desktop Notification
# ==========================================

# Step 1: Take city name from user
city = input("Enter city name: ")

# ==========================================
# STEP 2: GET COORDINATES FROM CITY NAME
# ==========================================

def get_coordinates(city):
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    try:
        geo_res = requests.get(geo_url, params=geo_params, timeout=10).json()

    except requests.exceptions.RequestException:
        print("❌ Unable to connect to the internet.")
        exit()

    # Check if city was found
    if "results" not in geo_res:
        print("City not found!")
        exit()

    # Get latitude and longitude
    lat = geo_res["results"][0]["latitude"]
    lon = geo_res["results"][0]["longitude"]

    return lat, lon

lat, lon = get_coordinates(city)



# ==========================================
# STEP 3: GET WEATHER DATA
# ==========================================
def get_weather_data(lat, lon):
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "weather_code",
            "cloud_cover",
            "wind_speed_10m"
        ],
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "weather_code"
        ],
        "forecast_days": 7
    }

    try:
        weather_res = requests.get(weather_url, params=weather_params, timeout=10).json()

    except requests.exceptions.RequestException:
        print("❌ Unable to connect to the internet.")
        exit()

    return weather_res

weather_res = get_weather_data(lat, lon)


# Get current weather
current = weather_res["current"]
#Get daily weather
daily = weather_res["daily"]

# print("Daily Weather Code:",daily["weather_code"])

def get_weather_condition(code):

    if code == 0:
        return "☀️ Clear Sky"

    elif code in [1, 2, 3]:
        return "⛅ Cloudy"

    elif code in [51, 53, 55, 56, 57]:
        return "🌦️ Drizzle"

    elif code in [61, 63, 65, 66, 67]:
        return "🌧️ Rain"

    elif code in [71, 73, 75, 77]:
        return "❄️ Snow"

    elif code in [95, 96, 99]:
        return "⛈️ Thunderstorm"

    else:
        return "❓ Unknown"




#Get Weather Code
weather_code = current["weather_code"]

#get weather condition
condition = get_weather_condition(weather_code)




# ==========================================
# STEP 4: DISPLAY WEATHER IN TERMINAL
# ==========================================

def display_weather(city,current,condition):
    print("\n================================")
    print("       CURRENT WEATHER")
    print("================================")

    print("City:", city)
    print("Temperature:", current["temperature_2m"], "°C")
    print("Feels Like:", current["apparent_temperature"], "°C")
    print("Humidity:", current["relative_humidity_2m"], "%")
    print("Rain:", current["precipitation"], "mm")
    print("Cloud Cover:", current["cloud_cover"], "%")
    print("Wind Speed:", current["wind_speed_10m"], "km/h")
    print("Weather Condition:", condition)

    print("================================")

    print("\n===== 7-DAY FORECAST =====")

    for i in range(7):
        daily_code = daily["weather_code"][i]

        condition = get_weather_condition(daily_code)

        print(
            daily["time"][i],
            "|",
            condition,
            "| Max:",
            daily["temperature_2m_max"][i],
            "°C | Min:",
            daily["temperature_2m_min"][i],
            "°C"
        )

display_weather(city, current, condition)



# ==========================================
# STEP 5: DESKTOP NOTIFICATION
# ==========================================
 

def send_notification(city, current, condition):
    notification.notify(
        title="🌤️ Weather Update",
        message=(
            f"{city}\n"
            f"Temperature: {current['temperature_2m']}°C\n"
            f"Feels Like: {current['apparent_temperature']}°C\n"
            f"Humidity: {current['relative_humidity_2m']}%\n"
            f"Condition: {condition}\n"
        ),
        timeout=5
    )

send_notification(city, current, condition)

