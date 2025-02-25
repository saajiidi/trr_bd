# scripts/load_data.R

# Load required libraries
library(dplyr)

# Function to load and preprocess data
load_and_preprocess_data <- function(sheet_url) {
  # Read the data
  df <- read.csv(sheet_url)
  
  # Check if required columns exist
  required_columns <- c("Longitude", "Latitude", "Group", "Date", "Location", 
                        "Target.Event", "Killed", "Injured", "Claimed.", "Notes")
  missing_columns <- setdiff(required_columns, colnames(df))
  
  if (length(missing_columns) > 0) {
    stop("Error: The dataset is missing the following columns: ", paste(missing_columns, collapse = ", "))
  }
  
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
  
  # Return the data and statistics
  return(list(df = df, group_stats = group_stats, group_pct = group_pct))
}