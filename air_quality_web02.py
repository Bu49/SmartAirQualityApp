import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
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
# Streamlit UI Setup
# -------------------------------
st.set_page_config(page_title="Smart Air Quality Monitor", layout="wide")

st.title("🌫 Smart Air Quality & Smog Monitoring System")
st.subheader("Hello Afsha! Real-time IoT Dashboard")

# City selector with your list
city = st.selectbox("Select City:", 
    ["Bahawalpur", "Lodhran", "Lahore", "Karachi", "Islamabad", "Multan", "Sahiwal", "Gujranwala"]
)
aq_data = get_air_quality(city)
aqi = aq_data.get("pm25", 150)

# -------------------------------
# 1. Real-time Monitoring (Gauge + Cards)
# -------------------------------
st.markdown("## 📊 Real-Time Monitoring")

col1, col2 = st.columns([2, 2])

with col1:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=aqi,
        title={'text': "Air Quality Index (AQI)"},
        gauge={'axis': {'range': [0, 500]},
               'bar': {'color': "red" if aqi > 150 else "green"}}
    ))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.metric("PM2.5", f"{aq_data.get('pm25', 'N/A')} µg/m³")
    st.metric("PM10", f"{aq_data.get('pm10', 'N/A')} µg/m³")
    st.metric("CO₂", f"{aq_data.get('co', 'N/A')} ppm")
    st.metric("O₃", f"{aq_data.get('o3', 'N/A')} ppb")

# -------------------------------
# 2. Alerts/Notifications
# -------------------------------
st.markdown("## ⚠ Alerts & Notifications")
if aqi > 150:
    st.error("Hazardous Air Quality! Wear a mask.")
elif aqi > 100:
    st.warning("Moderate Air Quality. Sensitive groups should limit outdoor activity.")
else:
    st.success("Air quality is safe.")

# -------------------------------
# 3. Analytics/Visualization (Trends)
# -------------------------------
st.markdown("## 📈 Analytics & Visualization")

trend_data = {
    "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "PM2.5": [120, 135, 150, 160, 180, 190, aqi],
    "PM10": [80, 95, 100, 110, 120, 130, aq_data.get("pm10", 100)],
    "CO₂": [700, 720, 750, 780, 800, 820, aq_data.get("co", 800)]
}

fig = px.line(trend_data, x="Day", y=["PM2.5", "PM10", "CO₂"], 
              markers=True, title=f"Pollutant Trends in {city}")
st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# 4. Map Visualization
# -------------------------------
st.markdown("## 🗺 Smog Map Visualization")

map_data = {
    "City": ["Bahawalpur", "Lodhran", "Lahore", "Karachi", "Islamabad", "Multan", "Sahiwal", "Gujranwala"],
    "AQI": [aqi, 140, 160, 180, 120, 150, 130, 170],
    "Lat": [29.3956, 29.5310, 31.5497, 24.8607, 33.6844, 30.1575, 30.6706, 32.1877],
    "Lon": [71.6833, 71.6333, 74.3436, 67.0011, 73.0479, 71.5249, 73.1064, 74.1883]
}

fig = px.scatter_mapbox(
    map_data, lat="Lat", lon="Lon", size="AQI", color="AQI",
    hover_name="City", zoom=5, mapbox_style="open-street-map",
    title="Smog Density Map"
)
st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# 5. Smart Assistant Recommendations
# -------------------------------
st.markdown("## 🤖 Smart Assistant")
if aqi > 150:
    st.info("Recommendation: Avoid outdoor activity, use purifier, and wear a mask.")
elif aqi > 100:
    st.info("Recommendation: Sensitive groups should limit outdoor exposure.")
else:
    st.info("Recommendation: Air quality is good. Enjoy outdoor activities!")