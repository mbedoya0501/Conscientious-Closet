import streamlit as st
import openai
from datetime import datetime

# Set up OpenAI API key
openai.api_key = "OPENAI_API_KEY"

def classify_clothes_age(purchase_date):
    # Convert purchase_date to datetime object
    purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d")
    
    # Calculate the difference between the purchase date and today's date
    delta = datetime.now() - purchase_date
    
    # Define age categories
    if delta.days <= 30:  # Less than or equal to 30 days old
        return 'New'
    elif delta.days <= 90:  # Less than or equal to 90 days old
        return 'Fairly New'
    elif delta.days <= 365:  # Less than or equal to 1 year old
        return 'Old'
    else:  # More than 1 year old
        return 'Very Old'

def main():
    st.title("Clothes Age Classifier")
    
    # Collect user input
    purchase_date = st.date_input("Enter the date of clothes purchase:")
    
    if st.button("Classify"):
        # Classify the age of clothes
        classification = classify_clothes_age(str(purchase_date))
        
        # Display classification result
        st.write(f"The clothes are classified as: {classification}")

if __name__ == "__main__":
    main()
