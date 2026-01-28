import pandas as pd
from fastapi import FastAPI
import joblib
import pydantic

app = FastAPI()

# Load the trained model
model = joblib.load('electricity_price_model.joblib')

class PredictionInput(pydantic.BaseModel):
    hour: int
    dayofweek: int
    month: int

@app.get("/")
def read_root():
    return {"status": "Electricity Price Prediction API is running."}

@app.post("/predict")
def predict_price(input_data: PredictionInput):
    # prepare input data for prediction as DataFrame 
    input_df = pd.DataFrame([input_data.model_dump()])
    # make prediction
    prediction = model.predict(input_df)
    return {"predicted_price": prediction[0]}