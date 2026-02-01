import pandas as pd
import requests
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
import joblib

def train_model():
    # get data
    elec_response = requests.get("https://api.porssisahko.net/v1/latest-prices.json")
    weather_response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=60.98208&longitude=25.66611&hourly=temperature_2m,windspeed_10m&past_days=31")
    df_elec = pd.DataFrame(elec_response.json()["prices"])
    df_weather = pd.DataFrame(weather_response.json()["hourly"])

    # preprocess data
    df_weather = pd.DataFrame({
        'time': pd.to_datetime(df_weather["time"]),
        'temp': df_weather["temperature_2m"],
        'wind': df_weather["windspeed_10m"]
    })

    df_elec['startDate'] = pd.to_datetime(df_elec['startDate'], utc=True).dt.tz_localize(None)
    df_weather['time'] = pd.to_datetime(df_weather['time'], utc=True).dt.tz_localize(None)

    # merge datasets on nearest timestamps
    df = pd.merge(df_elec, df_weather, left_on='startDate', right_on='time')

    # preprocess data
    df.drop(columns=['endDate'], inplace=True)
    # Convert timestamps to hours and days of the week and months
    df['hour'] = df['startDate'].dt.hour
    df['dayofweek'] = df['startDate'].dt.dayofweek
    df['month'] = df['startDate'].dt.month 


    # features (X) and target (y)
    feature_names = ['hour', 'dayofweek', 'month', 'temp', 'wind']
    X = df[feature_names]
    y = df['price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # train model
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X_train, y_train)

    # evaluate model
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"\n--- Model Performance ---")
    print(f"Mean Absolute Error: {mae:.2f} c/kWh")
    print(f"R2 Score: {r2:.2f}\n")

    # save model
    joblib.dump({'model': model, 'feature_names': feature_names, 'mae': mae, 'r2': r2}, 'electricity_price_model.joblib')
    df.to_csv('sahko_data.csv', index=False, encoding='utf-8')
    print("Model trained and saved as 'electricity_price_model.joblib'")

if __name__ == "__main__":
    train_model()