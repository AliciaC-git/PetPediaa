import streamlit as st
import os
import google.generativeai as genai
import numpy as np
import PIL.Image
from openai import OpenAI

# Initialize OpenAI and GenAI API clients
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Define CSS styles
st.markdown("""
    <style>
    body {
        background-color: #f0f2f6;
        font-family: 'Arial', sans-serif;
    }
    .main-title {
        color: #333;
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #888;
        font-size: 24px;
        margin-top: -10px;
        margin-bottom: 30px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        font-size: 16px;
        margin: 10px 0;
        cursor: pointer;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .input-box {
        margin-bottom: 15px;
    }
    textarea, input {
        width: 100%;
        padding: 12px;
        margin: 8px 0;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-sizing: border-box;
    }
    .uploaded-image {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 50%;
        border: 2px solid #ddd;
        border-radius: 10px;
    }
    .recommendation-text {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 8px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# App's main title and subtitle
st.markdown('<h1 class="main-title">Animal Dietary Consultant</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Your Pet Care Assistant</p>', unsafe_allow_html=True)

def petDetails():
    # Collect user input for pet type
    pet_type = st.selectbox("Select Pet Type", ["Dog", "Cat", "Bird", "Other"], key="pet_type")
    if pet_type == "Other":
        pet_type = st.text_input("Please specify the pet type", key="other_type")

    # Collect user input for pet age
    pet_age = st.number_input("Enter Pet Age (in years)", min_value=0, max_value=50, value=1, step=1, key="age")

    # Collect user input for pet breed
    pet_breed = st.text_input("Enter Pet Breed", key="breed")

    # Collect user input for pet mood
    pet_mood = st.selectbox("Select Pet Mood", ["Happy", "Anxious", "Aggressive", "Calm", "Neutral", "Other"], key="mood")
    if pet_mood == "Other":
        pet_mood = st.text_input("Please specify the pet mood", key="other_mood")

    # Collect user input for health condition
    health_condition = st.text_area("Describe any Health Conditions", value="None", key="health")

    return pet_type, pet_age, pet_breed, pet_mood, health_condition

def generate_food_recommendation(pet_type, pet_age, pet_breed, pet_mood, health_condition):
    system_prompt = f"""
    Based on the following pet details:
    - Type: {pet_type}
    - Age: {pet_age}
    - Breed: {pet_breed}
    - Mood: {pet_mood}
    - Health Condition: {health_condition}

    Suggest appropriate food and supplies (exclude toys) for this pet:
    """
    user_input = f"""
    Pet Type: {pet_type}, Age: {pet_age}, Breed: {pet_breed}, Mood: {pet_mood}, Health Condition: {health_condition}
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}],
        temperature=1.0,
        max_tokens=200
    )
    return response.choices[0].message.content

def foodRec(pet_type, pet_age, pet_breed, pet_mood, health_condition):
    if st.button("Generate Food Recommendation"):
        if pet_type and pet_breed and pet_age and pet_mood:
            recommendation = generate_food_recommendation(pet_type, pet_age, pet_breed, pet_mood, health_condition)
            st.markdown('<div class="recommendation-text"><h4>Recommended Food and Supplies:</h4>', unsafe_allow_html=True)
            st.write(recommendation)
        else:
            st.error("Please fill in all the required fields!")

def foodAnalyzer(pet_type, pet_age, pet_breed, pet_mood, health_condition):
    uploaded_file = st.file_uploader("Upload a food image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = PIL.Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True, output_format="JPEG", class_="uploaded-image")

        if st.button("Analyze Food"):
            model = genai.GenerativeModel(
                "gemini-1.5-flash",
                system_instruction="""
                You are an animal food analyzer.
                Analyze the food inside the uploaded image and determine if the specific animal can eat it.
                Bold the 'Food in the image' and 'Analysis'.
                """)
            response = model.generate_content([
                f"Analyze if a {pet_age} year old {pet_mood} {pet_breed} {pet_type} with {health_condition} can eat this.",
                image
            ])
            st.write(response.text)

# Collect user inputs and display recommendations
pet_type, pet_age, pet_breed, pet_mood, health_condition = petDetails()
foodRec(pet_type, pet_age, pet_breed, pet_mood, health_condition)
foodAnalyzer(pet_type, pet_age, pet_breed, pet_mood, health_condition)



    
    # def foodSupplyRecBot(animal):
    #     foodSupply_prompt = """
    #     You are an animal or insects consultant.
    #     Based on the animal or species provided by the user, 
    #     suggest suitable food for the animal.

    #     - If the user asks for food suggestions, provide suggestions.
    #     - If the user asks whether the animal can eat specific food, answer the question with details.
    #     - Only answer questions related to animal food, diet, or health.
    #     """

    #     response = openai.chat.completions.create(model='gpt-4-turbo',
    #                                               messages=[{
    #                                                   'role':
    #                                                   'system',
    #                                                   'content':
    #                                                   foodSupply_prompt
    #                                               }, {
    #                                                   'role': 'user',
    #                                                   'content': animal
    #                                               }],
    #                                               temperature=0.9,
    #                                               max_tokens=1000)
    #     return response.choices[0].message.content


    
    # # Input from the user
    # user_input = st.text_input("Ask your question about the animal:")

    # if st.button("Get Suggestion"):
    #     if user_input:
    #         with st.spinner("Fetching response..."):
    #             result = foodSupplyRecBot(user_input)
    #             st.success("Response received!")
    #             st.write(result)
    #     else:
    #         st.warning("Please enter a valid question.")