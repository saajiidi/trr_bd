# Install required packages only if not already installed
packages <- c("dplyr", "leaflet", "tidygeocoder", "htmltools", "tidyverse",
              "ggmap", "httr", "jsonlite", "remotes")

new_packages <- packages[!(packages %in% installed.packages()[,"Package"])]
if (length(new_packages)) install.packages(new_packages)

# Install leaflet.extras from GitHub if not available
if (!requireNamespace("leaflet.extras", quietly = TRUE)) {
  remotes::install_github("bhaskarvk/leaflet.extras")
}

# Load required libraries
library(dplyr)
library(leaflet)
library(leaflet.extras)
library(tidygeocoder)
library(htmltools)
library(htmlwidgets)

# Replace with your published Google Sheet link
sheet_url <- "https://docs.google.com/spreadsheets/d/e/2PACX-1vROsLYRpCh6rUAQFbNcXtTHKpeFFPyWzlQmniXa1DL7BVKeeHkl8-Ml-924kHzpRiUV__q0lD8C10FZ/pub?output=csv"

# Read the data
df <- read.csv(sheet_url)
# Load the geocoded dataset df <- read.csv("Terror Attack in BD - Main.csv")

# Check if required columns exist
required_columns <- c("Longitude", "Latitude", "Group", "Date", "Location", 
                      "Target.Event", "Killed", "Injured", "Claimed.", "Notes")
missing_columns <- setdiff(required_columns, colnames(df))

if (length(missing_columns) > 0) {
  stop("Error: The dataset is missing the following columns: ", paste(missing_columns, collapse = ", "))
}

# Define a color palette for groups
group_colors <- colorFactor(palette = c("red", "blue", "green", "orange"), domain = df$Group)

# Create leaflet map
m <- leaflet(df) %>%
  addProviderTiles(providers$CartoDB.Positron) %>%  # Use a cleaner tile layer
  setView(lng = 90.3563, lat = 23.6850, zoom = 7) %>%  # Center on Bangladesh
  
  # Add Marker Cluster
  
  addMarkers(
    
    lng = ~Longitude,
    
    lat = ~Latitude,
    
    clusterOptions = markerClusterOptions(),  # Enable marker clustering
    popup = ~paste0(
      "<b>Group:</b> ", Group, "<br>",
      "<b>Date:</b> ", Date, "<br>",
      "<b>Location:</b> ", Location, "<br>",
      "<b>Target/Event:</b> ", Target.Event, "<br>",
      "<b>Killed:</b> ", Killed, "<br>",
      "<b>Injured:</b> ", Injured, "<br>",
      "<b>Claimed?:</b> ", Claimed., "<br>",
      "<b>Notes:</b> ", Notes
    ),
    label = ~paste("Killed:", Killed, "| Injured:", Injured)
  ) %>%
  
  # Add Heatmap Layer
  addHeatmap(
    lng = ~Longitude,
    lat = ~Latitude,
    intensity = ~Killed + Injured,  # Use casualties for intensity
    blur = 15,  # Reduce blur for a sharper heatmap
    max = max(df$Killed + df$Injured, na.rm = TRUE) * 0.1,  # Dynamic scaling
    radius = 12,  # Adjust radius for better visualization
    gradient = c("blue", "yellow", "red")  # Improve heatmap color scheme
  ) %>%
  
  # Add Legend
  addLegend(
    position = "bottomright",
    pal = group_colors,
    values = ~Group,
    title = "Group"
  )

# Save the map as an HTML file
htmlwidgets::saveWidget(m, file = "cluster_map.html", selfcontained = TRUE)

# Display the map
m
