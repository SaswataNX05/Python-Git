import requests


def get_coordinate(cityname: str):

    url = "https://geocoding-api.open-meteo.com/v1/search"

    try:
        parameter = {"name" : cityname, "count": 1, "language" : "en", "format" : "json"}
        responce = requests.get(url, params = parameter, timeout=5)
        responce.raise_for_status()
        data = responce.json()

        if "results" in data and len(data["results"])>0:
            top = data["results"][0]
            latitude = top["latitude"]
            longitude = top["longitude"]
            country = top["country"]
            return latitude, longitude, country
        else :
            print(f"[!] City {cityname} not Found...")
            exit(-1)


    except requests.exceptions.HTTPError as http:
        print(f"[!] HTTP ERROR Ocurrs.. : {http}")
    except requests.exceptions.ConnectionError:
        print("[!] Network Error: Unable to connect the server..!")
    except requests.exceptions.Timeout:
        print("[!] Request time out after 5 second..!")
    except requests.exceptions.RequestException as err:
        print(f"[!] An unexpected Error Ocured: {err}")


def get_weather(code):

    WMO_WEATHER_CODES = {
    0:  ("Clear sky", "☀️"),
    1:  ("Mainly clear", "🌤️"),
    2:  ("Partly cloudy", "⛅"),
    3:  ("Overcast", "☁️"),
    45: ("Fog", "🌫️"),
    48: ("Depositing rime fog", "🌫️"),
    51: ("Light drizzle", "🌦️"),
    53: ("Moderate drizzle", "🌦️"),
    55: ("Dense drizzle", "🌧️"),
    56: ("Light freezing drizzle", "🌨️"),
    57: ("Dense freezing drizzle", "🌨️"),
    61: ("Slight rain", "🌦️"),
    63: ("Moderate rain", "🌧️"),
    65: ("Heavy rain", "🌧️"),
    66: ("Light freezing rain", "🌨️"),
    67: ("Heavy freezing rain", "🌨️"),
    71: ("Slight snow fall", "🌨️"),
    73: ("Moderate snow fall", "❄️"),
    75: ("Heavy snow fall", "❄️"),
    77: ("Snow grains", "❄️"),
    80: ("Slight rain showers", "🌦️"),
    81: ("Moderate rain showers", "🌧️"),
    82: ("Violent rain showers", "⛈️"),
    85: ("Slight snow showers", "🌨️"),
    86: ("Heavy snow showers", "❄️"),
    95: ("Thunderstorm", "⚡"),
    96: ("Thunderstorm with slight hail", "⛈️"),
    99: ("Thunderstorm with heavy hail", "⛈️"),
    }

    return WMO_WEATHER_CODES.get(code, ("Unkown Weather", ""))

def fetch_weather(coordinate, cityname):

    lat = coordinate[0]
    lon = coordinate[1]

    url = "https://api.open-meteo.com/v1/forecast"

    try:

        parameter = {"latitude" : lat, "longitude" : lon, "current" : ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "weather_code", "wind_speed_10m"]}
        responce = requests.get(url, params=parameter, timeout=5)
        responce.raise_for_status()
        data = responce.json()

        weather_code = data["current"]["weather_code"]
        temp = data["current"]["temperature_2m"]
        humidity = data["current"]["relative_humidity_2m"]
        feelslike = data["current"]["apparent_temperature"]
        wind = data["current"]["wind_speed_10m"]

        temp_unit = data["current_units"]["temperature_2m"]
        speed_unit = data["current_units"]["wind_speed_10m"]

        weather_type, imoji = get_weather(int(weather_code))

        print(f"----WEATHER IN {cityname}, {coordinate[2]} ----\n")
        print(f"Condition:    {weather_type} {imoji}")
        print(f"Temperature:  {temp}{temp_unit} (Feels like {feelslike}{temp_unit})")
        print(f"Humidity:     {humidity}%")
        print(f"Wind Speed:   {wind}{speed_unit}")
        print("\n---------------------------------------------\n")


    except requests.exceptions.HTTPError as http:
        print(f"[!] HTTP ERROR Ocurrs.. : {http}")
    except requests.exceptions.ConnectionError:
        print("[!] Network Error: Unable to connect the server..!")
    except requests.exceptions.Timeout:
        print("[!] Request time out after 5 second..!")
    except requests.exceptions.RequestException as err:
        print(f"[!] An unexpected Error Ocured: {err}")




def main():
    print("==================================================")
    print("            CLI WEATHER APLICATION                ")
    print("==================================================")

    cityname = input("Enter the city name: ")
    print(f"\n[+] Fetching Weather Data for {cityname}...\n")
    lst = get_coordinate(cityname)
    fetch_weather(lst, cityname)

if __name__ == "__main__":
    main()
