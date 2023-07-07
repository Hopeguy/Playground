import streamlit as st
import requests

def get_stockholm_temperature():
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": "Stockholm",
        "appid": "9cb45218b85f9b65bdec634d9872a67e",  # Replace with your OpenWeatherMap API key
        "units": "metric"
    }
    response = requests.get(url, params=params)
    data = response.json()
    temperature = data["main"]["temp"]
    return temperature

def main():
    temperature = get_stockholm_temperature()
    st.write("Temperature in Stockholm: ", temperature)

if __name__ == '__main__':
    main()
