import streamlit as st
import requests
from openai import OpenAI
client = OpenAI()


# Set the API key and base URL for OpenWeatherMap API
API_KEY = '36407eb7cff8c8ca66f775827ec2e84c'  # Replace with your actual OpenWeatherMap API key
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

st.markdown("# Prototype Feature 2: Suggestions Based on Weather")
st.sidebar.markdown("# Prototype Feature 2: Suggestions Based on Weather")

# Use Streamlit to create a text input for the city name
city = st.text_input('Enter a city and state (e.g., "Springfield, Illinois"):')

def get_completion(prompt, model="gpt-3.5-turbo"):
   completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role":"system",
         "content": "Based on the data provided, give suggestions on clothing to wear based on today's weather. Make sure to warn the user not to go out if it's too late."},
        {"role": "user",
         "content": prompt},
        ]
    )
   return completion.choices[0].message.content

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
        st.write(get_completion(str(weather_data)))
    except ValueError as ve:
        st.error(ve)
    except Exception as e:
        st.error(f"An error occurred: {e}")
