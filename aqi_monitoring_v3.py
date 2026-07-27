"""
Smart Indoor Air Quality Monitoring Dashboard
=============================================

Streamlit dashboard for visualizing real-time indoor air quality
data from an ESP32-based IoT monitoring system using DHT22 and
MQ135 sensors with ThingSpeak as the cloud backend.

Developed by:
    Ashmit Gupta
    Ayush Raj

Department:
    Electronics & Communication Engineering
    UIET, Panjab University
"""


import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from zoneinfo import ZoneInfo

# ============================================================
# CONFIGURATION
# ============================================================

CHANNEL_ID = "3386480"
READ_API_KEY = st.secrets["READ_API_KEY"]
REFRESH_SECONDS = 20

URL = (
    f"https://api.thingspeak.com/channels/"
    f"{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results=50"
)

st.set_page_config(
    page_title="Smart Indoor Air Quality Dashboard",
    page_icon="🌍",
    layout="wide",
)

# Automatically refresh every 20 seconds
st_autorefresh(interval=20000, key="refresh")

st.markdown("""
<style>
.main {padding-top:1rem;}
.status-box{
    border-radius:15px;
    padding:22px;
    color:white;
    font-weight:bold;
    text-align:center;
    font-size:24px;
    letter-spacing:1px;
}
.footer{
    text-align:center;
    color:gray;
    font-size:15px;
    padding-top:20px;
}
.recommend{
    padding:18px;
    border-radius:10px;
    border-left:6px solid #4CAF50;
    background-color:rgba(76,175,80,0.15);
    color:inherit;
    font-size:16px;
}
.room-card{
    background: rgba(255,255,255,0.03);
    border: 1px solid #3A3A3A;
    border-radius: 12px;
    padding: 24px;
    margin-top: 10px;
}

.room-title{
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 6px;
}

.room-message{
    color:#B0B0B0;
    font-size:16px;
    margin-bottom:18px;
}

.room-divider{
    border:none;
    border-top:1px solid #444;
    margin:18px 0;
}

.parameter-row{
    display:flex;
    justify-content:space-between;
    font-size:17px;
    padding:8px 0;
}

.parameter-label{
    font-weight:600;
}

.score-box{
    text-align:right;
    color:#CFCFCF;
    font-size:15px;
}
</style>
""", unsafe_allow_html=True)

st.title("🌍 Smart Indoor Air Quality Monitoring Dashboard")
st.caption("ESP32 • DHT22 • MQ135 • ThingSpeak • Streamlit")

try:
    response = requests.get(URL, timeout=10)
    response.raise_for_status()
    data = response.json()
    feeds = data["feeds"]
except Exception as e:
    st.error(f"Unable to fetch ThingSpeak data.\n\n{e}")
    st.stop()

df = pd.DataFrame(feeds)

df = df.rename(columns={
    "field1":"Temperature",
    "field2":"Humidity",
    "field3":"Gas",
    "field4":"AQ"
})

for col in ["Temperature","Humidity","Gas"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["created_at"] = (
    pd.to_datetime(df["created_at"], utc=True)
      .dt.tz_convert("Asia/Kolkata")
)

df = df.dropna()

latest = df.iloc[-1]

temp = latest["Temperature"]
hum = latest["Humidity"]
gas = latest["Gas"]

# =========================
# AIR QUALITY CLASSIFICATION
# =========================

if gas < 800:
    aq = "🟢 VERY GOOD"
    color = "#2E7D32"

    recommendation = """
🟢 Fresh Indoor Environment

The indoor air quality is excellent.

**Recommendations**
- ✅ No immediate action required.
- 🌬 Continue normal ventilation.
- 😊 Environment is comfortable for regular indoor activities.
"""

elif gas < 1500:
    aq = "🟡 GOOD"
    color = "#F9A825"

    recommendation = """
🟡 Good Indoor Air Quality

The indoor environment is healthy with only minor air pollutants.

**Recommendations**
- ✅ Indoor air is acceptable.
- 🌬 Maintain adequate room ventilation.
- 🚪 Open windows occasionally to ensure fresh air circulation.
"""

elif gas < 2200:
    aq = "🟠 SATISFACTORY"
    color = "#EF6C00"

    recommendation = """
🟠 Moderate Indoor Air Quality

Air pollutants are beginning to increase.

**Recommendations**
- 🌬 Improve natural ventilation.
- 🚪 Open nearby windows or doors if possible.
- 📈 Continue monitoring for further changes.
"""

elif gas < 3000:
    aq = "🔴 BAD"
    color = "#C62828"

    recommendation = """
🔴 Poor Indoor Air Quality

The concentration of indoor pollutants is above the recommended level.

**Recommendations**
- 🌬 Improve room ventilation immediately.
- 🚪 Open windows and doors.
- ⏳ Avoid staying in the room for prolonged periods.
- ⚠ Investigate possible pollution sources.
"""

else:
    aq = "☠️ HAZARDOUS"
    color = "#6A1B9A"

    recommendation = """
☠️ Hazardous Indoor Air Quality

Air quality has reached an unsafe level.

**Recommendations**
- 🚨 Immediate ventilation is required.
- 🚪 Leave the room if possible until air quality improves.
- 🔍 Check for smoke, gas leaks, or other pollution sources.
- ⚠ Avoid prolonged exposure.
"""

last_time = latest["created_at"].strftime("%d %b %Y\n%I:%M:%S %p IST")
st.write(f"**🕒 Last Updated:** {last_time}")

c1,c2,c3,c4 = st.columns(4)
c1.metric("🌡 Temperature",f"{temp:.1f} °C")
c2.metric("💧 Humidity",f"{hum:.1f} %")
c3.metric("🧪 Gas Sensor",f"{gas:.0f}")
c4.markdown(
    f"<div class='status-box' style='background:{color};'>{aq}</div>",
    unsafe_allow_html=True
)

st.divider()

# ============================================================
# OVERALL ROOM HEALTH
# ============================================================

st.subheader("🏠 Overall Room Health")

temp_ok = 20 <= temp <= 32
hum_ok = 30 <= hum <= 70
air_ok = gas < 2200

score = sum([temp_ok, hum_ok, air_ok])

if score == 3:
    overall = "HEALTHY"
    overall_color = "#43A047"
    message = "Indoor conditions are within the recommended operating range."

elif score == 2:
    overall = "MODERATE"
    overall_color = "#FB8C00"
    message = "Some environmental parameters require attention."

else:
    overall = "NEEDS ATTENTION"
    overall_color = "#E53935"
    message = "Indoor conditions are outside the recommended operating range."

temp_text = "Comfortable" if temp_ok else "Outside Comfort Range"
temp_color = "#43A047" if temp_ok else "#FB8C00"

hum_text = "Comfortable" if hum_ok else "Outside Comfort Range"
hum_color = "#43A047" if hum_ok else "#FB8C00"

air_text = aq.replace("🟢","").replace("🟡","").replace("🟠","").replace("🔴","").replace("☠️","").strip()

if "VERY GOOD" in air_text:
    air_color = "#43A047"
elif "GOOD" in air_text:
    air_color = "#7CB342"
elif "SATISFACTORY" in air_text:
    air_color = "#FB8C00"
elif "BAD" in air_text:
    air_color = "#E53935"
else:
    air_color = "#8E24AA"

st.markdown(f"""
<div class="room-card">

<div class="room-title" style="color:{overall_color};">
{overall}
</div>

<div class="room-message">
{message}
</div>

<hr class="room-divider">

<div class="parameter-row">
<span class="parameter-label">Temperature</span>
<span style="color:{temp_color};font-weight:600;">{temp_text}</span>
</div>

<div class="parameter-row">
<span class="parameter-label">Humidity</span>
<span style="color:{hum_color};font-weight:600;">{hum_text}</span>
</div>

<div class="parameter-row">
<span class="parameter-label">Air Quality</span>
<span style="color:{air_color};font-weight:600;">{air_text}</span>
</div>

<hr class="room-divider">

<div class="score-box">
<b>Overall Health Score</b><br>
{score} / 3 Parameters Within Recommended Range
</div>

</div>
""", unsafe_allow_html=True)

# ============================================================
# TREND INDICATOR
# ============================================================

st.subheader("📈 Trend Indicator")

if len(df)>=6:
    previous=df["Gas"].iloc[-6:-1].mean()
else:
    previous=df["Gas"].mean()

if gas>previous+50:
    st.error("⬆ Pollution Increasing")
elif gas<previous-50:
    st.success("⬇ Air Quality Improving")
else:
    st.info("➡ Air Quality Stable")

st.subheader("💡 Recommendation")
st.markdown(f"<div class='recommend'>{recommendation}</div>", unsafe_allow_html=True)

st.divider()

# ============================================================
# GRAPHS
# ============================================================

fig1 = px.line(
    df,
    x="created_at",
    y="Temperature",
    title="🌡 Temperature Trend"
)

fig1.update_traces(
    line=dict(color="#E53935", width=3)
)

fig1.update_layout(
    template="plotly_dark",
    margin=dict(l=20, r=20, t=50, b=20)
)

# -------------------------------------------------

fig2 = px.line(
    df,
    x="created_at",
    y="Humidity",
    title="💧 Humidity Trend"
)

fig2.update_traces(
    line=dict(color="#1E88E5", width=3)
)

fig2.update_layout(
    template="plotly_dark",
    margin=dict(l=20, r=20, t=50, b=20)
)

# -------------------------------------------------

fig3 = px.line(
    df,
    x="created_at",
    y="Gas",
    title="🧪 Gas Sensor Trend"
)

fig3.update_traces(
    line=dict(color="#FB8C00", width=3)
)

fig3.update_layout(
    template="plotly_dark",
    margin=dict(l=20, r=20, t=50, b=20)
)

st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
st.plotly_chart(fig3, use_container_width=True)

# ============================================================
# ENVIRONMENTAL SUMMARY
# ============================================================

st.subheader("📊 Environmental Summary")

a,b,c=st.columns(3)
a.metric("Average Temperature",f"{df['Temperature'].mean():.2f} °C")
b.metric("Average Humidity",f"{df['Humidity'].mean():.2f} %")
c.metric("Average Gas Value",f"{df['Gas'].mean():.0f}")

# ============================================================
# SYSTEM STATUS
# ============================================================

st.subheader("🖥 System Status")

status1, status2 = st.columns(2)

with status1:
    st.success("🟢 ESP32 Connected")
    st.success("🟢 Sensors Operational")

with status2:
    st.success("🟢 ThingSpeak Cloud Online")
    st.success("🟢 Data Logging Active")

# ============================================================
# RECENT SENSOR LOGS
# ============================================================

st.subheader("📋 Recent Sensor Logs")

table=df[["created_at","Temperature","Humidity","Gas"]].copy()

def classify(v):
    if v<800:return "🟢 Very Good"
    if v<1500:return "🟡 Good"
    if v<2200:return "🟠 Satisfactory"
    if v<3000:return "🔴 Bad"
    return "☠️ Hazardous"

table["AQ Status"]=table["Gas"].apply(classify)
table["created_at"]=table["created_at"].dt.strftime("%d-%m %H:%M:%S")

st.dataframe(
    table.sort_index(ascending=False),
    use_container_width=True,
    hide_index=True
)

st.markdown("---")
st.markdown("""
<div class='footer'>
<b>Developed By</b><br>
Ashmit Gupta • Ayush Raj<br><br>
Department of Electronics & Communication Engineering<br>
UIET, Panjab University<br><br>
Powered by ESP32 • DHT22 • MQ135 • ThingSpeak • Streamlit
</div>
""", unsafe_allow_html=True)
