import openai
import streamlit as st
from datetime import datetime

# Set up OpenAI API key
openai.api_key = "your_api_key"

def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

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
        
        # Generate prompt for GPT-3
        prompt = f"My clothing is classified as {classification}. What should I do with it?"
        
        # Get suggestion from GPT-3
        suggestion = chat_with_gpt(prompt)
        
        # Display classification result and suggestion
        st.write(f"The clothes are classified as: {classification}")
        st.write(f"Suggestion: {suggestion}")

if __name__ == "__main__":
    main()
