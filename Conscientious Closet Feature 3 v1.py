import streamlit as st 

with st.form(key = "chat"):
    st.title("Clothing Preferences")
    st.text_input("Hello welcome to contientious closet") # TODO!
    
    
    # Get user input for clothing styles
    clothing_styles = st.text_input("Enter your favorite clothing styles (separated by commas):")
    
    # Get user input for favorite colors
    favorite_colors = st.text_input("Enter your favorite colors (separated by commas):")
    
    # Get user input for favorite articles of clothing
    articles_of_clothing = st.text_input("Enter your favorite articles of clothing (separated by commas):")
    
    # Display user input
    if st.button("Submit"):
        st.write("Your favorite clothing styles:", clothing_styles)
        st.write("Your favorite colors:", favorite_colors)
        st.write("Your favorite articles of clothing:", articles_of_clothing)

    
    submitted = st.form_submit_button("Submit")

