import streamlit as st
import datetime
import calendar
import requests

st.set_page_config(layout='wide')

# Your OpenWeather API key
api_key = "API HERE"

# Let the user input a city
city = st.text_input('Enter a city:')

# Calculate the start date of the first week of the year
start_date = datetime.date(datetime.date.today().year, 1, 1) - datetime.timedelta(days=datetime.date(datetime.date.today().year, 1, 1).weekday())

# Generate a list of weeks for the dropdown
weeks = [f"{start_date + datetime.timedelta(weeks=i)} - {start_date + datetime.timedelta(weeks=i, days=6)}" for i in range(52)]

# Let the user select a week
selected_week = st.selectbox('Select a week:', weeks)

# Calculate the start date of the selected week
start_date = datetime.datetime.strptime(selected_week.split(' ')[0], '%Y-%m-%d').date()

# Generate the dates for the selected week
dates = [start_date + datetime.timedelta(days=i) for i in range(7)]

st.title(f'Calendar for {selected_week}')

# Create 7 columns
cols = st.columns(7)

# Make a request to the OpenWeather API for the 5-day forecast
response = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}")

# Check if the 'list' key exists in the response
if 'list' in response.json():
    # Loop through the forecast data
    for i in range(7):
        # Check if the index exists in the list
        if i < len(response.json()['list']):
            # Convert the temperature to Fahrenheit and round it to 2 decimal places
            temperature = round(response.json()['list'][i]['main']['temp'] * 9/5 - 459.67, 2)

            # Display the date and the temperature in a markdown text box
            cols[i].markdown(f"```\n{calendar.day_name[dates[i].weekday()]}: {dates[i].month}/{dates[i].day}/{dates[i].year}\nTemperature: {temperature}°F\n```")
        else:
            cols[i].markdown(f"```\n{calendar.day_name[dates[i].weekday()]}: {dates[i].month}/{dates[i].day}/{dates[i].year}\nTemperature: No data available\n```")
else:
    st.write("Error retrieving weather data")

def get_clothing_suggestion(temperature):
    if temperature < 32:
        return "It's freezing outside, wear a heavy coat, hat, gloves, and scarf."
    elif temperature < 60:
        return "It's quite chilly, wear a jacket and long pants."
    elif temperature < 70:
        return "It's a bit cool, a sweater and jeans should be fine."
    elif temperature < 80:
        return "It's warm, wear a t-shirt and shorts."
    else:
        return "It's hot, wear light clothing and don't forget sunscreen."

# ...

for i in range(7):
    # Check if the index exists in the list
    if i < len(response.json()['list']):
        # Convert the temperature to Fahrenheit and round it to 2 decimal places
        temperature = round(response.json()['list'][i]['main']['temp'] * 9/5 - 459.67, 2)

        # Display the date and the temperature in a markdown text box
        cols[i].markdown(f"```\n{calendar.day_name[dates[i].weekday()]}: {dates[i].month}/{dates[i].day}/{dates[i].year}\nTemperature: {temperature}°F\n```")
    else:
        cols[i].markdown(f"```\n{calendar.day_name[dates[i].weekday()]}: {dates[i].month}/{dates[i].day}/{dates[i].year}\nTemperature: No data available\n```")

# Ask the user which day they would like to get a clothing suggestion for
selected_day = st.selectbox('Select a day to get a clothing suggestion:', [calendar.day_name[dates[i].weekday()] for i in range(7)])

# Find the index of the selected day
selected_day_index = [calendar.day_name[dates[i].weekday()] for i in range(7)].index(selected_day)

# Check if the index exists in the list
if selected_day_index < len(response.json()['list']):
    # Convert the temperature to Fahrenheit and round it to 2 decimal places
    temperature = round(response.json()['list'][selected_day_index]['main']['temp'] * 9/5 - 459.67, 2)

    # Get a clothing suggestion based on the temperature
    clothing_suggestion = get_clothing_suggestion(temperature)

    # Display the clothing suggestion
    st.write(f"For {selected_day}, {clothing_suggestion}")
else:
    st.write("No data available for the selected day")
