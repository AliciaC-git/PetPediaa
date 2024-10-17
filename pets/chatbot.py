import streamlit as st
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
# Define the chatbot function
def show_feature():
    def chatbot(prompt):
        system_prompt = """
        You are a helpful and knowledgeable pet care assistant. Your primary function is to answer pet-related questions, provide health and behavior tips, suggest appropriate food and supplies based on pet age, breed, and preferences, and assist with common pet concerns. You can help pet owners by offering advice on exercise, vaccinations, feeding schedules, and general care. If the question involves medical emergencies, you suggest some necessary first aid steps, visiting a veterinarian, or locating the nearest vet (if location is provided). Be friendly, clear, and concise in your responses. """

        # Generate a response using OpenAI's API
        response = client.chat.completions.create(
            model="gpt-4o",  
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=1.0,
            max_tokens=1000  
        )

        return response.choices[0].message.content

    # Streamlit app layout
    st.title("Pet Care Assistant Chatbot")
    st.write("Ask me anything about pet care, and I'll do my best to assist you!")

    # Input field for the user to ask a question
    user_input = st.text_area("Ask a question about your pet:")

    # Button to trigger the chatbot response
    if st.button("Get Advice"):
        if user_input:
            with st.spinner("Thinking..."):
                answer = chatbot(user_input)  # Call the chatbot function
                st.write(answer)  # Display the chatbot's response
        else:
            st.write("Please enter a question!")

