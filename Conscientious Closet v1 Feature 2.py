import streamlit as st
import requests

# Set the API key and base URL for OpenWeatherMap API
API_KEY = '36407eb7cff8c8ca66f775827ec2e84c'  # Replace with your actual OpenWeatherMap API key
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Use Streamlit to create a text input for the city name
city = st.text_input('Enter a city:')

# If a city has been entered, fetch and display the weather data
if city:
    try:
        # Make a GET request to the OpenWeatherMap API
        response = requests.get(BASE_URL, params={'q': city, 'appid': API_KEY, 'units': 'imperial'})

        # If the request was successful, display the weather data
        response.raise_for_status()
        weather_data = response.json()

        # Get the temperature from the weather data
        temperature = weather_data['main']['temp']

        # Use Streamlit to display the temperature
        st.write(f'The current temperature in {city} is {temperature:.2f} degrees Fahrenheit.')
    except requests.exceptions.HTTPError as errh:
        st.write(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        st.write(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        st.write(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        st.write(f"Something went wrong: {err}")
