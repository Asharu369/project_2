from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List
import pandas as pd
import joblib
import io
from fastapi.middleware.cors import CORSMiddleware

# Load the ML Pipeline
model_path = r"pipeline\pipeline_star_type_pred.joblib"

try:
    model_pipeline = joblib.load(model_path)
except Exception as e:
    raise RuntimeError(f"Error loading the model pipeline: {str(e)}")

# Initialize the FastAPI App
app = FastAPI()

# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a Pydantic model for single prediction input
class StarFeatures(BaseModel):
    temperature: int = Field(..., alias='Temperature (K)', description='Temperature of the star in Kelvin')
    luminosity: float = Field(..., alias='Luminosity(L/Lo)', description='Luminosity of the star relative to the sun')
    radius: float = Field(..., alias='Radius(R/Ro)', description='Radius of the star relative to the sun')
    absolute_magnitude: float = Field(..., alias='Absolute magnitude(Mv)', description='Absolute magnitude of the star')

@app.get("/")
def root():
    """
    Root endpoint to check if the API is running.

    Returns:
        dict: A simple message indicating the API is active.
    """
    return {"Star Type Prediction API is running"}


# Endpoint for single prediction
@app.post("/predict")
def predict_star_type(features: StarFeatures):
    """
    Predict the star type based on given features.

    Args:
        features (StarFeatures): Input star features.

    Returns:
        dict: Prediction and probability.
    """
    # Prepare the input data
    input_data = pd.DataFrame([{
        'Temperature (K)': features.temperature,
        'Luminosity(L/Lo)': features.luminosity,
        'Radius(R/Ro)': features.radius,
        'Absolute magnitude(Mv)': features.absolute_magnitude
    }])

    # Make predictions
    try:
        prediction = model_pipeline.predict(input_data)[0]
        probability = model_pipeline.predict_proba(input_data)[0].max()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

    return {"predicted_type": prediction, "predicted_probability": probability}

# Endpoint for bulk prediction
@app.post("/bulk_predict")
async def bulk_predict(file: UploadFile = File(...)):
    """
    Perform bulk predictions for a CSV file containing star features.

    Args:
        file (UploadFile): CSV file with star features.

    Returns:
        StreamingResponse: CSV with predictions.
    """
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    # Read file content
    try:
        content = await file.read()
        input_df = pd.read_csv(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")

    # Validate required columns
    required_columns = ['Temperature (K)', 'Luminosity(L/Lo)', 'Radius(R/Ro)', 'Absolute magnitude(Mv)']
    if not all(column in input_df.columns for column in required_columns):
        raise HTTPException(
            status_code=400,
            detail=f"The file must contain the following columns: {required_columns}"
        )

    # Ensure correct column order
    input_df = input_df[required_columns]

    # Generate predictions
    try:
        input_df['Predicted Type'] = model_pipeline.predict(input_df)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bulk prediction error: {str(e)}")

    # Create CSV response
    output = io.StringIO()
    input_df.to_csv(output, index=False)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=predictions.csv"}
    )





