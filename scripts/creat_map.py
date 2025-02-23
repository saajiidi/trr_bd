import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap

# Load the geocoded dataset
df = pd.read_csv('../data/geocoded_dataset.csv')

# Create a base map centered on Bangladesh
m = folium.Map(location=[23.6850, 90.3563], zoom_start=7)

# Create a marker cluster
marker_cluster = MarkerCluster().add_to(m)

# Define a color mapping for groups
group_colors = {
    "JMB": "red",
    "HJB": "blue",
    "ISG": "green",
    "AQS": "orange"
}

# Add markers to the cluster
for idx, row in df.iterrows():
    if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
        # Create a popup with details
        popup_content = f"""
        <b>Group:</b> {row['Group']}<br>
        <b>Date:</b> {row['Date']}<br>
        <b>Location:</b> {row['Location']}<br>
        <b>Target/Event:</b> {row['Target/Event']}<br>
        <b>Killed:</b> {row['Killed']}<br>
        <b>Injured:</b> {row['Injured']}<br>
        <b>Claimed?:</b> {row['Claimed?']}<br>
        <b>Notes:</b> {row['Notes']}
        """
        popup = folium.Popup(popup_content, max_width=300)

        # Create a tooltip with death toll and injuries
        tooltip_content = f"Killed: {row['Killed']}, Injured: {row['Injured']}"
        tooltip = folium.Tooltip(tooltip_content)

        # Add the marker to the map with color coding
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=popup,
            tooltip=tooltip,
            icon=folium.Icon(color=group_colors.get(row['Group'], "gray"))  # Default to gray if group not in mapping
        ).add_to(marker_cluster)

# Create heatmap data
heat_data = [[row['Latitude'], row['Longitude'], row['Killed'] + row['Injured']] for idx, row in df.iterrows()]

# Add heatmap to the map
HeatMap(heat_data).add_to(m)

# Save the map to an HTML file
m.save('../output/combined_incident_map2.html')

print("Combined map created and saved to 'combined_incident_map.html'.")