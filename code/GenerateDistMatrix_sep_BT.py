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
        "annotations": "distance",
        "sources": "0",
        # Destinations are all coordinates after the first one
        "destinations": ";".join([str(i) for i in range(1, len(coordinates))]),
    }

    # Make the API call
    response = requests.get(url, params=params)
    # Return the JSON response
    return response.json()

def build_matrix(df, mapbox_token):
    # Initialize the matrix
    full_matrix = np.zeros(len(df))

    # Get the matrix data.
    # Goes through every source once
    # and then every destination for every source.
    col_idx = df.columns.get_loc("Coordinates")
    for i in tqdm.tqdm(range(len(df))):
        horizontal = [[]]
        # Goes through 24 destinations for every source due to api limit
        for j in range(0, len(df), 23):
            coordinate_list = [df.iloc[i, col_idx]] + df.iloc[
                j : j + 23, col_idx
            ].tolist()
            # API does not allow calls with only 1 destination
            # so we attach a dummy destination at the end
            # to make sure the call go through and remove it later
            coordinate_list.append(df.iloc[i, col_idx])
            result = [
                get_matrix_data(coordinate_list, mapbox_token)["distances"][0][
                    :-1
                ]
            ]

            horizontal = np.hstack((horizontal, result))
            time.sleep(1)
        full_matrix = np.vstack((full_matrix, horizontal))
    # remove the first row which is all zeros
    full_matrix = full_matrix[1:, :]
    return full_matrix


def generate_capacity_list(df_truck, df_bike, timestamp_str):
    """
    Generate a list of capacities from the dataframe.

    :param df: Dataframe
    :param timestamp_str: Timestamp string
    """
    # save list as pkl file
    capacity_file = f"data/capacity_list_{timestamp_str}_truck.pkl"
    with open(capacity_file, "wb") as f:
        pickle.dump(list(map(int, df_truck["Daily_Pickup_Totes"].tolist())), f)
    capacity_file = f"data/capacity_list_{timestamp_str}_bike.pkl"
    with open(capacity_file, "wb") as f:
        pickle.dump(list(map(int, df_bike["Daily_Pickup_Totes"].tolist())), f)


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
    df_truck = pd.read_csv(file_name)
    file_name = sys.argv[2]
    df_bike = pd.read_csv(file_name)
    # Convert coordinates to list of lists
    df_truck = add_cooridnates(df_truck)
    df_bike = add_cooridnates(df_bike)

    return df_truck, df_bike, mapbox_token

def add_cooridnates(df):
    df["Coordinates"] = df[["Longitude", "Latitude"]].values.tolist()
    df.drop(columns=["Longitude", "Latitude"], inplace=True)
    return df

def main():
    # Initialize the data
    df_truck, df_bike, mapbox_token = initialize_data()

    # Build the matrix for truck and bike
    full_matrix_truck = build_matrix(df_truck, mapbox_token)
    full_matrix_bike = build_matrix(df_bike, mapbox_token)

    # Get the timestamp
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Save the matrix to a file
    filename_root = "../data/generated_distance_matrices/distance_matrix"
    filename = f"{filename_root}_{timestamp_str}_truck.npy"
    np.save(filename, full_matrix_truck)
    filename = f"{filename_root}_{timestamp_str}_bike.npy"
    np.save(filename, full_matrix_bike)

    # Save the capacity list to a file
    generate_capacity_list(df_truck, df_bike, timestamp_str)

    print("Complete!")


if __name__ == "__main__":
    main()
