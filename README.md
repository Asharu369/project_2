# Star Type Predictor🌞

This [web application](https://startypespredictor.streamlit.app/) predicts star types based on various stellar characteristics using machine learning algorithms. It serves as an educational tool to understand classification models and their application in astronomy.

## Key Features

- **Data Input**: Users can input stellar parameters such as temperature, luminosity, radius, and color.
- **Machine Learning Model**: The application utilizes a trained classification model to predict the star type.
- **Visualization**: Results are presented with visual aids to enhance understanding.
- **API Documentation**: Access backend API documentation [here](https://star-type-predictor-6jei.onrender.com/docs).

## Getting Started

Follow these steps to set up the project locally:

### Prerequisites

- Python 3.7 or higher
- Virtual environment tool (e.g., `venv`)

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Asharu369/project_2.git
   cd project_2
   ```

2. **Create and Activate a Virtual Environment**:

   - For Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - For Linux/macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Backend**:

   The backend is built with FastAPI. Run it using:

   ```bash
   uvicorn backend:app --reload
   ```

2. **Start the Frontend**:

   The frontend is built with Streamlit. Run it using:

   ```bash
   streamlit run frontend.py
   ```

3. **Access the Application**:

   Open your browser and navigate to `http://localhost:8501` to interact with the application.

## Usage

- **Input Data**: Enter the stellar parameters into the input fields.
- **Predict**: Click the 'Predict' button to determine the star type.
- **Visualization**: View the results and accompanying visualizations to understand the prediction.

## Dataset

The model is trained on a dataset containing various star types with attributes like temperature, luminosity, radius, and color. This dataset is included in the repository as `sample_dataset_csv.csv`.

## Model Training

The `training_notebook` directory contains Jupyter notebooks used for data exploration and model training. These notebooks provide insights into the feature selection and model evaluation processes.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to the contributors of open-source libraries used in this project.
