# Electricity Price Prediction API (MLOps Project)

Production-ready starter for training and serving an electricity price prediction model. It includes a FastAPI REST API for inference, a Streamlit UI for local interaction and a simple training pipeline using scikit-learn with data pulled from public APIs.

## Features
- FastAPI service with OpenAPI docs at /docs
- Streamlit UI to interact with the model locally
- Training script that fetches recent market prices and weather, merges features, trains a RandomForest model and evaluate model
- Saved artifact with model, feature order, MAE, and R² in [electricity_price_model.joblib](electricity_price_model.joblib)
- Docker image that runs the API and UI together

## Project Structure
- [main.py](main.py): FastAPI app exposing GET `/` and POST `/predict`
- [train.py](train.py): Fetches data, engineers features, trains and evaluates model, saves artifacts
- [ui.py](ui.py): Streamlit client that calls the local API for predictions
- [requirements.txt](requirements.txt): Python dependencies
- [dockerfile](dockerfile): Containerize API + UI
- [data/](data): Notebooks and sample data
- [electricity_price.ipynb](electricity_price.ipynb): Exploration notebook

## Quickstart (Local)
1) Create environment and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

2) Train the model (downloads fresh data, trains, and saves artifacts)

```bash
python train.py
```

Artifacts created/updated:
- [electricity_price_model.joblib](electricity_price_model.joblib)

3) Run the API

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Open API docs: http://localhost:8000/docs

4) (Optional) Run the Streamlit UI in a separate terminal

```bash
streamlit run ui.py --server.address 0.0.0.0 --server.port 8501
```

Open UI: http://localhost:8501

## API

Base URL: http://localhost:8000

- GET `/` — Health/info
- GET `/docs` — OpenAPI/Swagger UI
- POST `/predict` — Predict electricity price

## Streamlit UI

Run locally with:

```bash
streamlit run ui.py --server.address 0.0.0.0 --server.port 8501
```

It calls the local API at http://localhost:8000. Make sure the API is running.

## Docker

Build and run both API (8000) and UI (8501) in one container:

```bash
docker build -t electricity-price-api .
docker run --rm -p 8000:8000 -p 8501:8501 electricity-price-api
```

Then open:
- API docs: http://localhost:8000/docs
- UI: http://localhost:8501

## Training Details

The trainer in [train.py](train.py):
- Pulls latest market prices from `https://api.porssisahko.net/v1/latest-prices.json`
- Pulls hourly weather for a fixed lat/lon from Open‑Meteo
- Merges on timestamp and derives features: `hour`, `dayofweek`, `month`, `temp`, `wind`
- Trains a `RandomForestRegressor`
- Saves [electricity_price_model.joblib](electricity_price_model.joblib) containing: `model`, `feature_names`, `mae`, `r2`

## Tech Stack
- FastAPI, Uvicorn
- scikit-learn, pandas, joblib
- Streamlit
- Docker (optional)

