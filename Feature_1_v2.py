import streamlit as st
import torch
import clip
from PIL import Image
from torchvision.transforms import Compose, Resize, CenterCrop, ToTensor, Normalize
import openai
import os
from openai import OpenAI
client = OpenAI()

# Load the model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load('ViT-B/32', device=device)

openai.api_key = os.environ["OPENAI_API_KEY"]

# Define the preprocessing steps
preprocess = Compose([
    Resize(256, interpolation=Image.BICUBIC),
    CenterCrop(224),
    ToTensor()
])

# Streamlit code
st.title('Clothing Classifier')

uploaded_file = st.file_uploader("Choose an image...", type="jpg")

def get_completion(prompt, model="gpt-3.5-turbo"):
    completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role":"system",
         "content": "Based on the result provided, give suggestions on brands that have similar items; provide valid and available links to websites of these brands."},
        {"role": "user",
         "content": prompt},
        ]
    )
    return completion.choices[0].message.content

# Streamlit code
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")

    # Preprocess the image
    image = preprocess(image).unsqueeze(0).to(device)

    # Generate a list of labels
    labels = ["crewneck", "hoodie", "cargo pants", "shirt", "shoes", "shorts", "sneakers", "sweater", "t-shirt", "jeans", "dress", "skirt"]

    # Encode the labels
    num_labels = min(len(labels), 1000) 
    text = clip.tokenize(labels[:num_labels]).to(device)

    # Get the model's prediction
    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)

    # Calculate the similarity between the image and the labels
    similarity = torch.nn.functional.cosine_similarity(image_features, text_features, dim=-1)
    values, indices = similarity.topk(1)
    values *= 100

    # Output the results
    st.write("This article of clothing is detected as:")
    for value, index in zip(values, indices):
        st.write(f"**{labels[index]}**")

    # Get GPT-3.5 Turbo completion
    completion = get_completion(labels[index])
    st.write(completion)
