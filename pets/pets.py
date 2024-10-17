import streamlit as st
from pets import foodAndSupplyRecommendation, viewMyPets, vetLocator, chatbot

# Function to render the sticky navigation bar
def show_navbar():
    st.markdown("""
        <style>
            .navbar {
                position: fixed;
                top: 0;
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
        """, unsafe_allow_html=True)

    # Navigation buttons
    cols = st.columns(4)

    with cols[0]:
        if st.button("Food & Supply"):
            st.session_state['nav'] = "Food and Supply Recommendations"

    with cols[1]:
        if st.button("View My Pets"):
            st.session_state['nav'] = "View My Pets"

    with cols[2]:
        if st.button("Vet Locator"):
            st.session_state['nav'] = "Vet Locator"

    with cols[3]:
        if st.button("Chatbot"):
            st.session_state['nav'] = "Chatbot"

# Function to manage which feature is shown
def show_pets_navigation():
    # Initialize session state
    if 'nav' not in st.session_state:
        st.session_state['nav'] = "Food and Supply Recommendations"  # Default selection

    # Render the sticky navbar
    show_navbar()

    # Display the selected feature
    if st.session_state['nav'] == "Food and Supply Recommendations":
        foodAndSupplyRecommendation.show_feature()

    elif st.session_state['nav'] == "View My Pets":
        viewMyPets.main()

    elif st.session_state['nav'] == "Vet Locator":
        vetLocator.show_feature()

    elif st.session_state['nav'] == "Chatbot":
        chatbot.show_feature()