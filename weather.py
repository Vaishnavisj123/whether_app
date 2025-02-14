import streamlit as st
import requests

# OpenWeather API Key
API_KEY = "50850f5ebac83a8fa4bc923d9c0629d0"

# Function to fetch weather data
def get_weather(city):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "City": data["name"],
            "Temperature": f"{data['main']['temp']} °C",
            "Humidity": f"{data['main']['humidity']}%",
            "Weather": data["weather"][0]["description"].title(),
            "Wind Speed": f"{data['wind']['speed']} m/s"
        }
        return weather_info
    else:
        return None

# Streamlit UI
st.title("🌤️ Weather App")

# City input
city = st.text_input("Enter City Name", "New York")

if st.button("Get Weather"):
    weather = get_weather(city)
    
    if weather:
        st.write("### Weather Information")
        for key, value in weather.items():
            st.write(f"**{key}:** {value}")
    else:
        st.error("City not found. Please enter a valid city name.")
