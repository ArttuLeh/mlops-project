import streamlit as st
import requests

st.title('Electricity price predicter')

# input fields
st.sidebar.header("Time and Weather Information")
hour = st.sidebar.number_input("Hour", 1, 24, 12)
dayofweek = st.sidebar.selectbox("Day of Week", list(range(7)), index=0, format_func=lambda x: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][x])
month = st.sidebar.selectbox("Month", list(range(1, 13)), index=0)
temp = st.sidebar.slider("Temperature (°C)", -40, 40, 0)
wind = st.sidebar.slider("Wind Speed (m/s)", 0, 30, 5)

# predict button
if st.button('Predict Electricity Price'):
    input_data = {
        "hour": hour,
        "dayofweek": dayofweek,
        "month": month,
        "temp": temp,
        "wind": wind
    }

    # send input data to the FastAPI prediction endpoint
    response = requests.post("http://localhost:8000/predict", json=input_data)
    result = response.json()

    # extract estimated price from response
    price = result["prediction"]["estimated_price"]
    
    # display result
    st.metric(label="Predicted Price", value=f"{price} s/kWh")
    st.write(f"Range: {result['prediction']['range']['min']} - {result['prediction']['range']['max']} s/kWh")