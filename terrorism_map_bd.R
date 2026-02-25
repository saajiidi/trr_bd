# Install required packages only if not already installed
packages <- c("dplyr", "leaflet", "leaflet.extras", "tidygeocoder", "htmltools", 
              "tidyverse", "htmlwidgets", "crosstalk", "remotes")

new_packages <- packages[!(packages %in% installed.packages()[,"Package"])]
if (length(new_packages)) install.packages(new_packages)

# Load required libraries
library(dplyr)
library(leaflet)
library(leaflet.extras)
library(tidygeocoder)
library(htmltools)
library(htmlwidgets)
library(crosstalk)

# 1. Data Loading & Robustness
sheet_url <- "https://docs.google.com/spreadsheets/d/e/2PACX-1vROsLYRpCh6rUAQFbNcXtTHKpeFFPyWzlQmniXa1DL7BVKeeHkl8-Ml-924kHzpRiUV__q0lD8C10FZ/pub?output=csv"

# Safe read function
df <- tryCatch({
  read.csv(sheet_url, stringsAsFactors = FALSE)
}, error = function(e) {
  stop("Failed to connect to the dataset. Please check your internet connection or the Sheet link.")
})

# Basic Sanitization
df <- df %>%
  mutate(
    Killed = as.numeric(gsub("[^0-9]", "", Killed)) %>% replace_na(0),
    Injured = as.numeric(gsub("[^0-9]", "", Injured)) %>% replace_na(0),
    Casualties = Killed + Injured,
    Longitude = as.numeric(Longitude),
    Latitude = as.numeric(Latitude),
    Group = ifelse(is.na(Group) | Group == "", "Unknown", Group)
  ) %>%
  filter(!is.na(Longitude) & !is.na(Latitude)) # Remove invalid coordinates

# 2. Crosstalk for Interactive Filtering
sd <- SharedData$new(df)

# 3. Premium UI Components
# Define a color palette for groups
group_colors <- colorFactor(
  palette = "YlOrRd", 
  domain = df$Group
)

# Custom Popup Logic (Premium Styling)
popup_content <- paste0(
  "<div style='font-family: Arial, sans-serif; min-width: 200px;'>",
  "<h4 style='color: #d9534f; margin-bottom: 5px; border-bottom: 1px solid #eee;'>", df$Group, "</h4>",
  "<b>📍 Location:</b> ", df$Location, "<br>",
  "<b>📅 Date:</b> ", df$Date, "<br>",
  "<div style='margin-top: 10px; background: #f9f9f9; padding: 5px; border-radius: 4px;'>",
  "<b>Casualties:</b> ",
  "<span style='color:red;'>💀 ", df$Killed, " Killed</span> | ",
  "<span style='color:orange;'>🩹 ", df$Injured, " Injured</span>",
  "</div>",
  "<p style='font-size: 0.9em; color: #666; font-style: italic; margin-top: 8px;'>", df$Notes, "</p>",
  "</div>"
)

# 4. Create Interactive Leaflet Map
m <- leaflet(sd) %>%
  # --- Base Layers ---
  addProviderTiles(providers$CartoDB.Positron, group = "Light (Standard)") %>%
  addProviderTiles(providers$CartoDB.DarkMatter, group = "Dark Mode") %>%
  addProviderTiles(providers$Esri.WorldImagery, group = "Satellite") %>%
  
  # Set view on Bangladesh
  setView(lng = 90.3563, lat = 23.6850, zoom = 7) %>%
  
  # --- Add Features ---
  # 1. Marker Cluster Layer
  addMarkers(
    lng = ~Longitude, 
    lat = ~Latitude,
    clusterOptions = markerClusterOptions(),
    popup = popup_content,
    label = ~paste0(Group, " (", Casualties, " casualties)"),
    group = "Markers (Clustered)"
  ) %>%
  
  # 2. Heatmap Layer
  addHeatmap(
    lng = ~Longitude, 
    lat = ~Latitude,
    intensity = ~Casualties,
    blur = 20, 
    max = max(df$Casualties, na.rm = TRUE), 
    radius = 15,
    group = "Heatmap"
  ) %>%
  
  # --- Controls ---
  # Search Bar
  addSearchOSM() %>%
  
  # Fullscreen toggle
  addFullscreenControl() %>%
  
  # Mini-map for context
  addMiniMap(tiles = providers$CartoDB.Positron, toggleDisplay = TRUE) %>%
  
  # Layer Control
  addLayersControl(
    baseGroups = c("Light (Standard)", "Dark Mode", "Satellite"),
    overlayGroups = c("Markers (Clustered)", "Heatmap"),
    options = layersControlOptions(collapsed = FALSE)
  ) %>%
  
  # Legend
  addLegend(
    position = "bottomleft",
    pal = group_colors,
    values = df$Group,
    title = "Incident Responsible",
    opacity = 0.7
  )

# 5. Assemble Interactive Dashboard
# Combine filters and map into a single page
dashboard <- bscols(
  widths = c(3, 9),
  list(
    filter_checkbox("group", "Select Incident Group", sd, ~Group, inline = FALSE),
    filter_slider("casualties", "Filter by Casualties", sd, ~Casualties, step = 1),
    filter_select("location", "Search Location", sd, ~Location),
    hr(),
    div(style = "font-size: 0.8em; color: gray;",
        "Data source: National Security Incident Tracker",
        br(),
        a(href = "https://docs.google.com/spreadsheets/d/e/2PACX-1vROsLYRpCh6rUAQFbNcXtTHKpeFFPyWzlQmniXa1DL7BVKeeHkl8-Ml-924kHzpRiUV__q0lD8C10FZ/pubhtml", 
          "View Full Dataset", target = "_blank")
    )
  ),
  m
)

# 6. Save & Display
# Wrap in a theme-friendly div
final_page <- tagList(
  tags$head(
    tags$style(HTML("
      .selectized { font-family: 'Arial', sans-serif !important; }
      .well { background-color: #ffffff; border: 1px solid #e3e3e3; border-radius: 8px; }
      h4 { font-weight: bold; color: #333; }
    "))
  ),
  div(style = "padding: 20px;",
      h2("SafeBD Intelligence Dashboard", style = "margin-top: 0; color: #2c3e50; font-weight: 800;"),
      p("Interactive analysis of public security incidents in Bangladesh."),
      hr(),
      dashboard
  )
)

# Save to file
saveWidget(final_page, file = "index.html", selfcontained = TRUE)

# View in RStudio Viewer
final_page