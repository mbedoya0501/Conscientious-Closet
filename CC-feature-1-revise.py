# Import necessary libraries
import streamlit as st
import requests
import base64
import os
from PIL import Image
api_key = os.environ["OPENAI_API_KEY"]

# Function to encode image to base64
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# OpenAI API Headers
headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

# OpenAI API Payload
payload = {
  "model": "gpt-4-vision-preview",
  "max_tokens": 50,  # Limit the response to 50 tokens
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "give me the type of clothing and color of the item in the image."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": ""
          }
        }
      ]
    }
  ]
}

# Streamlit code
st.title('Clothing Item Description')

uploaded_file = st.file_uploader("Choose an image...", type="jpg")

if uploaded_file is not None:
    # Convert the file to an image
    image = Image.open(uploaded_file)

    # Create a temporary file path
    temp_image_path = "/tmp/temp_image.jpg"

    # Save the image to the temporary file path
    image.save(temp_image_path)

    # Encode the image to base64
    base64_image = encode_image(temp_image_path)

    # Update the image_url in the payload
    payload['messages'][0]['content'][1]['image_url']['url'] = f"data:image/jpeg;base64,{base64_image}"

    # Make the request to the OpenAI API
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Display the description


    # Extract the description from the response
    description = response.json()['choices'][0]['message']['content']

    # Display the description in a text box
    st.text_area("Description:", value=description, height=200)

