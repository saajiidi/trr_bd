# scripts/create_charts.R

# Load required libraries
library(ggplot2)

# Function to create bar chart
create_bar_chart <- function(group_stats, output_file) {
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
  
  # Save the bar chart as an image
  ggsave(output_file, bar_chart, width = 6, height = 4)
}

# Function to create pie chart
create_pie_chart <- function(group_pct, output_file) {
  pie_chart <- ggplot(group_pct, aes(x = "", y = Percentage, fill = Group)) +
    geom_bar(stat = "identity", width = 1) +
    coord_polar("y", start = 0) +
    labs(
      title = "Group-Wise Killing Percentage",
      fill = "Group"
    ) +
    theme_void() +
    theme(legend.position = "right")
  
  # Save the pie chart as an image
  ggsave(output_file, pie_chart, width = 6, height = 4)
}