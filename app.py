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
    
    :root {
        --primary: #10b981;
        --primary-soft: #ecfdf5;
        --bg-main: #f8fafc;
        --card-bg: rgba(255, 255, 255, 0.8);
        --border-color: #e2e8f0;
        --text-main: #1e293b;
        --text-muted: #64748b;
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(16, 185, 129, 0.03) 0%, transparent 40%),
                    radial-gradient(circle at 90% 80%, rgba(59, 130, 246, 0.03) 0%, transparent 40%),
                    var(--bg-main);
    }

    /* Modern Glassmorphism Cards */
    .glass-card {
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px -1px rgba(0, 0, 0, 0.01);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 20px;
    }
    .glass-card:hover {
        transform: translateY(-4px) scale(1.005);
        border-color: var(--primary);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.02);
    }

    /* Metric Customization */
    div[data-testid="stMetric"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }

    /* Typography & Branding */
    .brand-title {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -0.04em;
    }

    .status-badge {
        background: var(--primary-soft);
        color: #059669;
        padding: 6px 14px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border: 1px solid #d1fae5;
        box-shadow: 0 2px 4px rgba(16, 185, 129, 0.1);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid var(--border-color);
    }
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--text-main);
        font-weight: 700;
        margin-top: 20px;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f1f5f9;
        padding: 6px;
        border-radius: 16px;
        margin-bottom: 30px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        border-radius: 12px;
        padding: 0 24px;
        background-color: transparent;
        border: none;
        color: var(--text-muted);
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: var(--primary) !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--primary);
    }
    
    /* Hide Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 24px; margin-bottom: 30px;">
            <div style="background: white; padding: 12px; border-radius: 20px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2L4 5V11C4 16.19 7.41 21.05 12 22C16.59 21.05 20 16.19 20 11V5L12 2Z" fill="#10B981" fill-opacity="0.1"/>
                    <path d="M12 2L4 5V11C4 16.19 7.41 21.05 12 22C16.59 21.05 20 16.19 20 11V5L12 2Z" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <circle cx="12" cy="11" r="4" stroke="#1E293B" stroke-width="2"/>
                    <path d="M15 14L18 17" stroke="#1E293B" stroke-width="2" stroke-linecap="round"/>
                </svg>
            </div>
            <div>
                <h1 class="brand-title" style="font-size: 3rem; margin: 0; line-height: 1;">
                    False Flag <span style="color: #10b981;">Watch</span>
                </h1>
                <p style="color: #64748b; font-size: 1.1rem; margin-top: 5px; font-weight: 500;">National Security Verification & Reporting Framework</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
with col_status:
    st.markdown('<div style="text-align: right; padding-top: 10px;"><span class="status-badge">● INFRASTRUCTURE READY</span></div>', unsafe_allow_html=True)

# Sidebar
    st.markdown("### 📋 Research Parameters")
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
def styled_metric(label, value, color="#10b981"):
    st.markdown(f"""
        <div class="glass-card">
            <p style="color: #64748b; font-size: 0.8rem; margin: 0; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700;">{label}</p>
            <h2 style="margin: 5px 0 0 0; color: #1e293b; font-weight: 800; font-size: 2.2rem;">{value}</h2>
            <div style="height: 4px; width: 40px; background: {color}; border-radius: 2px; margin-top: 10px;"></div>
        </div>
    """, unsafe_allow_html=True)

with m1: styled_metric("Total Events", f"{len(df_final):,}", color="#3b82f6")
with m2: styled_metric("Fatalities", f"{int(df_final['Killed'].sum()):,}", color="#ef4444")
with m3: styled_metric("Injuries", f"{int(df_final['Injured'].sum()):,}", color="#f59e0b")
with m4: styled_metric("Total Impact", f"{int(df_final['Casualties'].sum()):,}", color="#8b5cf6")

# Main Display
tab1, tab2, tab3 = st.tabs(["🌎 Geospatial Intelligence", "📉 Behavioral Analysis", "📑 Intelligence Ledger"])

with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Interactive Event Mapping")
    # ... (Folium implementation)
    m = folium.Map(location=[23.6850, 90.3563], zoom_start=7, tiles='CartoDB Positron')
    folium.TileLayer('CartoDB DarkMatter', name='Dark Mode').add_to(m)
    
    if not df_final.empty:
        heat_data = [[row['Latitude'], row['Longitude'], row['Casualties']] for _, row in df_final.iterrows()]
        HeatMap(heat_data, name="Intensity Heatmap", radius=20, blur=25, min_opacity=0.3, gradient={0.4: '#34d399', 0.65: '#f59e0b', 1: '#ef4444'}).add_to(m)
        
        marker_layer = folium.FeatureGroup(name="Incident Markers")
        marker_cluster = MarkerCluster().add_to(marker_layer)
        for _, row in df_final.iterrows():
            popup_html = f"""
            <div style="font-family: 'Plus Jakarta Sans', sans-serif; padding: 12px; width: 240px; background: #fff; border-radius: 12px;">
                <h6 style="margin:0; color: #10B981; font-weight: 700;">{row['Group']}</h6>
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
                radius=8, color="#10b981", weight=2, fill=True, fill_color="#10b981", fill_opacity=0.6,
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{row['Group']} | {int(row['Casualties'])} casualties"
            ).add_to(marker_cluster)
        
        marker_layer.add_to(m)
        Fullscreen().add_to(m)
        MiniMap(toggle_display=True).add_to(m)
        Search(layer=marker_cluster, geom_type='Point', placeholder='Find group...', search_label='Group').add_to(m)
        folium.LayerControl(collapsed=False).add_to(m)
        st_folium(m, width="100%", height=650, use_container_width=True)
    else:
        st.info("No data available for the selected filters.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("Statistical Patterns & Metrics")
    
    # Restored Sunburst and Scatter Plot with Card Containers
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        target_col = 'Target/Event' if 'Target/Event' in df_final.columns else 'Location'
        fig_sun = px.sunburst(
            df_final, path=['Group', target_col], values='Casualties',
            title='Casualty Hierarchy',
            color='Casualties', color_continuous_scale='GnBu',
            template="plotly_white"
        )
        fig_sun.update_layout(margin=dict(t=40, l=0, r=0, b=0))
        st.plotly_chart(fig_sun, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        top_groups = df_final.groupby('Group')['Casualties'].sum().sort_values(ascending=False).head(10).reset_index()
        fig_groups = px.bar(
            top_groups, x='Casualties', y='Group', orientation='h',
            title='Top High-Impact Entities',
            color='Casualties', color_continuous_scale='Reds',
            template="plotly_white", text_auto=True
        )
        fig_groups.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_groups, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        fig_scatter = px.scatter(
            df_final, x='Killed', y='Injured', size='Casualties', color='Group',
            hover_name='Location', title='Incident Intensity Analysis',
            labels={'Killed': 'Fatalities', 'Injured': 'Injuries'},
            template="plotly_white"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        fig_dist = px.pie(
            df_final, values='Casualties', names='Group',
            title='Impact Distribution',
            hole=0.4, template="plotly_white"
        )
        fig_dist.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_dist, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if not df_final.empty:
        df_final_clean = df_final.dropna(subset=['Date'])
        if not df_final_clean.empty:
            timeline = df_final_clean.set_index('Date').resample('QE').sum().reset_index()
            fig_trend = px.area(
                timeline, x='Date', y='Casualties',
                title='Quarterly Impact Trajectory',
                template="plotly_white", color_discrete_sequence=['#10b981']
            )
            fig_trend.update_layout(margin=dict(t=40, l=10, r=10, b=10))
            st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Event Documentation Ledger")
    
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


