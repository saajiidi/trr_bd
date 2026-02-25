import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster, HeatMap, Fullscreen, MiniMap, Search
import plotly.express as px
import re

# Theme & Data State Management
if 'theme' not in st.session_state:
    st.session_state.theme = 'Light'
if 'world_url' not in st.session_state:
    st.session_state.world_url = "https://raw.githubusercontent.com/lschlessinger1/Global-Terrorism-Database-K-Means/master/clean_data.csv"

# Set page config
st.set_page_config(
    page_title="False Flag Watch | Reporting",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for high-end aesthetics
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    :root {{
        --primary: #10b981;
        --primary-soft: { '#064e3b' if st.session_state.theme == 'Dark' else '#ecfdf5' };
        --bg-main: { '#0f172a' if st.session_state.theme == 'Dark' else '#f8fafc' };
        --card-bg: { 'rgba(30, 41, 59, 0.7)' if st.session_state.theme == 'Dark' else 'rgba(255, 255, 255, 0.8)' };
        --border-color: { '#334155' if st.session_state.theme == 'Dark' else '#e2e8f0' };
        --text-main: { '#f1f5f9' if st.session_state.theme == 'Dark' else '#1e293b' };
        --text-muted: { '#94a3b8' if st.session_state.theme == 'Dark' else '#64748b' };
    }}

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: var(--text-main);
    }}

    .stApp {{
        background: var(--bg-main);
        transition: background 0.3s ease;
    }}

    /* Modern Glassmorphism Cards */
    .glass-card {{
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
        transition: all 0.3s ease;
        margin-bottom: 12px;
    }}
    .glass-card:hover {{
        transform: translateY(-2px);
        border-color: var(--primary);
    }}

    /* Metric Customization */
    div[data-testid="stMetric"] {{
        background: transparent !important;
    }}
    div[data-testid="stMetricValue"] > div {{
        color: var(--text-main) !important;
    }}
    div[data-testid="stMetricLabel"] > div {{
        color: var(--text-muted) !important;
    }}

    /* Typography & Branding */
    .brand-title {{
        background: { 'linear-gradient(135deg, #f1f5f9 0%, #cbd5e1 100%)' if st.session_state.theme == 'Dark' else 'linear-gradient(135deg, #1e293b 0%, #334155 100%)' };
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }}

    .status-badge {{
        background: var(--primary-soft);
        color: var(--primary);
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 0.7rem;
        font-weight: 700;
        border: 1px solid var(--primary);
    }}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: { '#1e293b' if st.session_state.theme == 'Dark' else '#ffffff' };
        border-right: 1px solid var(--border-color);
    }}

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 4px;
        background-color: { '#1e293b' if st.session_state.theme == 'Dark' else '#f1f5f9' };
        padding: 4px;
        border-radius: 12px;
        margin-bottom: 20px;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        color: var(--text-muted);
    }}
    .stTabs [aria-selected="true"] {{
        background-color: { '#334155' if st.session_state.theme == 'Dark' else '#ffffff' } !important;
        color: var(--primary) !important;
    }}
    
    /* Header optimization */
    .header-container {{
        margin-bottom: 15px !important;
        padding-top: 5px !important;
    }}

    /* Hide Default Elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

# Data Loaders
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vROsLYRpCh6rUAQFbNcXtTHKpeFFPyWzlQmniXa1DL7BVKeeHkl8-Ml-924kHzpRiUV__q0lD8C10FZ/pub?output=csv"

@st.cache_data(ttl=3600)
def load_data(url):
    try:
        df = pd.read_csv(url)
        # Robust numeric conversion
        def clean_numeric(x):
            if pd.isna(x): return 0
            val = re.sub(r'[^0-9]', '', str(x))
            return int(val) if val else 0

        df['Killed'] = df['Killed'].apply(clean_numeric)
        df['Injured'] = df['Injured'].apply(clean_numeric)
        df['Casualties'] = df['Killed'] + df['Injured']
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Group'] = df['Group'].fillna('Unknown').replace('', 'Unknown')
        return df
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_world_data(url):
    try:
        w_df = pd.read_csv(url)
        rename_map = {
            'latitude': 'Latitude', 'longitude': 'Longitude', 
            'nkill': 'Killed', 'nwound': 'Injured',
            'gname': 'Group', 'city': 'Location',
            'iyear': 'Year'
        }
        w_df = w_df.rename(columns=rename_map)
        w_df['Latitude'] = pd.to_numeric(w_df.get('Latitude'), errors='coerce')
        w_df['Longitude'] = pd.to_numeric(w_df.get('Longitude'), errors='coerce')
        w_df = w_df.dropna(subset=['Latitude', 'Longitude'])
        w_df['Killed'] = pd.to_numeric(w_df.get('Killed'), errors='coerce').fillna(0)
        w_df['Injured'] = pd.to_numeric(w_df.get('Injured'), errors='coerce').fillna(0)
        w_df['Casualties'] = w_df['Killed'] + w_df['Injured']
        return w_df
    except Exception:
        return pd.DataFrame()

df = load_data(sheet_url)
world_df_raw = load_world_data(st.session_state.world_url)

# Header Section
col_head, col_status = st.columns([3, 1])
with col_head:
    st.markdown("""
        <div class="header-container" style="display: flex; align-items: center; gap: 16px;">
            <div style="background: var(--card-bg); padding: 10px; border-radius: 16px; border: 1px solid var(--border-color);">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2L4 5V11C4 16.19 7.41 21.05 12 22C16.59 21.05 20 16.19 20 11V5L12 2Z" fill="#10B981" fill-opacity="0.2"/>
                    <path d="M12 2L4 5V11C4 16.19 7.41 21.05 12 22C16.59 21.05 20 16.19 20 11V5L12 2Z" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <circle cx="12" cy="11" r="4" stroke="#1E293B" stroke-width="2"/>
                </svg>
            </div>
            <div>
                <h1 class="brand-title" style="font-size: 2.2rem; margin: 0; line-height: 1.1;">
                    False Flag <span style="color: #10b981;">Watch</span>
                </h1>
                <p style="color: var(--text-muted); font-size: 0.95rem; margin-top: 2px;">Verification & Reporting Framework</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
with col_status:
    st.markdown('<div style="text-align: right; padding-top: 15px;"><span class="status-badge">● INFRASTRUCTURE READY</span></div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎨 Visual Theme")
    st.session_state.theme = st.radio("Interface Mode", ["Light", "Dark"], index=0 if st.session_state.theme == 'Light' else 1, horizontal=True)
    
    st.markdown("### 🌐 Global Parameters")
    st.session_state.world_url = st.text_input("World Dataset (CSV URL)", value=st.session_state.world_url)
    
    st.markdown("### 📋 National Parameters")
    if not df.empty:
        min_date = df['Date'].min().date() if not df['Date'].isna().all() else None
        max_date = df['Date'].max().date() if not df['Date'].isna().all() else None

        if min_date and max_date:
            date_range = st.date_input("Observation Period", value=(min_date, max_date), min_value=min_date, max_value=max_date)
            if len(date_range) == 2:
                start_date, end_date = date_range
                df_filtered = df[(df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)]
            else:
                df_filtered = df
        else:
            df_filtered = df

        all_groups = sorted(df['Group'].unique().astype(str))
        selected_groups = st.multiselect("Active Entities", options=all_groups, default=all_groups)
        df_final = df_filtered[df_filtered['Group'].isin(selected_groups)].copy()
    else:
        df_final = pd.DataFrame()

# World Filter
if not world_df_raw.empty:
    world_df = world_df_raw.tail(2000).copy()
else:
    world_df = pd.DataFrame()

# Operational Overview
st.markdown("### 📊 Operational Overview")
m1, m2, m3, m4 = st.columns(4)

def styled_metric(label, value, color="#10b981"):
    st.markdown(f"""
        <div class="glass-card">
            <p style="color: var(--text-muted); font-size: 0.75rem; margin: 0; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700;">{label}</p>
            <h2 style="margin: 5px 0 0 0; color: var(--text-main); font-weight: 800; font-size: 2rem;">{value}</h2>
            <div style="height: 3px; width: 30px; background: {color}; border-radius: 2px; margin-top: 8px;"></div>
        </div>
    """, unsafe_allow_html=True)

if not df_final.empty:
    with m1: styled_metric("Events Logs", f"{len(df_final):,}", color="#3b82f6")
    with m2: styled_metric("Fatalities", f"{int(df_final['Killed'].sum()):,}", color="#ef4444")
    with m3: styled_metric("Injuries", f"{int(df_final['Injured'].sum()):,}", color="#f59e0b")
    with m4: styled_metric("Total Impact", f"{int(df_final['Casualties'].sum()):,}", color="#8b5cf6")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🌎 National View", "📉 Analysis", "📑 Ledger", "🌐 World Surveillance"])

with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Interactive Event Mapping")
    if not df_final.empty:
        map_tiles = 'CartoDB DarkMatter' if st.session_state.theme == 'Dark' else 'CartoDB Positron'
        m = folium.Map(location=[23.6850, 90.3563], zoom_start=7, tiles=map_tiles)
        heat_data = [[row['Latitude'], row['Longitude'], row['Casualties']] for _, row in df_final.iterrows()]
        HeatMap(heat_data, name="Intensity", radius=20, blur=25).add_to(m)
        w_cluster = MarkerCluster(name="Markers").add_to(m)
        for _, row in df_final.iterrows():
            popup_html = f"<b>{row['Group']}</b><br>{row['Location']}<br>K: {int(row['Killed'])} | I: {int(row['Injured'])}"
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=8, color="#10b981", fill=True,
                popup=folium.Popup(popup_html, max_width=250)
            ).add_to(w_cluster)
        Fullscreen().add_to(m)
        st_folium(m, width="100%", height=600, key="nat_map")
    else:
        st.info("No data available.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    plotly_template = "plotly_dark" if st.session_state.theme == "Dark" else "plotly_white"
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if not df_final.empty:
            fig_sun = px.sunburst(df_final, path=['Group', 'Location'], values='Casualties', title='Hierarchy', template=plotly_template)
            fig_sun.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_sun, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if not df_final.empty:
            top = df_final.groupby('Group')['Casualties'].sum().sort_values(ascending=False).head(10).reset_index()
            fig_bar = px.bar(top, x='Casualties', y='Group', orientation='h', title='Top Entities', template=plotly_template)
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if not df_final.empty:
        st.dataframe(df_final[['Date', 'Group', 'Location', 'Killed', 'Injured', 'Notes']], use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Global Security Surveillance")
    if not world_df.empty:
        col_w1, col_w2, col_w3 = st.columns(3)
        col_w1.metric("World Logs", f"{len(world_df):,}")
        col_w2.metric("Fatalities", f"{int(world_df['Killed'].sum()):,}")
        col_w3.metric("Impact", f"{int(world_df['Casualties'].sum()):,}")
        map_tiles = 'CartoDB DarkMatter' if st.session_state.theme == 'Dark' else 'CartoDB Positron'
        wm = folium.Map(location=[20, 0], zoom_start=2, tiles=map_tiles)
        w_heat_data = [[row['Latitude'], row['Longitude'], row['Casualties']] for _, row in world_df.iterrows()]
        HeatMap(w_heat_data, radius=15).add_to(wm)
        st_folium(wm, width="100%", height=600, key="world_map")
    else:
        st.warning("Update Global CSV URL in sidebar.")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="background-color: var(--card-bg); padding: 20px; border-radius: 12px; border: 1px solid var(--border-color); margin-top: 40px; text-align: center;">
    <p style="color: var(--text-muted); font-size: 0.8rem; margin: 0;">
        False Flag Watch v5.0 • World Surveillance Unified Edition
    </p>
</div>
""", unsafe_allow_html=True)
