import streamlit as st
import pandas as pd
import requests
import openai

# Ensure you replace these with your actual API keys
OPENAI_API_KEY = 'your-api-key-here'
OPENWEATHER_API_KEY = 'weather-api-key-here'
FORECAST_URL = 'http://api.openweathermap.org/data/2.5/forecast'  # Forecast endpoint

# Initialize OpenAI API key
openai.api_key = OPENAI_API_KEY

def get_outfit_suggestion(weather):
    """Generate an outfit suggestion based on the weather using GPT-3.5."""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Ensure this model is available in your API plan
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Suggest an outfit for a {weather.lower()} day:"}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

def get_weather(city, date):
    """Fetch the forecasted weather for a specified city and date."""
    response = requests.get(FORECAST_URL, params={'q': city, 'appid': OPENWEATHER_API_KEY, 'units': 'imperial'})
    if response.status_code != 200:
        response.raise_for_status()  # This will raise an HTTPError for bad responses

    data = response.json()
    for item in data['list']:
        if item['dt_txt'].startswith(date.strftime('%Y-%m-%d')):
            return item['weather'][0]['description'], item['main']['temp']
    return "clear sky", 70  # Default weather if no exact match found

def main():
    st.title('Outfit Planning and Weather App')

    city = st.text_input('Enter a city and state (e.g., "Springfield, Illinois"):')
    date = st.date_input("Choose a date for your outfit plan:")

    if city and date:
        try:
            weather_description, temperature = get_weather(city, date)
            st.write(f"The forecasted temperature in {city} on {date} is {temperature:.2f} degrees Fahrenheit with {weather_description}.")
            suggestion_button = st.button("Get Outfit Suggestion")
            if suggestion_button:
                suggestion = get_outfit_suggestion(weather_description)
                st.session_state['suggestion'] = suggestion
                st.write(f"Suggested Outfit: {suggestion}")
        except requests.exceptions.HTTPError as e:
            st.error(f"An error occurred: {e}")
            return  # Exit the function if there's an error
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
            return  # Exit the function on other errors

    if city and 'weather_description' in locals():
        with st.form("outfit_planner"):
            outfit = st.text_input("Describe your outfit for the day:", value=st.session_state.get('suggestion', ''))
            submitted = st.form_submit_button("Submit Outfit Plan")
            if submitted:
                if 'outfits' not in st.session_state:
                    st.session_state['outfits'] = pd.DataFrame(columns=['Date', 'City', 'Weather', 'Temperature', 'Outfit'])
                new_data = pd.DataFrame([[date, city, weather_description, temperature, outfit]], columns=['Date', 'City', 'Weather', 'Temperature', 'Outfit'])
                st.session_state['outfits'] = pd.concat([st.session_state['outfits'], new_data], ignore_index=True)

        if 'outfits' in st.session_state and not st.session_state['outfits'].empty:
            st.write("Your Outfit Plans:")
            st.table(st.session_state['outfits'].sort_values(by='Date'))

if __name__ == "__main__":
    main()
