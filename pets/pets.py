import streamlit as st
from pets import foodAndSupplyRecommendation, petHealthMonitoringAndAlerts, vetLocator, chatbot

# Function to render the sticky navigation bar
def show_navbar():
    st.markdown("""
        <style>
            .navbar {
                position: fixed;
                top: 45px;
                left: 0;
                right: 0;
                z-index: 1000;
                display: flex;
                background-color: #333;
            }
            .navbar button {
                flex: 1;
                background-color: #333;
                border: none;
                color: white;
                padding: 15px 0;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            .navbar button:hover {
                background-color: #555;
            }
            .navbar button:active {
                background-color: #4CAF50;
            }
            .content {
                margin-top: 50px;
            }
        </style>
        <div class="navbar">
            <form action="/" method="post" style="display: flex; width: 100%;">
                <button type="submit" name="nav" value="Food and Supply Recommendations">Food & Supply</button>
                <button type="submit" name="nav" value="Pet Health Monitoring">Health Monitoring</button>
                <button type="submit" name="nav" value="Vet Locator">Vet Locator</button>
                <button type="submit" name="nav" value="Chatbot">Chatbot</button>
            </form>
        </div>
        <div class="content">
            <!-- Your page content goes here -->
        </div>
        """, unsafe_allow_html=True)

# Function to manage which feature is shown
def show_pets_navigation():
    # Render the sticky navbar
    show_navbar()

    # Collect selected navigation option from the buttons
    if 'nav' not in st.session_state:
        st.session_state['nav'] = "Food and Supply Recommendations"  # Default selection

    if st.session_state['nav'] == "Food and Supply Recommendations":
        foodAndSupplyRecommendation.show_feature()

    elif st.session_state['nav'] == "Pet Health Monitoring":
        petHealthMonitoringAndAlerts.show_feature()

    elif st.session_state['nav'] == "Vet Locator":
        vetLocator.show_feature()

    elif st.session_state['nav'] == "Chatbot":
        chatbot.show_feature()

# Handle the form submission from the navbar
def handle_nav_form():
    if st.form_submit_button():
        selected_option = st.experimental_get_query_params().get("nav")
        if selected_option:
            st.session_state['nav'] = selected_option[0]