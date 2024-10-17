import sqlite3
import streamlit as st

# Function to insert pet data into SQLite database
def show_feature():
  st.write("test")
  def insert_pet_data(pet_type, age, breed, mood, health_condition):
      conn = sqlite3.connect('petpedia.db')
      cur = conn.cursor()
      cur.execute('''
      INSERT INTO pets (pet_type, age, breed, mood, health_condition)
      VALUES (?, ?, ?, ?, ?)
      ''', (pet_type, age, breed, mood, health_condition))
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

      if st.button("Submit"):
          insert_pet_data(pet_type, age, breed, mood, health_condition)
          st.success("Pet information saved successfully!")

  # Show the form in Streamlit
  show_pet_form()
  # Connect to SQLite database (it will create the file if it doesn't exist)
  conn = sqlite3.connect('petpedia.db')

  # Create a cursor object to interact with the database
  cur = conn.cursor()

  # Create a table to store pet details (if it doesn't already exist)
  cur.execute('''
  CREATE TABLE IF NOT EXISTS pets (
      id INTEGER PRIMARY KEY,
      pet_type TEXT,
      age INTEGER,
      breed TEXT,
      mood TEXT,
      health_condition TEXT
  )
  ''')

  # Commit changes and close the connection
  conn.commit()
  conn.close()

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
              st.write(f"Pet ID: {row[0]}")
              st.write(f"Type: {row[1]}, Age: {row[2]}, Breed: {row[3]}")
              st.write(f"Mood: {row[4]}, Health Condition: {row[5]}")
              st.write("---")
      else:
          st.write("No pet data found.")

  # Show pet data in Streamlit
  insert_pet_data("dog", 3, "samoyed", "happy", "healthy")
  insert_pet_data("cat", 4, "ragdoll", "angry", "healthy")
  insert_pet_data("cat", 5, "british shorthair", "sad", "healthy")
  insert_pet_data("cat", 4, "persian", "happy", "healthy")
  insert_pet_data("cat", 9, "siamese", "sad", "healthy")
  insert_pet_data("cat", 8, "sphynx", "happy", "healthy")
  show_pet_data()
