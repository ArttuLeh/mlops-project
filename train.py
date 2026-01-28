import pandas as pd
import requests
from sklearn.ensemble import RandomForestRegressor
import joblib

# get data
response = requests.get("https://api.porssisahko.net/v1/latest-prices.json")
data = response.json()["prices"]
df = pd.DataFrame(data)

# preprocess data
# Convert timestamps to hours and days of the week and months
df['startDate'] = pd.to_datetime(df['startDate'])
df['hour'] = df['startDate'].dt.hour
df['dayofweek'] = df['startDate'].dt.dayofweek
df['month'] = df['startDate'].dt.month 


# features (X) and target (y)
feature_names = ['hour', 'dayofweek', 'month']
X = df[feature_names]
y = df['price']

# train model
model = RandomForestRegressor(n_estimators=100)
model.fit(X, y)

# save model
joblib.dump(model, 'electricity_price_model.joblib')
df.to_csv('sahko_data.csv', index=False, encoding='utf-8')
print("Model trained and saved as 'electricity_price_model.joblib'")
