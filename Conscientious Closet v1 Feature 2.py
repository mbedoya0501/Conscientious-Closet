import streamlit as st
import requests

# Set the API key and base URL for OpenWeatherMap API
API_KEY = 'OpenWeatherAPI'  # Replace with your actual OpenWeatherMap API key
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Use Streamlit to create a text input for the city name
city = st.text_input('Enter a city and state (e.g., "Springfield, Illinois"):')

# If a city has been entered, fetch and display the weather data
if city:
    try:
        # Make a GET request to the OpenWeatherMap API
        response = requests.get(BASE_URL, params={'q': city, 'appid': API_KEY, 'units': 'imperial'})

        # If the city is not found, raise an exception
        if response.status_code == 404:
            raise ValueError("City not found. Please check the city and state spelling and try again.")

        # If the request was successful, display the weather data
        weather_data = response.json()

        # Get the temperature from the weather data and display it
        st.write(f'The current temperature in {city} is {weather_data["main"]["temp"]:.2f} degrees Fahrenheit.')
    except ValueError as ve:
        st.error(ve)
    except Exception as e:
        st.error(f"An error occurred: {e}")
