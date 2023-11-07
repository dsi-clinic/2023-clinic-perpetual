import configparser
import sys
import time

import pandas as pd
import requests
import tqdm


def get_list_data(coordinates, access_token):
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


def request_time(df, mapbox_token):
    col_duration = [300]
    total_time = 300
    col_idx = df.columns.get_loc("Coordinates")

    for i in tqdm.tqdm(range(0, len(df) - 1, 24)):
        # Goes through 24 destinations for every source due to api limit
        coordinate_list = df.iloc[i : i + 25, col_idx].tolist()
        result = get_list_data(coordinate_list, mapbox_token)
        # pull out duration list from result
        leg_list = result["routes"][0]["legs"]
        time_list = [i["duration"] for i in leg_list]
        # accumulate time along the route
        for j in range(len(time_list) - 1):
            total_time += time_list[j] + 5 * 60
            col_duration.append(int(total_time))
        time.sleep(1)

    return col_duration


def main():
    # Initialize the data
    df_list, mapbox_token = initialize_data()

    # Get the matrix data.
    # Goes through every source once
    for i, df in enumerate(df_list):
        df['duration'] = request_time(df, mapbox_token)
        # Save the DataFrame to a CSV file
        csv_filename = f'duration_df_{i}.csv'
        output_path = f"../data/{csv_filename}"
        df.to_csv(output_path, index=False)
        print(f"Saved duration for dataframe {i} to {csv_filename}")

    print("\nComplete!")
    


if __name__ == "__main__":
    main()
