# scripts/create_map.R

# Load required libraries
library(leaflet)
library(htmlwidgets)
library(htmltools)

# Function to create the map
create_map <- function(df, bar_chart_file, pie_chart_file, output_file) {
  # Create HTML content for the legend
  legend_html <- paste0(
    '<div style="position: fixed; top: 10px; left: 10px; z-index: 1000; background: white; padding: 10px; border: 2px solid grey; border-radius: 5px; box-shadow: 2px 2px 10px rgba(0,0,0,0.5);">',
    '<h3 style="margin: 0;">Group-Wise Statistics</h3>',
    '<h4 style="margin: 5px 0;">Killed by Group (Claimed vs Not Claimed)</h4>',
    '<img src="', bar_chart_file, '" width="300" height="200">',
    '<h4 style="margin: 5px 0;">Group-Wise Killing Percentage</h4>',
    '<img src="', pie_chart_file, '" width="300" height="200">',
    '</div>'
  )
  
  # Create leaflet map with legend
  m <- leaflet(df) %>%
    addProviderTiles(providers$CartoDB.Positron) %>%
    setView(lng = 90.3563, lat = 23.6850, zoom = 7) %>%
    addMarkers(
      lng = ~Longitude,
      lat = ~Latitude,
      clusterOptions = markerClusterOptions(),
      popup = ~paste0(
        "<b>Group:</b> ", Group, "<br>",
        "<b>Date:</b> ", Date, "<br>",
        "<b>Location:</b> ", Location, "<br>",
        "<b>Target/Event:</b> ", Target.Event, "<br>",
        "<b>Killed:</b> ", Killed, "<br>",
        "<b>Injured:</b> ", Injured, "<br>",
        "<b>Claimed?:</b> ", Claimed., "<br>",
        "<b>Notes:</b> ", Notes
      )
    ) %>%
    addControl(
      html = htmltools::HTML(legend_html),
      position = "topleft"
    )
  
  # Save the map as an HTML file
  saveWidget(m, file = output_file, selfcontained = TRUE)
  
  return(m)
}