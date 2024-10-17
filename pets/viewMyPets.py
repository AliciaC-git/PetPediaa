import sqlite3
import streamlit as st
from io import BytesIO
from PIL import Image

# Mock GPT-4 API call to convert image to URL (replace with actual API call)
def get_image_url(image):
    # Assuming the API returns a URL when you pass the image.
    # Here we mock it by just returning a placeholder URL.
    return "https://yourimagestorage.com/uploaded_image.jpg"

# Function to insert pet data into SQLite database
def insert_pet_data(pet_type, age, breed, mood, health_condition, image_url):
    conn = sqlite3.connect('petpedia.db')
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO pets (pet_type, age, breed, mood, health_condition, image_url)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (pet_type, age, breed, mood, health_condition, image_url))
    conn.commit()
    conn.close()

# Streamlit form to collect pet details
def show_pet_form():
    st.title("Add Pet Information")

    pet_type = st.selectbox("Pet Type", ["Dog", "Cat", "Bird", "Other"])
    if pet_type == "Other":
        pet_type = st.text_input("Specify Pet Type")

    age = st.number_input("Age", min_value=0)
    breed = st.text_input("Breed")
    mood = st.selectbox("Mood", ["Happy", "Sad", "Aggressive", "Calm", "Other"])
    if mood == "Other":
        mood = st.text_input("Specify Mood")

    health_condition = st.text_area("Health Condition")

    # Image upload feature
    uploaded_image = st.file_uploader("Upload Pet Image", type=["png", "jpg", "jpeg"])

    if st.button("Submit"):
        if uploaded_image is not None:
            image = Image.open(BytesIO(uploaded_image.read()))  # Read the uploaded image
            image_url = get_image_url(image)  # Call GPT-4 or other API to get the image URL
            st.success(f"Image uploaded successfully! URL: {image_url}")

            # Insert all details into the database
            insert_pet_data(pet_type, age, breed, mood, health_condition, image_url)
            st.success("Pet information saved successfully!")
        else:
            st.error("Please upload an image.")

# Function to fetch and display pet data
def fetch_pet_data():
    conn = sqlite3.connect('petpedia.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM pets')
    rows = cur.fetchall()
    conn.close()
    return rows

# Streamlit app to display pet data
def show_pet_data():
    st.title("Pet Information")
    pet_data = fetch_pet_data()

    if pet_data:
        for row in pet_data:
            st.markdown(f"## Pet ID: {row[0]}")
            st.markdown(f"### Type: {row[1]}")
            st.markdown(f"**Age**: {row[2]} years")
            st.markdown(f"**Breed**: {row[3]}")
            st.markdown(f"**Mood**: {row[4]}")
            st.markdown(f"**Health Condition**: {row[5]}")

            # Display pet image
            if row[6]:
                st.image(row[6], caption=f"{row[1]} Image")
            st.write("---")
    else:
        st.write("No pet data found.")

# Create a table to store pet details, including image URLs
def create_table():
    conn = sqlite3.connect('petpedia.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS pets (
        id INTEGER PRIMARY KEY,
        pet_type TEXT,
        age INTEGER,
        breed TEXT,
        mood TEXT,
        health_condition TEXT,
        image_url TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Main application
def main():
    st.write("Test")
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Add Pet", "View Pets"])

    create_table()  # Ensure table is created

    if page == "Add Pet":
        show_pet_form()
    elif page == "View Pets":
        show_pet_data()

if __name__ == "__main__":
    main()
