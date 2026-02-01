import pandas as pd
from fastapi import FastAPI, HTTPException
import joblib
import pydantic
import os

app = FastAPI()
MODEL_FILE = 'electricity_price_model.joblib'

if os.path.exists(MODEL_FILE):
    # load the trained model
    model_data = joblib.load(MODEL_FILE)
    model = model_data['model']
    feature_names = model_data['feature_names']
    mae = model_data.get('mae')
    r2 = model_data.get('r2')
    print(f"Model loaded successfully. Features: {feature_names}")
else:
    print("WARNING: Model file not found! Run train.py first.")
    model = None

class PredictionInput(pydantic.BaseModel):
    hour: int
    dayofweek: int
    month: int
    temp: float
    wind: float

@app.get("/")
def read_root():
    return {"status": "Electricity Price Prediction API is running. Go to /docs for Swagger UI."}

@app.post("/predict")
def predict_price(input_data: PredictionInput):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded on server.")

    try:
        # prepare input data for prediction as DataFrame
        input_dict = input_data.model_dump()
        input_df = pd.DataFrame([input_dict])
        input_df = input_df[feature_names]

        # make prediction
        prediction = float(model.predict(input_df)[0])

        lower_bound = round(prediction - mae, 2)
        upper_bound = round(prediction + mae, 2)

        return {
                "prediction": {
                    "estimated_price": round(prediction, 2),
                    "unit": "s/kWh",
                    "range": {
                        "min": max(0, lower_bound),
                        "max": upper_bound
                    }
                },
                "meta": {
                    "model_mae": round(mae, 2),
                    "model_r2": round(r2, 2),
                    "input_received": input_dict
                }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)