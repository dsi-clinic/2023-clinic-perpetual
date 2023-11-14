#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 15:55:43 2023

@author: genie_god
"""

import pandas as pd
import folium
import sys
# pull from google
center_galveston = [29.3013, -94.7977]


def convert_string_to_coords(coord_str):
    """
    Converts a coordinate string of the form '[-94.852238, 29.273577]'
    into a list of float values.

    Args:
    coord_str (str): A string representing coordinates.

    Returns:
    list: A list containing two float values [longitude, latitude].
    """
    # Remove brackets and split by comma
    point_list = coord_str.strip('[]').split(',')
    # Convert each part to float and return
    return [float(x) for x in reversed(point_list)]


df = pd.read_csv(sys.argv[1])

mapping_point = df['waypoints_location']

mapping_point_list = mapping_point.values.tolist()

mapping_point_list = [convert_string_to_coords(i) for i in mapping_point_list]



map = folium.Map(center_galveston, zoom_start=12)

# Create a string from mapping_point_list (if needed)
waypoint_string = ', '.join([str(point) for point in mapping_point_list])

# Connect waypoints using a PolyLine
folium.PolyLine(mapping_point_list, color='blue',
                weight=2.5, opacity=1).add_to(map)

df_plot = df.dropna()
mapping_point_location = df_plot['waypoints_location']

mapping_point_location_list = mapping_point_location.values.tolist()

mapping_point_location_list = [convert_string_to_coords(
    i) for i in mapping_point_location_list]

for item, name, address in zip(mapping_point_location_list, df_plot['name'],
                               df_plot['address']):
    if name != 'nan':
        folium.Marker(item, popup=[name, address]).add_to(map)

# Save the map to an HTML file
map.save("../output/map_with_waypoints.html")
