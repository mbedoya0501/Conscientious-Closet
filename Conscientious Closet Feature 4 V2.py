import streamlit as st
import openai
from datetime import datetime, timedelta

# Set your OpenAI API key
openai.api_key = "Open_AI_Key_Here"

def classify_clothing_purchase(purchase_date):
    current_date = datetime.now().date()
    threshold_date = current_date - timedelta(days=3*30)  # Three months ago

    if purchase_date < threshold_date:
        return "Old"
    else:
        return "Not old"

def generate_response(classification):
    prompt = f"What’s in this image? This clothing item is classified as: {classification}"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50
    )
    return response.choices[0].text.strip()

def main():
    st.title("Clothing Item Classifier")

    # User input for purchase date
    purchase_date = st.date_input("Enter the purchase date of the clothing item:")
    
    if st.button("Classify"):
        classification = classify_clothing_purchase(purchase_date)
        response = generate_response(classification)
        st.write(f"The clothing item is classified as: {classification}")
        st.write("OpenAI Response:")
        st.write(response)

if __name__ == "__main__":
    main()
    
