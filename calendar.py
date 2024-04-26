import streamlit as st
import datetime
import calendar

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

# Display the dates in a markdown text box in each column
for i, date in enumerate(dates):
    cols[i].markdown(f"```\n{calendar.day_name[date.weekday()]}: {date.month}/{date.day}/{date.year}\n```")
