# 🌍 Smart Indoor Air Quality Monitoring System

> **An IoT-Based Real-Time Indoor Air Quality Monitoring System**  
> **Semester 6 Project | B.E. Electronics & Communication Engineering**  
> UIET, Panjab University

---

## 📖 Project Overview

Indoor air quality plays a crucial role in health, comfort, and productivity. This project presents a **low-cost IoT-based Indoor Air Quality Monitoring System** capable of continuously monitoring environmental parameters and visualizing them through a cloud-connected dashboard.

Unlike conventional sensor projects that only display raw values locally, this system demonstrates a complete **IoT pipeline** by collecting sensor data, uploading it to the cloud, and presenting meaningful insights through a modern web dashboard.

The system monitors:

- 🌡 Temperature
- 💧 Humidity
- 🧪 Indoor Air Quality (MQ135 Gas Sensor)

The collected data is transmitted over Wi-Fi using an **ESP32**, stored on **ThingSpeak**, and visualized using a **Streamlit Dashboard**.

---

## 🚀 Live Dashboard

🌐 **Streamlit Dashboard**

https://smart-indoor-air-quality-monitoring-system-hgrmkxmsghtqxvwp4hg.streamlit.app/

---

## ✨ Features

- 📡 Real-time sensor monitoring
- ☁ Cloud data logging using ThingSpeak
- 📊 Historical trend visualization
- 🌍 Overall Room Health Assessment
- 🟢 Air Quality Classification
- 💡 Intelligent recommendations based on sensor readings
- 📈 Environmental statistics
- 🖥 System status monitoring
- 📋 Recent sensor logs
- 🔄 Automatic dashboard refresh

---

## 🛠 Hardware Used

- ESP32 Development Board
- DHT22 Temperature & Humidity Sensor
- MQ135 Gas Sensor
- Breadboard
- Jumper Wires

---

## 💻 Software & Technologies

- Arduino IDE
- ESP32 Arduino Framework
- Python
- Streamlit
- ThingSpeak Cloud
- Plotly
- Pandas

---

## 🏗 System Architecture

```text
        DHT22               MQ135
           │                   │
           └────────┬──────────┘
                    │
               ESP32 Dev Board
                    │
              Wi-Fi Communication
                    │
             ThingSpeak Cloud
                    │
          Streamlit Dashboard
                    │
                  User
```

---

## ⚙ Working Principle

1. DHT22 measures **temperature** and **humidity**.
2. MQ135 measures the **relative concentration of indoor gases**.
3. ESP32 reads both sensors.
4. Sensor readings are uploaded to **ThingSpeak** over Wi-Fi.
5. The Streamlit application periodically fetches the latest data.
6. The dashboard displays:
   - Live sensor values
   - Historical graphs
   - Air quality category
   - Overall room health
   - Recommendations
   - Recent sensor logs

---

## 📷 Project Demonstration

*(Add hardware photographs, dashboard screenshots, and demonstration GIFs here.)*

---

## 📊 Dashboard Highlights

- Real-Time Environmental Monitoring
- Historical Trend Analysis
- Automatic Air Quality Classification
- Overall Room Health Evaluation
- Recommendation Engine
- Interactive Graphs
- Cloud-Based Data Logging
- Responsive Web Dashboard

---

## 📌 Project Limitations

- MQ135 requires proper calibration for higher accuracy.
- The system is intended for **indoor environmental monitoring**.
- Air Quality is estimated using MQ135 and should **not be considered an official AQI measurement**.
- Internet connectivity is required for cloud synchronization.

---

## 🔮 Future Scope

- PM2.5 Dust Sensor Integration
- NDIR CO₂ Sensor
- Mobile Application
- Push Notifications
- AI-Based Air Quality Prediction
- Home Automation Integration
- Battery Backup
- Multi-room Monitoring

---

## 👨‍💻 Authors

**Ashmit Gupta**

Department of Electronics & Communication Engineering

UIET, Panjab University

---

## 📜 Academic Information

This project was developed as a **Semester 6 Mini Project** for the Bachelor of Engineering (Electronics & Communication Engineering).

---

## ⭐ If you found this project interesting, consider giving it a star!
