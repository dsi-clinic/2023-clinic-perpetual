#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 14:36:59 2023

@author: genie_god
"""

import configparser
import time
import sys
import csv
import pandas as pd
import requests
import tqdm


def get_route_data(coordinates, access_token):
    """
    Fetch travel time list using Mapbox Direction API.
    :param coordinates: List of coordinates [longitude, latitude]
    :param access_token: Your Mapbox Access Token
    :return: JSON response from Mapbox API
    """
    # Convert list of coordinates to string format
    coordinates_str = ";".join([f"{lon},{lat}" for lon, lat in coordinates])

    # Endpoint URL (assuming driving mode here,
    # but can be changed to walking, cycling, etc.)
    url_root = "https://api.mapbox.com/directions/v5/mapbox/driving"
    url = f"{url_root}/{coordinates_str}?"

    # Parameters
    params = {
        "access_token": access_token,
        # "annotation": "duration",
        "steps": "true",
        "waypoints_per_route": "true",
    }

    # Make the API call
    response = requests.get(url, params=params)
    # Return the JSON response
    return response.json()


def add_coordinator(df):
    df["Coordinates"] = df[["Longitude", "Latitude"]].values.tolist()
    df.drop(columns=["Longitude", "Latitude"], inplace=True)
    return df

def read_csv_files_to_dataframes():
    df_list = []
    for i in range(1, len(sys.argv)):
        file_name = sys.argv[i]
        df = pd.read_csv(file_name)
        df = add_coordinator(df)
        df_list.append(df)
    return df_list



def initialize_data():
    """
    Initialize the data from the CSV file
    and the Mapbox token from the config file.

    :return: Dataframe and Mapbox token
    """

    # Initialize the parser
    config = configparser.ConfigParser()
    # Read the config file
    config.read("config.ini")
    mapbox_token = config["mapbox"]["token"]
    
    
    # Take file name from terminal
    df_list = read_csv_files_to_dataframes()

    return df_list, mapbox_token


def request_waypoints(df, mapbox_token):
    waypoints_location = []
    waypoints_instruction = []
    location_index = []
    way_points_index = []
    col_idx = df.columns.get_loc("Coordinates")

    for i in tqdm.tqdm(range(0, len(df), 24)):
        # Goes through 24 destinations for every source due to api limit
        coordinate_list = df.iloc[i : i + 24, col_idx].tolist()
        result = get_route_data(coordinate_list, mapbox_token)
        # pull out duration list from result
        legs = result["routes"][0]["legs"]
        for j in range(len(legs)):
            steps = legs[j]["steps"]
            for k in range(len(steps)):
                waypoints_location.append(
                    legs[j]["steps"][k]["maneuver"]["location"]
                )
                waypoints_instruction.append(
                    legs[j]["steps"][k]["maneuver"]["instruction"]
                )
                location_index.append(i + j)
                way_points_index.append(k)

        time.sleep(1)

    df_waypoints = pd.DataFrame(
        {
            "location": location_index,
            "way_points": way_points_index,
            "waypoints_location": waypoints_location,
            "waypoints_instruction": waypoints_instruction,
        }
    )
    return df_waypoints


def main():
    # Initialize the data
    df_list, mapbox_token = initialize_data()

    # Get the matrix data.
    # Goes through every source once
    for i, df in enumerate(df_list):
        df_waypoints = request_waypoints(df, mapbox_token)
        # Save the DataFrame to a CSV file
        csv_filename = f'waypoints_df_{i}.csv'
        output_path = f"../data/{csv_filename}"
        df_waypoints.to_csv(output_path, index=False)
        print(f"Saved waypoints for dataframe {i} to {csv_filename}")

    print("\nComplete!")


if __name__ == "__main__":
    main()
