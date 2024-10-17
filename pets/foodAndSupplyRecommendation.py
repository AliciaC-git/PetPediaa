    import streamlit as st
    import os
    import google.generativeai as genai
    import numpy as np
    import PIL.Image
    from openai import OpenAI


    client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

    def show_feature():

        st.subheader("Food and Supply Recommendations")

        def petDetails():
            # Collect user input for pet type
            pet_type = st.selectbox("Select Pet Type",
                                    options=["Dog", "Cat", "Bird", "Other"])
            if pet_type == "Other":
                pet_type = st.text_input("Please specify the pet type")

            # Collect user input for pet age
            pet_age = st.number_input("Enter Pet Age (in years)",
                                      min_value=0,
                                      max_value=50,
                                      value=1,
                                      step=1)

            # Collect user input for pet breed
            pet_breed = st.text_input("Enter Pet Breed")

            # Collect user input for pet mood
            pet_mood = st.selectbox("Select Pet Mood",
                                    options=[
                                        "Happy", "Anxious", "Aggressive", "Calm",
                                        "Neutral", "Other"
                                    ])
            if pet_mood == "Other":
                pet_mood = st.text_input("Please specify the pet mood")

            # Collect user input for health condition
            health_condition = st.text_area("Describe any Health Conditions",
                                            value="None")

            return pet_type, pet_age, pet_breed, pet_mood, health_condition


        def generate_food_recommendation(pet_type, pet_age, pet_breed, pet_mood,
                                         health_condition):
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

            response = client.chat.completions.create(model="gpt-4o",
                                                      messages=[{
                                                          "role":
                                                          "system",
                                                          "content":
                                                          system_prompt
                                                      }, {
                                                          "role":
                                                          "user",
                                                          "content":
                                                          user_input
                                                      }],
                                                      temperature=1.0,
                                                      max_tokens=200)

            return response.choices[0].message.content

        def foodRec(pet_type, pet_age, pet_breed, pet_mood,health_condition):
            # Button to trigger recommendation
            if st.button("Generate Food Recommendation"):
                if pet_type and pet_breed and pet_age and pet_mood:
                    recommendation = generate_food_recommendation(
                        pet_type, pet_age, pet_breed, pet_mood, health_condition)
                    st.subheader("Recommended Food and Supplies:")
                    st.write(recommendation)
                else:
                    st.error("Please fill in all the required fields!")


        def foodAnalyzer(pet_type, pet_age, pet_breed, pet_mood, health_condition):
            # File uploader for images
            uploaded_file = st.file_uploader("Upload a food image", type=["jpg", "jpeg", "png"])

            if uploaded_file is not None:
                image = PIL.Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image")

                if st.button("Analyze Food"):
                    model = genai.GenerativeModel(
                        "gemini-1.5-flash",
                        system_instruction="""
                        You are an animal food analyzer.
                        You will first analyze the food inside the uploaded image.
                        Then analyze whether the specific animal can eat the food or not.
                        You will list all the food in the image.
                        Provide detailed analysis for all edible and non-edible foods.
                        Bold the 'Food in teh image', and 'Analysis'
                        You will only analyze food related image. Else, tell the user that "please upload only food images".
                        The output will be in the format as shown below:
                        Food in the image:

                        <food>

                        Analysis:

                        <Edible food>
                        <Non-edible food>
                        """
                    )
                    response = model.generate_content([f"Identify whether a {pet_age} year old {pet_mood} {pet_breed} {pet_type} animal with {health_condition} historical cases can eat the food.", image])
                    st.write(response.text)


        # Streamlit app interface
        st.title("Animal Dietary Consultant")
        st.write("Enter your animal-related food or health question below:")
        st.title("Pet Care Assistant")

        pet_type, pet_age, pet_breed, pet_mood, health_condition = petDetails()
        foodRec(pet_type, pet_age, pet_breed, pet_mood, health_condition)
        foodAnalyzer(pet_type, pet_age, pet_breed, pet_mood, health_condition)