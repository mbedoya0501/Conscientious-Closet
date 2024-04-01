import os
import openai
import streamlit as st
from openai import OpenAI

st.markdown("# Prototype Feature 3: Clothing Sizing")
st.sidebar.markdown("# Prototype Feature 3: Clothing Sizing")
shoe_size=""
shirt_size=""
pants_size=""

with st.form(key = "chat"):
    prompt = st.text_input("What is your shoe size? ") 
    prompt2 = st.text_input("What is your shirt size?" )
    prompt3 = st.text_input("What is your pants size? ") 
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        shoe_size = prompt
        shirt_size = prompt2
        pants_size = prompt3
        st.write(f"Your shoe size is: **{shoe_size}**")
        st.write(f"Your shirt size is: **{shirt_size}**")
        st.write(f"Your pants size is: **{pants_size}**")

