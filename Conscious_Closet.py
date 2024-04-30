import streamlit as st
import torch
import clip
from PIL import Image
from torchvision.transforms import Compose, Resize, CenterCrop, ToTensor
import openai
import os
import requests
import folium
import pandas as pd
from streamlit_folium import folium_static
from googleplaces import GooglePlaces, types
from openai import OpenAI
import datetime
client = OpenAI()

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
background: linear-gradient(12deg, rgba(9,17,11,1) 0%, rgba(25,45,30,1) 44%, rgba(58,96,64,1) 100%)
}
"""

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load('ViT-B/32', device=device)

PLACES_API_KEY = 'AIzaSyA61n7kgs23ROpA0vZZrJqUcoR52BXQa0o'
google_places = GooglePlaces(PLACES_API_KEY)
API_KEY = '36407eb7cff8c8ca66f775827ec2e84c'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'
FORECAST_URL = 'http://api.openweathermap.org/data/2.5/forecast'
openai.api_key = os.environ["OPENAI_API_KEY"]

im = Image.open('Logov3.png')
st.set_page_config(page_title = "Conscious Closet", page_icon = im, layout="wide")

st.sidebar.image(im, width=120)
st.sidebar.title("Conscious Closet")

st.markdown(page_bg_img, unsafe_allow_html=True)
st.title("Welcome to your Conscious Closet!", anchor=None)
st.markdown('Sustainable Fashion at your Fingertips')

preprocess = Compose([
    Resize(256, interpolation=Image.BICUBIC),
    CenterCrop(224),
    ToTensor()
])

@st.experimental_fragment
def get_completion(prompt, model="gpt-3.5-turbo"): 
    completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role":"system",
         "content": "Based on the result provided, list suggestions on brands that have are eco-friendly and promote \
                     carbon footprint awareness."},
        {"role": "user",
         "content": prompt},
        ]
    )
    return completion.choices[0].message.content

@st.cache_resource
def get_weather_completion(prompt, model="gpt-3.5-turbo"):
   completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role":"system",
         "content": "Based on the data provided, give numerous and slightly detailed suggestions on clothing to wear based on today's weather \
                     as a bullet-pointed list. Take note of any weather such as rain, snow, or extreme heat."},
        {"role": "user",
         "content": prompt},
        ]
    )
   return completion.choices[0].message.content

@st.experimental_fragment
def get_weather_completion_forecast(prompt, model="gpt-3.5-turbo"):
   completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role":"system",
         "content": "Based on the data provided, give numerous and slightly detailed suggestions on clothing to wear based on today's weather \
                     as a bullet-pointed list. Take note of any weather such as rain, snow, or extreme heat."},
        {"role": "user",
         "content": prompt},
        ]
    )
   return completion.choices[0].message.content

@st.cache_resource
def weather_info_summarizer(prompt, model = "gpt-3.5-turbo"):
    completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role":"system",
         "content": "Using this list, list out how hot or cold it is, then specifically ONLY what clothing suggestions the model says briefly and nothing more. \
                     Be very short and very brief, and make sure to separate with commas followed by a space."},
        {"role": "user",
         "content": prompt},
        ]
    )
    return completion.choices[0].message.content

@st.experimental_fragment
def get_tips_completion(prompt, model="gpt-3.5-turbo"):
   completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role":"system",
         "content": "Give 3 suggestions / tips as a brief list, one sentence each, each beginning with 🌿, line break each sentence"},
        {"role": "user",
         "content": prompt},
        ]
    )
   return completion.choices[0].message.content

@st.experimental_fragment
def weather_suggestions():
    city = st.session_state.city
    if city:
        try:
            response = requests.get(BASE_URL, params={'q': city, 'appid': API_KEY, 'units': 'imperial'})        
            if response.status_code == 404:
                raise ValueError("City / State not found. Please check the city and state spelling and try again.")
            weather_data = response.json()
            st.text("")
            st.write(f'The current temperature in **{city}** is {weather_data["main"]["temp"]:.2f}° Fahrenheit. ({weather_data["weather"][0]["description"]})')
            completion = get_weather_completion(str(weather_data))
            st.write(completion)
        except ValueError as ve:
            st.error(ve)
        except Exception as e:
            st.error(f"An error occurred: {e}")

@st.experimental_fragment
def get_weather_forecast(city, day):
    response = requests.get(FORECAST_URL, params={'q': city, 'appid': API_KEY, 'units': 'imperial'})        
    if response.status_code != 200:
        response.raise_for_status()
    weather_data = response.json()
    for item in weather_data['list']:
        if item['dt_txt'].startswith(day.strftime('%Y-%m-%d')):
            return item['weather'][0]['description'], item['main']['temp']
    return "clear sky", 70

@st.experimental_fragment
def outfit_planner():
    st.write("_Planning your outfit for a future day? Organize your plan here!_")
    col1, col2 = st.columns([0.5, 0.5], gap="medium")
    with col1:
        day = st.date_input('Select a date to plan your outfit:', min_value=datetime.date.today(), format="MM-DD-YYYY")
    with col2:
        cityplan = st.text_input("Enter a city and state / province / country:", value = city)

    if cityplan and day:
        try:
            weather_description, temperature = get_weather_forecast(cityplan, day)
            st.write(f"The forecasted temperature in {cityplan} on {day.strftime('%m-%d-%Y')} is around {temperature:.2f}° Fahrenheit ({weather_description}).")
            suggestion_button = st.button("Get Outfit Suggestions")
            if suggestion_button:
                suggestion = get_weather_completion_forecast(str(get_weather_forecast(city, day)))
                st.session_state['suggestion'] = suggestion
                st.write(f"Suggestions for your outfit on {day}: \n {suggestion}")
                completion = weather_info_summarizer(suggestion)
                if 'weather' not in st.session_state or st.session_state['weather'] is None:
                    st.session_state['weather'] = completion
                else:
                    st.session_state['weather'] = completion

        except requests.exceptions.HTTPError as e:
            st.error(f"An error occurred: {e}")
            return
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            return
    
    if 'weather_description' in locals():
        with st.form("outfit_planner"):
            outfit = st.text_input(f"Describe your outfit ({day.strftime('%m-%d-%Y')})", value = st.session_state.get('weather', ''))
            submitted = st.form_submit_button("Submit Notes")

            if submitted:
                if 'outfits' not in st.session_state:
                    st.session_state['outfits'] = pd.DataFrame(columns=['Date', 'City', 'Weather', 'Temperature', 'Notes'])
                new_data = pd.DataFrame([[day, cityplan, weather_description, temperature, outfit]], columns=['Date', 'City', 'Weather', 'Temperature', 'Notes'])
                st.session_state['outfits'] = pd.concat([st.session_state['outfits'], new_data])
            
            if 'outfits' in st.session_state and not st.session_state['outfits'].empty:
                st.write("Your planned outfits:")
                st.table(st.session_state['outfits'].sort_values(by='Date', ascending=True, ignore_index=True))

@st.experimental_fragment
def upcycling_tips():
    with st.container(border=True):
        st.write("""
            <style>
                div[data-testid="stVerticalBlockBorderWrapper"]:has(
                >div>div>div[data-testid="element-container"] 
                .beige-frame
                ) {
                    text-align: center;
                    background: linear-gradient(12deg, rgba(152,135,123,1) 0%, rgba(217,182,162,1) 44%, rgba(225,201,183,1) 100%);
                    border-color: #FFFFFF;
                    border-radius: 18px; 
                    color: #44332D;
                }
                .stApp a:first-child {
                    display: none;
                }
                .css-15zrgzn {display: none}
                .css-eczf16 {display: none}
                .css-jn99sy {display: none}
            </style>
            <span class="beige-frame"/>
            <h1 style="color: #44332D;"
                    <b>Upcycling Tips🌿</b>
            </h1>
            """, unsafe_allow_html=True)
        completion = get_tips_completion("Upcycling")
        st.write(f"{completion: <20}")
        st.button("Refresh Tips", type="primary")

@st.experimental_fragment
def map_location():
    if city:
        try:
            response = requests.get(BASE_URL, params={'q': city, 'appid': API_KEY, 'units': 'imperial'})        
            if response.status_code == 404:
                raise ValueError("City / State not found. Please check the city and state spelling and try again.")
            weather_data = response.json()
            map = folium.Map(location=[weather_data["coord"]["lat"], weather_data["coord"]["lon"]], tiles = "cartodb positron", zoom_start = 13)

            query_result = google_places.nearby_search(
            location = city, keyword = 'Thrift Store',
            radius = 10000, types=[types.TYPE_CLOTHING_STORE])

            for place in query_result.places:
                place.get_details()
                store = (place.geo_location['lat'], place.geo_location['lng'])
                folium.Marker(store, popup = folium.Popup(f"<strong>{place.name}</strong> ({str(place.rating)}⭐) <br><br>{place.formatted_address}",\
                              max_width = 100), icon = folium.Icon(color = 'darkgreen', icon_color = 'beige', icon = "shirt", prefix = 'fa')).add_to(map)
                
            folium_static(map, width = 800, height = 550)

        except ValueError as ve:
            st.error(ve)
        except Exception as e:
            st.error(f"An error occurred: {e}")

@st.experimental_fragment
def clothing_suggestions():
    uploaded_file = st.file_uploader("Take a photo of an article of clothing to be provided with brand suggestions:", type="jpg")
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', width = 350)
        st.write("")

        image = preprocess(image).unsqueeze(0).to(device)
        labels = ["crewneck", "hoodie", "cargo pants", "shirt", "shoes", "shorts", "sneakers", "sweater", "t-shirt", "jeans", "dress", "skirt", "N/A"]

        num_labels = min(len(labels), 1000) 
        text = clip.tokenize(labels[:num_labels]).to(device)

        with torch.no_grad():
            image_features = model.encode_image(image)
            text_features = model.encode_text(text)

            similarity = torch.nn.functional.cosine_similarity(image_features, text_features, dim=-1)
            values, indices = similarity.topk(1)
            values *= 100

        st.write("This article of clothing is detected as:")
        for value, index in zip(values, indices):
            st.write(f"**{labels[index]}**")

        with st.expander("See brand suggestions"):
            if labels[index] != "N/A":
                completion = get_completion(labels[index])
                st.write(completion)
            else:
                st.write("The uploaded image does not seem to contain any clothing. Please try again.")
            st.button("Refresh", type="secondary")

city = "San Francisco, California"
if 'city' not in st.session_state:
    st.session_state['city'] = city

with st.sidebar:
    with st.popover("Your Location 📍"):
        st.text_input("Enter a city and state / province / country (e.g., 'Springfield, Illinois'):", key = "city")
        city = st.session_state.city
    st.write("📍 ", f"**{city}**")
    st.text("")
    st.text("")
    st.sidebar.success('_"Buy less, choose well, make it last." - Vivienne Westwood_')

tab1, tab2, tab3 = st.tabs(["Weather", "Stores Near Me", "Clothing Suggestions"])

with tab1:
    st.write("📍 ", f"**{st.session_state.city}**")
    col1, col2, col3, col4 = st.columns([0.5, 0.05, 0.4, 0.05], gap = "small")
    with col1:
        weather_suggestions()
    with col3:
        upcycling_tips()
    st.write("--------------------------------")
    st.write("👕 **Outfit Planner**")
    outfit_planner()

with tab2:
    st.write("📍 ", f"**{city}**")
    st.write("Here are the nearest thrift stores near your location:")
    map_location()

with tab3: 
    clothing_suggestions()