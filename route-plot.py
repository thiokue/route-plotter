import folium
import pandas as pd
from tsp_solver.greedy import solve_tsp
import numpy as np
from math import radians, sin, cos, sqrt, atan2

# Haversine formula to calculate distance between two coordinates
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth's radius in kilometers

    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def calculate_tsp(df):
    # Extract latitude and longitude coordinates from the dataframe
    coordinates = df[['latitude', 'longitude']].values

    # Calculate the distance matrix using the haversine formula
    num_points = len(coordinates)
    distances = np.zeros((num_points, num_points))

    for i in range(num_points):
        for j in range(i+1, num_points):
            lat1, lon1 = coordinates[i]
            lat2, lon2 = coordinates[j]
            distances[i, j] = haversine(lat1, lon1, lat2, lon2)
            distances[j, i] = distances[i, j]

    # Solve the TSP to get the optimal route
    route = solve_tsp(distances)

    # Reorder the dataframe according to the route
    df = df.iloc[route]
    return df


def plot_map(df):
    # Create a map centered at the first point
    map_center = [df['latitude'].iloc[0], df['longitude'].iloc[0]]
    map_route = folium.Map(location=map_center, zoom_start=10)

    # Add markers for each point
    for index, row in df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=row['adress']
        ).add_to(map_route)

    # Add a polyline to connect the markers in the route
    route_points = df[['latitude', 'longitude']].values
    folium.PolyLine(route_points, color='blue', weight=2.5, opacity=1).add_to(map_route)

    # Save the map as an HTML file
    map_route.save("route_map.html")
    return True


