import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Load the dataset
df = pd.read_csv('../data/trr_bd.csv')

# Initialize Nominatim API
geolocator = Nominatim(user_agent="visualization_map_project")

# Add rate limiter to avoid overloading the service
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Function to get latitude and longitude from district name
def get_lat_long(district_name):
    try:
        location = geocode(district_name + ", Bangladesh")  # Add country for better accuracy
        return (location.latitude, location.longitude)
    except:
        return (None, None)

# Apply the function to your dataset
df['Coordinates'] = df['Location'].apply(get_lat_long)

# Split coordinates into separate columns
df['Latitude'] = df['Coordinates'].apply(lambda x: x[0])
df['Longitude'] = df['Coordinates'].apply(lambda x: x[1])

# Drop the 'Coordinates' column
df.drop(columns=['Coordinates'], inplace=True)

# Save the updated dataset
df.to_csv('geocoded_dataset.csv', index=False)

print("Geocoding completed. Updated dataset saved to 'geocoded_dataset.csv'.")