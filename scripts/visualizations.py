from folium.plugins import HeatMap

# Create heatmap data
heat_data = [[row['Latitude'], row['Longitude'], row['Killed'] + row['Injured']] for idx, row in df.iterrows()]

# Add heatmap to the map
HeatMap(heat_data).add_to(m)

# Save the map
m.save('incident_heatmap.html')