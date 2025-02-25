# Load required libraries
library(dplyr)
library(leaflet)
library(ggplot2)
library(htmlwidgets)
library(base64enc)

# Replace with your published Google Sheet link
sheet_url <- "https://docs.google.com/spreadsheets/d/e/2PACX-1vROsLYRpCh6rUAQFbNcXtTHKpeFFPyWzlQmniXa1DL7BVKeeHkl8-Ml-924kHzpRiUV__q0lD8C10FZ/pub?output=csv"

# Read the data
df <- read.csv(sheet_url)

# Calculate group-wise statistics
group_stats <- df %>%
  group_by(Group, Claimed.) %>%
  summarise(Total_Killed = sum(Killed, na.rm = TRUE), .groups = 'drop') %>%
  mutate(Claimed. = ifelse(Claimed. == "Yes", "Claimed", "Not Claimed"))

# Calculate percentage of killings by each group
group_pct <- df %>%
  group_by(Group) %>%
  summarise(Total_Killed = sum(Killed, na.rm = TRUE), .groups = 'drop') %>%
  mutate(Percentage = Total_Killed / sum(Total_Killed) * 100)

# Bar chart for killed by group (claimed/not claimed)
bar_chart <- ggplot(group_stats, aes(x = Group, y = Total_Killed, fill = Claimed.)) +
  geom_bar(stat = "identity", position = "stack") +
  labs(
    title = "Killed by Group (Claimed vs Not Claimed)",
    x = "Group",
    y = "Total Killed",
    fill = "Claimed?"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Pie chart for group-wise killing percentage
pie_chart <- ggplot(group_pct, aes(x = "", y = Percentage, fill = Group)) +
  geom_bar(stat = "identity", width = 1) +
  coord_polar("y", start = 0) +
  labs(
    title = "Group-Wise Killing Percentage",
    fill = "Group"
  ) +
  theme_void() +
  theme(legend.position = "right"))

# Save the charts as images
ggsave("bar_chart.png", bar_chart, width = 6, height = 4)
ggsave("pie_chart.png", pie_chart, width = 6, height = 4)

# Convert charts to base64 images
bar_chart_base64 <- base64enc::base64encode("bar_chart.png")
pie_chart_base64 <- base64enc::base64encode("pie_chart.png")

# Create HTML content for popup
popup_content <- paste0(
  "<h3>Group-Wise Statistics</h3>",
  "<h4>Killed by Group (Claimed vs Not Claimed)</h4>",
  "<img src='data:image/png;base64,", bar_chart_base64, "' width='400' height='300'>",
  "<h4>Group-Wise Killing Percentage</h4>",
  "<img src='data:image/png;base64,", pie_chart_base64, "' width='400' height='300'>"
)

# Create leaflet map with popup
m <- leaflet(df) %>%
  addProviderTiles(providers$CartoDB.Positron) %>%
  setView(lng = 90.3563, lat = 23.6850, zoom = 7) %>%
  addMarkers(
    lng = ~Longitude,
    lat = ~Latitude,
    clusterOptions = markerClusterOptions(),
    popup = popup_content
  )

# Save the map as an HTML file
htmlwidgets::saveWidget(m, file = "map_with_charts.html", selfcontained = TRUE)

# Display the map
m