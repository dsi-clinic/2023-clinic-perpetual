#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 15:55:43 2023

@author: genie_god
"""

import pandas as pd
import folium


df_FUE = pd.read_csv('data/FUE_Galveston.csv')

FUE_mapping_point = df_FUE[['Latitude', 'Longitude']]

FUE_mapping_point_list = FUE_mapping_point.values.tolist()

#pull from google
center_galveston= [29.3013, -94.7977]

map = folium.Map(location=center_galveston, zoom_start=12)
for item, name in zip(FUE_mapping_point_list, df_FUE['Name']):
    folium.Marker(item, popup=name).add_to(map)

map.save("map.html")
