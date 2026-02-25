# SafeBD | Security Research & Reporting Dashboard

A short, accessible, and mobile-friendly platform for security documentation in Bangladesh.

## 🌟 Key Features
*   **Dual-Platform Intelligence**: Choose between a standalone interactive HTML dashboard (R) or a full-featured web app (Python).
*   **Dynamic Geospatial Controls**: Toggle between **Heatmaps**, **Marker Clusters**, and multiple base map styles (Dark Mode, Satellite, Light).
*   **Interactive Filtering**: Filter by casualty count, date range, or responsible group using advanced client-side (Crosstalk) or server-side (Streamlit) logic.
*   **Behavioral Analytics**: In-depth Plotly-powered charts for casualty trajectories, impact distribution, and entity leaderboards.
*   **Search & Navigation**: Integrated search bars for groups and locations, mini-maps for spatial context, and full-screen visualization.
*   **Direct Export**: Download filtered operational data directly as CSV for further reporting.

## 🛠️ Technology Stack
*   **R Language**: `leaflet`, `crosstalk`, `htmlwidgets`, `dplyr`, `htmltools`.
*   **Python**: `streamlit`, `folium`, `plotly`, `pandas`.

## 📂 Project Structure
*   `terrorism_map_bd.R`: Generates the standalone dashboard (`index.html`).
*   `app.py`: The main Streamlit web application.
*   `index.html`: The high-performance, filterable map dashboard (built with R).

## 🚀 Getting Started

### 1. Python Streamlit App
```bash
pip install -r requirements.txt
streamlit run app.py
```

### 2. R Standalone Dashboard
Open `terrorism_map_bd.R` in RStudio and run the entire script. It will generate `index.html` which can be opened in any web browser.

## 📊 Dataset
The intelligence is sourced from a live Google Sheet: [National Incident Tracker](https://docs.google.com/spreadsheets/d/e/2PACX-1vROsLYRpCh6rUAQFbNcXtTHKpeFFPyWzlQmniXa1DL7BVKeeHkl8-Ml-924kHzpRiUV__q0lD8C10FZ/pubhtml).

---
🛡️ **SafeBD v2.5** | Built for Modern Security Analytics
