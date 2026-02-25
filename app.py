import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster, HeatMap, Fullscreen, MiniMap, Search
import plotly.express as px
import re

# Set page config for a premium feel
st.set_page_config(
    page_title="False Flag Watch | Reporting",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="collapsed"
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
    
    /* MOBILE OPTIMIZATION */
    @media (max-width: 768px) {
        .main-title {
            font-size: 1.8rem !important;
        }
        div[data-testid="stMetric"] {
            padding: 15px !important;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 0.8rem !important;
            padding: 10px !important;
        }
        .metric-container {
            flex-direction: column !important;
        }
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
    
    # Robust numeric conversion
    def clean_numeric(x):
        if pd.isna(x): return 0
        val = re.sub(r'[^0-9]', '', str(x))
        return int(val) if val else 0

    df['Killed'] = df['Killed'].apply(clean_numeric)
    df['Injured'] = df['Injured'].apply(clean_numeric)
    df['Casualties'] = df['Killed'] + df['Injured']
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    # Fill missing group names
    df['Group'] = df['Group'].fillna('Unknown').replace('', 'Unknown')
    
    return df

try:
    df = load_data(sheet_url)
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

# Header Section
col_head, col_status = st.columns([3, 1])
with col_head:
    st.markdown('<h1 class="main-title">False Flag <span class="brand-accent">Watch</span></h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #64748b; font-size: 1rem; margin-top: -10px;">National Security Incident Monitoring & Verification System</p>', unsafe_allow_html=True)
with col_status:
    st.markdown('<div style="text-align: right; margin-top: 15px;"><span class="status-badge">● ANALYSIS LIVE</span></div>', unsafe_allow_html=True)

# Sidebar
    st.markdown("### � Research Parameters")
    st.write("Configure the scope of documentation and analysis.")
    
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
df_final = df_filtered[df_filtered['Group'].isin(selected_groups)].copy()

# Metrics Section
st.markdown("### 📊 Operational Overview")
m1, m2, m3, m4 = st.columns(4)

# Enhanced Metric Display
def styled_metric(label, value, delta=None, color="#10b981"):
    st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 15px; border-left: 5px solid {color}; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
            <p style="color: #64748b; font-size: 0.8rem; margin: 0; text-transform: uppercase; letter-spacing: 1px;">{label}</p>
            <h2 style="margin: 0; color: #1e293b; font-weight: 800;">{value}</h2>
        </div>
    """, unsafe_allow_html=True)

with m1: styled_metric("Total Incidents", len(df_final), color="#3b82f6")
with m2: styled_metric("Fatalities", int(df_final['Killed'].sum()), color="#ef4444")
with m3: styled_metric("Injuries", int(df_final['Injured'].sum()), color="#f59e0b")
with m4: styled_metric("Total Impact", int(df_final['Casualties'].sum()), color="#8b5cf6")

# Main Display
tab1, tab2, tab3 = st.tabs(["🌎 Geospatial Intelligence", "📉 Behavioral Analysis", "📑 Intelligence Ledger"])

with tab1:
    st.subheader("Dynamic Incident Mapping")
    m = folium.Map(location=[23.6850, 90.3563], zoom_start=7, tiles='CartoDB Positron')
    folium.TileLayer('CartoDB DarkMatter', name='Dark Mode').add_to(m)
    
    if not df_final.empty:
        heat_data = [[row['Latitude'], row['Longitude'], row['Casualties']] for _, row in df_final.iterrows()]
        HeatMap(heat_data, name="Intensity Heatmap", radius=20, blur=25, min_opacity=0.3, gradient={0.4: '#34d399', 0.65: '#f59e0b', 1: '#ef4444'}).add_to(m)
        
        marker_cluster = MarkerCluster(name="Detailed Incidents").add_to(m)
        for _, row in df_final.iterrows():
            popup_html = f"""
            <div style="font-family: 'Plus Jakarta Sans', sans-serif; padding: 12px; width: 240px; background: #fff; border-radius: 12px;">
                <h6 style="margin:0; color: #059669; font-weight: 700;">{row['Group']}</h6>
                <div style="margin-top: 8px; font-size: 0.85rem; color: #475569;">
                    <b>📅 Date:</b> {row['Date'].strftime('%d %b %Y') if pd.notnull(row['Date']) else 'N/A'}<br>
                    <b>📍 Location:</b> {row['Location']}<br>
                    <b>🎯 Target:</b> {row.get('Target/Event', 'N/A')}
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
                radius=8, color="#10b981", fill=True, fill_color="#10b981", fill_opacity=0.6,
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{row['Group']} | {int(row['Casualties'])} casualties"
            ).add_to(marker_cluster)
        
        Fullscreen().add_to(m)
        MiniMap(toggle_display=True).add_to(m)
        Search(layer=marker_cluster, geom_type='Point', placeholder='Find group...', search_label='Group').add_to(m)
        folium.LayerControl().add_to(m)
        st_folium(m, width="100%", height=600, use_container_width=True)
    else:
        st.info("No data available for the selected filters.")

with tab2:
    st.subheader("Statistical Patterns & Investigative Insights")
    
    # Grid Row 1: Hierarchical & Distribution
    col1, col2 = st.columns(2)
    with col1:
        # Sunburst Chart (RESTORED)
        target_col = 'Target/Event' if 'Target/Event' in df_final.columns else 'Location'
        fig_sun = px.sunburst(
            df_final, path=['Group', target_col], values='Casualties',
            title='Casualty Hierarchy: Group & Target Type',
            color='Casualties', color_continuous_scale='GnBu',
            template="plotly_white"
        )
        fig_sun.update_layout(margin=dict(t=40, l=0, r=0, b=0))
        st.plotly_chart(fig_sun, use_container_width=True)
    
    with col2:
        # Top Active Groups (Bar chart)
        top_groups = df_final.groupby('Group')['Casualties'].sum().sort_values(ascending=False).head(10).reset_index()
        fig_groups = px.bar(
            top_groups, x='Casualties', y='Group', orientation='h',
            title='Top 10 High-Impact Entities',
            color='Casualties', color_continuous_scale='Reds',
            template="plotly_white", text_auto=True
        )
        fig_groups.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_groups, use_container_width=True)

    # Grid Row 2: Intensity Scatter & Proportional Impact
    col3, col4 = st.columns(2)
    with col3:
        # Scatter Plot (RESTORED)
        fig_scatter = px.scatter(
            df_final, x='Killed', y='Injured', size='Casualties', color='Group',
            hover_name='Location', title='Incident Intensity Comparison',
            labels={'Killed': 'Fatalities', 'Injured': 'Injuries'},
            template="plotly_white"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col4:
        # Impact Distribution (Pie chart)
        fig_dist = px.pie(
            df_final, values='Casualties', names='Group',
            title='Proportional Impact Distribution',
            hole=0.4, template="plotly_white"
        )
        fig_dist.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_dist, use_container_width=True)
    
    # Grid Row 3: Full Width Timeline
    st.markdown("---")
    if not df_final.empty:
        df_final_clean = df_final.dropna(subset=['Date'])
        if not df_final_clean.empty:
            timeline = df_final_clean.set_index('Date').resample('QE').sum().reset_index()
            fig_trend = px.area(
                timeline, x='Date', y='Casualties',
                title='Quarterly Casualty Trajectory',
                template="plotly_white", color_discrete_sequence=['#ef4444']
            )
            st.plotly_chart(fig_trend, use_container_width=True)

with tab3:
    st.subheader("Incident Ledger")
    
    # Export Control
    csv = df_final.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Intel (CSV)",
        data=csv,
        file_name="safebd_intelligence_export.csv",
        mime="text/csv",
    )
    
    st.dataframe(
        df_final[['Date', 'Group', 'Location', 'Killed', 'Injured', 'Notes']],
        use_container_width=True,
        hide_index=True
    )


# Footer
st.markdown("""
<div style="background-color: #ffffff; padding: 24px; border-radius: 12px; border: 1px solid #e2e8f0; margin-top: 40px; text-align: center;">
    <p style="color: #64748b; font-size: 0.8rem; margin: 0;">
        False Flag Watch v4.5 • Investigative Reporting Portal
    </p>
</div>
""", unsafe_allow_html=True)


