import streamlit as st
from pets import pets
import animalIdentification

# Custom CSS for radio buttons
st.markdown("""
<style>
    div.row-widget.stRadio > div {
        flex-direction: column;
        align-items: stretch;
    }
    div.row-widget.stRadio > div[role="radiogroup"] > label {
        padding: 10px 15px;
        margin: 4px 0;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s, color 0.3s;
        text-align: center;
    }
    div.row-widget.stRadio > div[role="radiogroup"] > label:hover {
        background-color: #555;
    }
    div.row-widget.stRadio > div[role="radiogroup"] > label[data-checked="true"] {
        background-color: #4CAF50;
        color: white;
    }
    /* Hide the radio button circle */
    div.row-widget.stRadio > div[role="radiogroup"] input[type="radio"] {
        position: absolute;
        opacity: 0;
        width: 0;
        height: 0;
    }
    /* Adjust spacing to account for hidden radio button */
    div.row-widget.stRadio > div[role="radiogroup"] > label > div:first-child {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Create two columns for layout
col1, col2 = st.columns([1, 3])  # Adjust the ratio for width (1:3 is an example)

# Left-side navigation
with col1:
    st.sidebar.title("Main Navigation")
    # Set default to "Home" by specifying index=2 (as "Home" is the 3rd option in the list)
    main_selection = st.sidebar.radio(
        "Select a Page", 
        ["Animal Identification", "Pets", "Home"], 
        index=2  # Set the default selection to "Home"
    )

# Right-side navigation (only appears if "Pets" is selected)
with col2:
    if main_selection == "Animal Identification":
        animalIdentification.animal_identification()

    elif main_selection == "Pets":
        pets.show_pets_navigation()
    else:
        st.title("Welcome to PetPedia")
        st.write("Select a page from the left sidebar.")