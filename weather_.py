import streamlit as st
import requests
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

# OpenWeather API Key
API_KEY = "50850f5ebac83a8fa4bc923d9c0629d0"

# Function to fetch weather data
def get_weather(city):
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        forecast_list = data["list"]
        
        # Extracting required information for graphs
        dates = [entry["dt_txt"] for entry in forecast_list]
        temperatures = [entry["main"]["temp"] for entry in forecast_list]
        humidity = [entry["main"]["humidity"] for entry in forecast_list]
        wind_speed = [entry["wind"]["speed"] for entry in forecast_list]
        
        # Extracting min and max temperatures for each day
        df = pd.DataFrame({"Date": pd.to_datetime(dates), 
                           "Temperature": temperatures})
        df["Day"] = df["Date"].dt.date  # Extract only the date part
        daily_temps = df.groupby("Day")["Temperature"].agg(["min", "max"]).reset_index()

        weather_info = {
            "City": data["city"]["name"],
            "Temperature": temperatures[0],
            "Humidity": humidity[0],
            "Weather": forecast_list[0]["weather"][0]["description"].title(),
            "Wind Speed": wind_speed[0]
        }
        
        return weather_info, dates, temperatures, humidity, wind_speed, daily_temps
    else:
        return None, None, None, None, None, None

# Streamlit UI
st.title("🌤️ Weather App with Graphs")

# City input
city = st.text_input("Enter City Name", "New York")

if st.button("Get Weather"):
    weather, dates, temperatures, humidity, wind_speed, daily_temps = get_weather(city)
    
    if weather:
        st.write("### Current Weather Information")
        for key, value in weather.items():
            st.write(f"**{key}:** {value}")

        # Convert date strings to pandas datetime format
        df = pd.DataFrame({"Date": pd.to_datetime(dates), 
                           "Temperature (°C)": temperatures, 
                           "Humidity (%)": humidity, 
                           "Wind Speed (m/s)": wind_speed})

        # **📈 Temperature Trend (Line Chart)**
        st.write("### 📈 Temperature Trend")
        fig, ax = plt.subplots()
        ax.plot(df["Date"], df["Temperature (°C)"], marker="o", linestyle="-", color="red")
        ax.set_xlabel("Date")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title(f"Temperature Trend in {city}")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # **📊 Bar Chart for Min/Max Temperature**
        st.write("### 🌡️ Min/Max Temperature for Next 5 Days")
        fig_bar = px.bar(daily_temps, x="Day", y=["min", "max"], 
                         labels={"value": "Temperature (°C)", "variable": "Type"},
                         title="Daily Min/Max Temperature",
                         barmode="group", color_discrete_map={"min": "blue", "max": "red"})
        st.plotly_chart(fig_bar)

        # **💧 Humidity Graph**
        st.write("### 💧 Humidity Levels")
        fig_humidity = px.line(df, x="Date", y="Humidity (%)", markers=True, title="Humidity Levels Over Time")
        st.plotly_chart(fig_humidity)

        # **🌬️ Wind Speed Graph**
        st.write("### 🌬️ Wind Speed")
        fig_wind = px.line(df, x="Date", y="Wind Speed (m/s)", markers=True, title="Wind Speed Over Time")
        st.plotly_chart(fig_wind)

    else:
        st.error("City not found. Please enter a valid city name.")
