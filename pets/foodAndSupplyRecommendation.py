import streamlit as st
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
def show_feature():
    st.subheader("Food and Supply Recommendations")
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
        # Combine the user input into a single string for the 'content' field
        user_input = f"""
        Pet Type: {pet_type}, Age: {pet_age}, Breed: {pet_breed}, Mood: {pet_mood}, Health Condition: {health_condition}
        """

        response = client.chat.completions.create(
            model="gpt-4o",  
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=1.0,
            max_tokens=200  
        )

        return response.choices[0].message.content

    def foodRec():
        st.title("Pet Care Assistant")

        # Collect user input for pet type
        pet_type = st.selectbox("Select Pet Type", options=["Dog", "Cat", "Bird", "Other"])
        if pet_type == "Other":
            pet_type = st.text_input("Please specify the pet type")

        # Collect user input for pet age
        pet_age = st.number_input("Enter Pet Age (in years)", min_value=0, max_value=30, value=1, step=1)

        # Collect user input for pet breed
        pet_breed = st.text_input("Enter Pet Breed")

        # Collect user input for pet mood
        pet_mood = st.selectbox("Select Pet Mood", options=["Happy", "Anxious", "Aggressive", "Calm", "Neutral", "Other"])
        if pet_mood == "Other":
            pet_mood = st.text_input("Please specify the pet mood")

        # Collect user input for health condition
        health_condition = st.text_area("Describe any Health Conditions", value="None")

        # Button to trigger recommendation
        if st.button("Generate Food Recommendation"):
            if pet_type and pet_breed and pet_age and pet_mood:
                recommendation = generate_food_recommendation(pet_type, pet_age, pet_breed, pet_mood, health_condition)
                st.subheader("Recommended Food and Supplies:")
                st.write(recommendation)
            else:
                st.error("Please fill in all the required fields!")

    def foodSupplyRecBot(animal):
        foodSupply_prompt = """
        You are an animal or insects consultant.
        Based on the animal or species provided by the user, 
        suggest suitable food for the animal.

        - If the user asks for food suggestions, provide suggestions.
        - If the user asks whether the animal can eat specific food, answer the question with details.
        - Only answer questions related to animal food, diet, or health.
        """

        response = openai.chat.completions.create(
            model='gpt-4-turbo',
            messages=[
                {'role': 'system', 'content': foodSupply_prompt},
                {'role': 'user', 'content': animal}
            ],
            temperature=0.9,
            max_tokens=1000
        )
        return response.choices[0].message.content

    # Streamlit app interface
    st.title("Animal Dietary Consultant")
    st.write("Enter your animal-related food or health question below:")

    foodRec()
    # Input from the user
    user_input = st.text_input("Ask your question about the animal:")

    if st.button("Get Suggestion"):
        if user_input:
            with st.spinner("Fetching response..."):
                result = foodSupplyRecBot(user_input)
                st.success("Response received!")
                st.write(result)
        else:
            st.warning("Please enter a valid question.")
