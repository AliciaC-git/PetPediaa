import streamlit as st
from PIL import Image
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

# Title and Introduction
st.title("Animal Dietary Consultant")
st.write("Get food and supply recommendations or analyze food for your pet!")

# Function: Generate Food Recommendation using OpenAI
def generate_food_recommendation(pet_type, pet_age, pet_breed, pet_mood, health_condition):
    system_prompt = f"""
    Based on the following pet details:
    - Type: {pet_type}
    - Age: {pet_age}
    - Breed: {pet_breed}
    - Mood: {pet_mood}
    - Health Conditions: {health_condition}

    Suggest appropriate food and supplies (exclude toys) for this pet:
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",  
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Pet Type: {pet_type}, Age: {pet_age}, Breed: {pet_breed}, Mood: {pet_mood}, Health Condition: {health_condition}"}
        ],
        temperature=1.0,
        max_tokens=200  
    )
    return response.choices[0].message.content

# Function: Analyze Food Image
def food_analyzing(image, pet_type, pet_age, pet_breed, pet_mood, health_condition):
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Simulate model response (replace this with actual API/model interaction)
    analysis = f"""
    **Food in the Image:** Example Food  
    **Analysis:**  
    A {pet_age}-year-old {pet_mood} {pet_breed} ({pet_type}) with {health_condition} can eat this food.
    """

    st.subheader("Analysis Result")
    st.text(analysis)

# Sidebar Inputs: Animal Details
st.sidebar.header("Animal Details")
pet_type = st.sidebar.selectbox("Animal Type", ["Dog", "Cat", "Bird", "Rabbit"])
pet_age = st.sidebar.slider("Age", 0, 20, 2)
pet_breed = st.sidebar.text_input("Breed", "Chihuahua")
pet_mood = st.sidebar.selectbox("Mood", ["Happy", "Sad", "Energetic", "Calm"])
health_condition = st.sidebar.text_input("Health Condition", "None")

# Button to Generate Recommendation
if st.button("Generate Food Recommendation"):
    if pet_type and pet_breed and pet_age and pet_mood:
        recommendation = generate_food_recommendation(pet_type, pet_age, pet_breed, pet_mood, health_condition)
        st.subheader("Recommended Food and Supplies:")
        st.write(recommendation)
    else:
        st.error("Please fill in all the required fields!")

# File Uploader for Food Image
uploaded_file = st.file_uploader("Upload a food image", type=["jpg", "jpeg", "png"])

# Handle Image Upload and Analysis
if uploaded_file:
    image = Image.open(uploaded_file)
    food_analyzing(image, pet_type, pet_age, pet_breed, pet_mood, health_condition)
else:
    st.warning("Please upload an image to proceed.")
