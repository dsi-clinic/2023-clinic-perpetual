import configparser
import datetime
import pickle
import sys
import time

import numpy as np
import pandas as pd
import requests
import tqdm


def get_matrix_data(coordinates, access_token):
    """
    Fetch travel time matrix using Mapbox Matrix API.
    Sets the first coordinate as the source and the rest as destinations.

    :param coordinates: List of coordinates [longitude, latitude]
    :param access_token: Your Mapbox Access Token
    :return: JSON response from Mapbox API
    """
    # Convert list of coordinates to string format
    coordinates_str = ";".join([f"{lon},{lat}" for lon, lat in coordinates])

    # Endpoint URL (assuming driving mode here,
    # but can be changed to walking, cycling, etc.)
    url_root = "https://api.mapbox.com/directions-matrix/v1/mapbox/driving"
    url = f"{url_root}/{coordinates_str}"

    # Parameters
    params = {
        "access_token": access_token,
        "annotations": "duration",
    }

    # Make the API call
    response = requests.get(url, params=params)
    # Return the JSON response
    return response.json()


def add_coordinator(df):
    df["Coordinates"] = df[["Longitude", "Latitude"]].values.tolist()
    df.drop(columns=["Longitude", "Latitude"], inplace=True)
    return df


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
    file_name = sys.argv[1]
    df1 = pd.read_csv(file_name)
    file_name = sys.argv[2]
    df2 = pd.read_csv(file_name)
    # Convert coordinates to list of lists
    df1 = add_coordinator(df1)
    df2 = add_coordinator(df2)

    return df1, df2, mapbox_token


def request_time(df, mapbox_token):
    col_duration = [300]
    total_time = 300
    col_idx = df.columns.get_loc("Coordinates")
    for i in tqdm.tqdm(range(0, len(df) - 1, 24)):
        # Goes through 24 destinations for every source due to api limit
        coordinate_list = df.iloc[i : i + 25, col_idx].tolist()
        result = get_matrix_data(coordinate_list, mapbox_token)
        for j in range(len(result["durations"]) - 1):
            time_ = result["durations"][j][j + 1]
            total_time += time_ + 5 * 60
            col_duration.append(int(total_time))
        time.sleep(1)

    return col_duration


def main():
    # Initialize the data
    df1, df2, mapbox_token = initialize_data()

    # Get the matrix data.
    # Goes through every source once
    df1["duration"] = request_time(df1, mapbox_token)
    df2["duration"] = request_time(df2, mapbox_token)

    # Save the DataFrame to a CSV file
    output_file = "../data/route1_time.csv"
    df1.to_csv(output_file, index=False)

    output_file = "../data/route2_time.csv"
    df2.to_csv(output_file, index=False)

    print("\nComplete!")


if __name__ == "__main__":
    main()
