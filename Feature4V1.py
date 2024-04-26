import streamlit as st
import pandas as pd
import requests
import openai

# Ensure you replace 'your_openai_api_key_here' and 'your_openweather_api_key_here' with your actual API keys
OPENAI_API_KEY = 'your-api-key-here'
OPENWEATHER_API_KEY = 'your-weather-api-key-here'  
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Initialize OpenAI API key
openai.api_key = OPENAI_API_KEY

def get_outfit_suggestion(weather):
    """Generate an outfit suggestion based on the weather using GPT-4."""
    response = openai.Completion.create(
        model="gpt-4",
        prompt=f"Suggest an outfit for a {weather.lower()} day:",
        max_tokens=60
    )
    return response.choices[0].text.strip()

def get_weather(city):
    """Fetch the current weather for a specified city."""
    response = requests.get(BASE_URL, params={'q': city, 'appid': OPENWEATHER_API_KEY, 'units': 'imperial'})
    if response.status_code != 200:
        response.raise_for_status()  # This will raise an HTTPError for bad responses
    return response.json()

def main():
    st.title('Outfit Planning and Weather App')

    city = st.text_input('Enter a city and state (e.g., "Springfield, Illinois"):')
    if city:
        try:
            weather_data = get_weather(city)
            weather_description = weather_data["weather"][0]["description"]
            st.write(f'The current temperature in {city} is {weather_data["main"]["temp"]:.2f} degrees Fahrenheit with {weather_description}.')
        except requests.exceptions.HTTPError as e:
            st.error(f"An error occurred: {e}")
            return  # Exit the function if there's an error
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
            return  # Exit the function on other errors

    if city and 'weather_description' in locals():
        with st.form("outfit_planner"):
            date = st.date_input("Choose a date for your outfit plan:")
            suggestion = get_outfit_suggestion(weather_description) if 'Get Outfit Suggestion' in st.session_state else ""
            outfit = st.text_input("Describe your outfit for the day:", value=suggestion)
            submitted = st.form_submit_button("Submit Outfit Plan")
            if submitted:
                if 'outfits' not in st.session_state:
                    st.session_state['outfits'] = pd.DataFrame(columns=['Date', 'City', 'Weather', 'Outfit'])
                new_data = pd.DataFrame([[date, city, weather_description, outfit]], columns=['Date', 'City', 'Weather', 'Outfit'])
                st.session_state['outfits'] = pd.concat([st.session_state['outfits'], new_data], ignore_index=True)

        if 'outfits' in st.session_state and not st.session_state['outfits'].empty:
            st.write("Your Outfit Plans:")
            st.table(st.session_state['outfits'].sort_values(by='Date'))

if __name__ == "__main__":
    main()
