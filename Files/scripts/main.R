# scripts/main.R

# Load required libraries
source("scripts/load_data.R")
source("scripts/create_charts.R")
source("scripts/create_map.R")

# Define file paths
sheet_url <- "https://docs.google.com/spreadsheets/d/e/2PACX-1vROsLYRpCh6rUAQFbNcXtTHKpeFFPyWzlQmniXa1DL7BVKeeHkl8-Ml-924kHzpRiUV__q0lD8C10FZ/pub?output=csv"
bar_chart_file <- "output/bar_chart.png"
pie_chart_file <- "output/pie_chart.png"
output_map_file <- "output/map_with_legend.html"

# Step 1: Load and preprocess data
data <- load_and_preprocess_data(sheet_url)
df <- data$df
group_stats <- data$group_stats
group_pct <- data$group_pct

# Step 2: Create charts
create_bar_chart(group_stats, bar_chart_file)
create_pie_chart(group_pct, pie_chart_file)

# Step 3: Create the map
map <- create_map(df, bar_chart_file, pie_chart_file, output_map_file)

# Display the map
map