# 📱 PhonePe Analytics Dashboard

Welcome to the **PhonePe Analytics Dashboard**, a Streamlit-powered project that decodes transaction and user behavior data to uncover growth opportunities and digital trends across India.

---

## 📊 Overview

This dashboard visualizes PhonePe data from 2018–2024, enabling stakeholders to:

- 📈 Track transaction growth by state, district, and pincode
- 🧠 Analyze transaction modes and seasonal variations
- 📳 Measure user engagement (registered users vs. app opens)
- 🗺️ Understand device brand impact on user behavior

---

## 🧩 Dashboard Pages

- **Home:** Welcome page introducing the platform and its capabilities  
- **Transaction Dashboard:** Trends across states, quarters, and transaction modes  
- **User Dashboard:** App opens vs. registered users across regions  
- **Dynamics Dashboard:** Deeper transaction behavior insights  
- **Device Dashboard:** User engagement analysis by device brand  
- **District Pincode Dashboard:** Hyperlocal transaction insights by district and pincode  

---

## 💡 Key Insights

- **Market Expansion Potential:** Identify states/districts with high app opens but low user registration.
- **User Engagement Strategy:** Uncover behavior gaps by device and region.
- **Performance Hotspots:** Locate top-performing regions based on transaction value and volume.

---

## 🛠️ Tech Stack

- **Language:** Python
- **Framework:** Streamlit
- **Visualization:** Plotly, Matplotlib
- **Data Handling:** Pandas
- **Version Control:** Git & GitHub

---

## 📁 Folder Structure

phonepe_data_analysis/
│
├── data/ # CSV files (user_data.csv, transaction data, etc.)
├── env/ # Python virtual environment (ignored in Git)
├── pages/ # Streamlit sub-pages (Dashboard scripts)
│ ├── Device_Dashboard.py
│ ├── District_Pincode_Dashboard.py
│ ├── Dynamics_Dashboard.py
│ ├── Transaction_Dashboard.py
│ └── User_Dashboard.py
│
├── pulse/ # PhonePe Pulse data directory (optional)
├── home.py # Main Streamlit entrypoint
└── README.md # This file
