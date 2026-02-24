import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster, HeatMap
import plotly.express as px

# Set page config for a premium feel
st.set_page_config(
    page_title="SafeBD | Incident Tracker",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for high-end LIGHT aesthetics
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .main {
        background-color: #f8fafc;
    }

    /* Modern Light Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    /* Elegant Metric Cards */
    div[data-testid="stMetric"] {
        background: #ffffff;
        padding: 24px;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: all 0.3s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
        border-color: #10b981;
    }

    /* Typography & Branding */
    .main-title {
        font-weight: 800;
        color: #1e293b;
        font-size: 3rem;
        letter-spacing: -0.025em;
        margin-bottom: 0rem;
    }
    .brand-accent {
        color: #10b981;
    }
    
    .status-badge {
        background: #ecfdf5;
        color: #059669;
        padding: 4px 12px;
        border-radius: 99px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid #d1fae5;
    }

    /* Custom Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        color: #64748b;
        font-weight: 600;
        font-size: 1rem;
    }
    .stTabs [aria-selected="true"] {
        color: #10b981 !important;
        border-bottom-color: #10b981 !important;
    }
</style>
""", unsafe_allow_html=True)

# Load data
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vROsLYRpCh6rUAQFbNcXtTHKpeFFPyWzlQmniXa1DL7BVKeeHkl8-Ml-924kHzpRiUV__q0lD8C10FZ/pub?output=csv"

@st.cache_data(ttl=3600)
def load_data(url):
    df = pd.read_csv(url)
    df['Killed'] = pd.to_numeric(df['Killed'], errors='coerce').fillna(0)
    df['Injured'] = pd.to_numeric(df['Injured'], errors='coerce').fillna(0)
    df['Casualties'] = df['Killed'] + df['Injured']
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    return df

try:
    df = load_data(sheet_url)
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

# Header Section
col_head, col_status = st.columns([3, 1])
with col_head:
    st.markdown('<h1 class="main-title">SafeBD <span class="brand-accent">Tracker</span></h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #64748b; font-size: 1.1rem; margin-top: -10px;">Keeping track of public security incidents across Bangladesh</p>', unsafe_allow_html=True)
with col_status:
    st.markdown('<div style="text-align: right; margin-top: 25px;"><span class="status-badge">● LIVE INTELLIGENCE</span></div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### �️ Strategic Filters")
    st.write("Refine your view of the operational landscape.")
    
    st.subheader("📅 Date Range")
    min_date = df['Date'].min().date() if not df['Date'].isna().all() else None
    max_date = df['Date'].max().date() if not df['Date'].isna().all() else None

    if min_date and max_date:
        date_range = st.date_input(
            "Observation Period",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        if len(date_range) == 2:
            start_date, end_date = date_range
            df_filtered = df[(df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)]
        else:
            df_filtered = df
    else:
        df_filtered = df

    st.subheader("👥 Active Entities")
    all_groups = sorted(df['Group'].unique().astype(str))
    selected_groups = st.multiselect("Select Group(s)", options=all_groups, default=all_groups)

# Final filter
df_final = df_filtered[df_filtered['Group'].isin(selected_groups)]

# Metrics Section
st.markdown("### 📊 Operational Overview")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Incidents", len(df_final))
m2.metric("Fatalities", int(df_final['Killed'].sum()))
m3.metric("Injuries", int(df_final['Injured'].sum()))
m4.metric("Total Casualties", int(df_final['Casualties'].sum()))

# Main Display
tab1, tab2, tab3 = st.tabs(["🌎 Geospatial View", "📉 Advanced Analysis", "� Incident Logs"])

with tab1:
    st.subheader("Incident Distribution Map")
    
    # Modern Light Map configuration
    m = folium.Map(
        location=[23.6850, 90.3563], 
        zoom_start=7, 
        tiles='CartoDB Positron',  # Light premium tiles
        zoom_control=True,
    )
    
    if not df_final.empty:
        # Heatmap Layer (Refined for light mode)
        heat_data = [[row['Latitude'], row['Longitude'], row['Casualties']] for _, row in df_final.iterrows()]
        HeatMap(heat_data, radius=20, blur=25, min_opacity=0.3, gradient={0.4: '#34d399', 0.65: '#f59e0b', 1: '#ef4444'}).add_to(m)

        # Custom Cluster
        marker_cluster = MarkerCluster(name="Incidents").add_to(m)
        for _, row in df_final.iterrows():
            popup_html = f"""
            <div style="font-family: 'Plus Jakarta Sans', sans-serif; padding: 12px; width: 240px; background: #fff; border-radius: 12px;">
                <h6 style="margin:0; color: #059669; font-weight: 700;">{row['Group']}</h6>
                <div style="margin-top: 8px; font-size: 0.85rem; color: #475569;">
                    <b>📅 Date:</b> {row['Date'].strftime('%d %b %Y') if pd.notnull(row['Date']) else 'N/A'}<br>
                    <b>📍 Location:</b> {row['Location']}<br>
                    <b>🎯 Target:</b> {row['Target/Event']}
                </div>
                <hr style="margin: 10px 0; border: none; border-top: 1px solid #f1f5f9;">
                <div style="display: flex; gap: 10px;">
                    <span style="color: #ef4444; font-weight: 600;">K: {int(row['Killed'])}</span>
                    <span style="color: #3b82f6; font-weight: 600;">I: {int(row['Injured'])}</span>
                </div>
            </div>
            """
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=7,
                color="#10b981",
                weight=1,
                fill=True,
                fill_color="#10b981",
                fill_opacity=0.5,
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{row['Group']} | {int(row['Casualties'])} casualties"
            ).add_to(marker_cluster)

        st_folium(m, width="100%", height=650, use_container_width=True)
    else:
        st.info("Adjust filters to display geospatial intelligence.")

with tab2:
    st.subheader("Strategic Insights")
    c1, c2 = st.columns(2)
    
    with c1:
        # Sunburst Chart for hierarchical view
        fig_sun = px.sunburst(
            df_final,
            path=['Group', 'Target/Event'],
            values='Casualties',
            title='Casualty Hierarchy: Group & Target Type',
            color='Casualties',
            color_continuous_scale='GnBu',
            template="plotly_white"
        )
        fig_sun.update_layout(margin=dict(t=40, l=0, r=0, b=0))
        st.plotly_chart(fig_sun, use_container_width=True)

    with c2:
        # Scatter Plot for intensity comparison
        fig_scatter = px.scatter(
            df_final,
            x='Killed',
            y='Injured',
            size='Casualties',
            color='Group',
            hover_name='Location',
            title='Incident Intensity Comparison',
            labels={'Killed': 'Fatalities', 'Injured': 'Injuries'},
            template="plotly_white"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Full width Timeline
    st.markdown("---")
    if not df_final.empty:
        timeline = df_final.sort_values('Date').set_index('Date').resample('QE').sum().reset_index()
        fig_trend = px.line(
            timeline, 
            x='Date', 
            y='Casualties',
            title='Quarterly Impact Trend',
            markers=True,
            line_shape='spline',
            template="plotly_white"
        )
        fig_trend.update_traces(line_color='#10b981', fill='tozeroy')
        st.plotly_chart(fig_trend, use_container_width=True)

with tab3:
    st.subheader("Incident Ledger")
    st.write("Browse and export filtered operational records.")
    st.dataframe(
        df_final[['Date', 'Group', 'Location', 'Target/Event', 'Killed', 'Injured', 'Notes']],
        use_container_width=True,
        hide_index=True
    )

# Footer
st.markdown("""
<div style="background-color: #ffffff; padding: 24px; border-radius: 12px; border: 1px solid #e2e8f0; margin-top: 40px; text-align: center;">
    <p style="color: #64748b; font-size: 0.9rem; margin: 0;">
        Built for Modern Security Analytics • Data Source: National Incident Records • 🛡️ Sentinel v2.5
    </p>
</div>
""", unsafe_allow_html=True)

