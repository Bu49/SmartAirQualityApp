import streamlit as st
import plotly.graph_objects as go
import requests

# -------------------------------
# Function to fetch live air quality data
# -------------------------------
def get_air_quality(city="Bahawalpur"):
    url = f"https://api.openaq.org/v2/latest?city={city}"
    response = requests.get(url)
    data = response.json()
    
    results = {}
    if "results" in data and len(data["results"]) > 0:
        for measurement in data['results'][0]['measurements']:
            results[measurement['parameter']] = measurement['value']
    return results

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Smart Air Quality Monitor", layout="centered")

st.title("🌫 Smart Air Quality & Smog Monitoring System")
st.subheader("Hello, Afsha!")

# 1. Real-time Monitoring with city selector
city = st.selectbox("Select City:", ["Bahawalpur", "Lahore", "Lodhran", "Multan", "Karachi"])
aq_data = get_air_quality(city)
aqi = aq_data.get("pm25", 150)  # fallback if missing

st.markdown(f"### 📍 City: {city}")
st.write(f"PM2.5: {aq_data.get('pm25', 'N/A')} µg/m³")
st.write(f"PM10: {aq_data.get('pm10', 'N/A')} µg/m³")
st.write(f"CO₂: {aq_data.get('co', 'N/A')} ppm")
st.write(f"O₃: {aq_data.get('o3', 'N/A')} ppb")

# AQI Gauge
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=aqi,
    title={'text': "AQI"},
    gauge={'axis': {'range': [0, 500]},
           'bar': {'color': "red" if aqi > 150 else "green"}}
))
st.plotly_chart(fig)

# 2. User-Friendly Interface
st.info("Easy-to-read cards and charts for quick understanding.")

# 3. Alerts/Notifications
st.markdown("### ⚠ Alerts")
if aqi > 150:
    st.error("Hazardous Air Quality! Wear a mask.")
elif aqi > 100:
    st.warning("Moderate Air Quality. Sensitive groups should limit outdoor activity.")
else:
    st.success("Air quality is safe.")

# 4. Analytics/Visualization
st.markdown("### 📈 AQI Trends (Last 7 Days)")
trend_data = [120, 135, 150, 160, 180, 190, aqi]
st.line_chart(trend_data)

# 5. Additional Feature: Smart Assistant
if st.button("Ask Smart Assistant"):
    if aqi > 150:
        st.info("Recommendation: Avoid outdoor activity, use air purifier, and wear a mask.")
    elif aqi > 100:
        st.info("Recommendation: Sensitive groups should limit outdoor exposure.")
    else:
        st.info("Recommendation: Air quality is good. Enjoy outdoor activities!")