    import streamlit as st
    import os
    import google.generativeai as genai
    import numpy as np
    import PIL.Image
    from openai import OpenAI

    # Initialize clients
    client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

    # Custom CSS styling
    st.markdown(
        """
        <style>
            body {
                background-color: #f5f5f5;
            }
            .title {
                color: #2e8b57;
                font-size: 50px;
                font-weight: bold;
                text-align: center;
                margin-bottom: 20px;
            }
            .header {
                color: #4682b4;
                font-size: 25px;
                margin-top: 30px;
                text-align: left;
            }
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 24px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
            }
            .stButton>button:hover {
                background-color: #45a049;
            }
            .stFileUploader {
                margin-top: 10px;
            }
            .error {
                color: red;
                font-weight: bold;
            }
        </style>
        """, unsafe_allow_html=True
    )

    def show_feature():
        st.markdown("<div class='title'>Animal Dietary Consultant</div>", unsafe_allow_html=True)
        st.write("Enter your animal-related food or health question below:")
        st.markdown("<div class='title'>Pet Care Assistant</div>", unsafe_allow_html=True)

        def petDetails():
            st.markdown("<div class='header'>Pet Details</div>", unsafe_allow_html=True)
            pet_type = st.selectbox("Select Pet Type", options=["Dog", "Cat", "Bird", "Other"])
            if pet_type == "Other":
                pet_type = st.text_input("Please specify the pet type")

            pet_age = st.number_input("Enter Pet Age (in years)", min_value=0, max_value=50, value=1, step=1)
            pet_breed = st.text_input("Enter Pet Breed")

            return pet_type, pet_age, pet_breed

        def generate_food_recommendation(pet_type, pet_age, pet_breed):
            system_prompt = f"""
            Based on the following pet details:
            - Type: {pet_type}
            - Age: {pet_age}
            - Breed: {pet_breed}

            Suggest appropriate food and supplies (exclude toys) for this pet:
            """
            user_input = f"Pet Type: {pet_type}, Age: {pet_age}, Breed: {pet_breed}"

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": system_prompt},
                          {"role": "user", "content": user_input}],
                temperature=1.0
            )
            return response.choices[0].message.content

        def foodRec(pet_type, pet_age, pet_breed):
            if st.button("Generate Food Recommendation"):
                if pet_type and pet_breed and pet_age:
                    recommendation = generate_food_recommendation(pet_type, pet_age, pet_breed)
                    st.markdown("<div class='header'>Recommended Food and Supplies:</div>", unsafe_allow_html=True)
                    st.write(recommendation)
                else:
                    st.markdown("<div class='error'>Please fill in all the required fields!</div>", unsafe_allow_html=True)

        def foodAnalyzer(pet_type, pet_age, pet_breed):
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
                        Bold the 'Food in the image', and 'Analysis'
                        You will only analyze food related image. Else, tell the user that "please upload only food images".
                        The output will be in the format as shown below:
                        Food in the image:

                        <food>

                        Analysis:

                        <Edible food>
                        <Non-edible food>
                        """
                    )
                    response = model.generate_content([f"Identify whether a {pet_age} year old {pet_breed} {pet_type} animal can eat the food.", image])
                    st.write(response.text)

        pet_type, pet_age, pet_breed = petDetails()
        foodRec(pet_type, pet_age, pet_breed)
        foodAnalyzer(pet_type, pet_age, pet_breed)

    show_feature()
