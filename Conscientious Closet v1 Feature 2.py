import os
import openai
import streamlit as st
from openai import OpenAI


st.markdown("# Prototype Feature 2: Suggestions Based on Weather")
st.sidebar.markdown("# Prototype Feature 2: Suggestions Based on Weather")

openai.api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI()


# create a wrapper function
def get_completion(prompt, model="gpt-3.5-turbo"):
   completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role":"system",
         "content": "Based on the location provided, display a weather forecast for today and the rest of the week and provide suggestions on clothing to wear based on today's weather. Make sure to warn the user not to go out if it's too late."},
        {"role": "user",
         "content": prompt},
        ]
    )
   return completion.choices[0].message.content

# create our streamlit app
with st.form(key = "chat"):
    prompt = st.text_input("What is your current location? (City, State)") 
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.write(get_completion(prompt))
