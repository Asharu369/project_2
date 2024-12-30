import streamlit as st
import pandas as pd
import requests
from io import StringIO
import base64

# API URL
API_BASE_URL = "https://star-type-predictor-6jei.onrender.com"

# Sample dataset file path
SAMPLE_DATASET_FILE_PATH = "sample_dataset_csv.csv"

# Define a mapping of star types to background images
STAR_TYPE_BACKGROUNDS = {
    "Supergiant": "images/supergiant_star.jpg",
    "Hypergiant": "images/hypergiant_star.jpg",
    "Main Sequence": "images/main_sequence star.jpg",
    "White Dwarf": "images/whitedwarf_star.jpg",
    "Red Dwarf": "images/reddwarf_star.jpg",
    "Brown Dwarf": "images/brown_dwarf.jpg",
}

# Function to set dynamic background
def set_background(image_path):
    with open(image_path, "rb") as bg_file:
        bg_image_base64 = base64.b64encode(bg_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/webp;base64,{bg_image_base64}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set up the Streamlit app
st.set_page_config(page_title="Star Type Predictor", page_icon="☀️", layout="wide")

# Add static default background image
DEFAULT_BACKGROUND_IMAGE_PATH = "images/static_image.jpg"
with open(DEFAULT_BACKGROUND_IMAGE_PATH, "rb") as bg_file:
    default_bg_image_base64 = base64.b64encode(bg_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/webp;base64,{default_bg_image_base64}");
            background-size: cover;
        }}
        .stContainer {{
            background: rgba(0, 0, 0, 0.7);
            padding: 20px;
            border-radius: 10px;
        }}
        .stSidebar {{
            background: rgba(0, 0, 0, 0.7);
        }}
        .black-transparent {{
            background: rgba(0, 0, 0, 0.7);
            padding: 15px;
            border-radius: 10px;
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Page selection
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Introduction", "Single Star Type Predictor", "Multiple Star Type Predictor"])

if page == "Introduction":
    with st.container():
        st.markdown(
            """
            <div class="black-transparent">
                <h1>Welcome to the Star Type Predictor Web App</h1>
                <p>This web application is designed to help you predict the type of stars based on their physical parameters. 
                Using machine learning models, we analyze key attributes of stars, such as temperature, luminosity, radius, 
                and absolute magnitude, to classify them into different types.</p>
                <p>Choose either the Single or Bulk Prediction mode from the menu to start exploring the stars!</p>
                <h2>How to Use This Application</h2>
                <ul>
                    <li><strong>Single Star Type Predictor</strong>: Enter the star's features like temperature, luminosity, radius, and absolute magnitude, then click on the Predict button to determine the star type.</li>
                    <li><strong>Multiple Star Type Predictor</strong>: Upload a CSV file containing multiple star data, and the app will return predictions for each star.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

elif page == "Single Star Type Predictor":
    with st.container():
        st.markdown(
            """
            <div class="black-transparent">
                <h1>Single Star Type Predictor</h1>
                <p>Enter the star's features below to predict its type:</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        temperature = st.number_input("Temperature (K)", min_value=0, step=100, value=5000)
        luminosity = st.number_input("Luminosity (L/Lo)", min_value=0.0, step=0.1, value=1.0)
        radius = st.number_input("Radius (R/Ro)", min_value=0.0, step=0.1, value=1.0)
        absolute_magnitude = st.number_input("Absolute Magnitude (Mv)", step=0.1, value=5.0)

        if st.button("Predict Star Type"):
            payload = {
                "Temperature (K)": temperature,
                "Luminosity(L/Lo)": luminosity,
                "Radius(R/Ro)": radius,
                "Absolute magnitude(Mv)": absolute_magnitude,
            }

            response = requests.post(f"{API_BASE_URL}/predict", json=payload)

            if response.status_code == 200:
                result = response.json()
                predicted_type = result["predicted_type"]

                # Set background based on star type
                background_image_path = STAR_TYPE_BACKGROUNDS.get(predicted_type)
                if background_image_path:
                    set_background(background_image_path)

                st.markdown(
                    f"""
                    <div class="black-transparent">
                        <h2>Predicted Star Type: {predicted_type}</h2>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.error(f"Error: {response.json()['detail']}")

elif page == "Multiple Star Type Predictor":
    with st.container():
        st.markdown(
            """
            <div class="black-transparent">
                <h1>Multiple Star Type Predictor</h1>
                <p>Upload a CSV file with star features to get predictions for multiple stars:</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Load the uploaded sample dataset here
        with open(SAMPLE_DATASET_FILE_PATH, "rb") as file:
            sample_file_content = file.read()

        # Add a download button for the sample dataset
        st.download_button(
            label="Download Sample Dataset",
            data=sample_file_content,
            file_name="sample_dataset.csv",
            mime="text/csv",
        )

        uploaded_file = st.file_uploader("Upload a CSV file with star features", type=["csv"])

        if uploaded_file:
            try:
                file_content = uploaded_file.read()
                uploaded_df = pd.read_csv(StringIO(file_content.decode("utf-8")))

                st.markdown(
                    """
                    <div class="black-transparent">
                        <h2>Uploaded Data</h2>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.dataframe(uploaded_df)

                response = requests.post(
                    f"{API_BASE_URL}/bulk_predict",
                    files={"file": (uploaded_file.name, file_content, "text/csv")},
                )

                if response.status_code == 200:
                    predictions_csv = response.content.decode("utf-8")
                    predictions_df = pd.read_csv(StringIO(predictions_csv))

                    st.markdown(
                        """
                        <div class="black-transparent">
                            <h2>Predictions</h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.dataframe(predictions_df)

                    st.download_button(
                        label="Download Predictions",
                        data=predictions_csv,
                        file_name="predictions.csv",
                        mime="text/csv",
                    )
                else:
                    st.error(f"Error: {response.json()['detail']}")

            except Exception as e:
                st.error(f"Error processing file: {str(e)}")

# Footer section
footer_style = """
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: black;
            color: white;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            z-index: 1000;
        }
    </style>
    <div class="footer">
        Developed by <b>Muhammed Asharudheen</b> as part of the ML4A Training Program at Spartifical.
    </div>
"""
st.markdown(footer_style, unsafe_allow_html=True)


                








