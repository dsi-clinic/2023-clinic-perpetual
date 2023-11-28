import configparser
import folium
import pandas as pd


def add_markers(f_map, points, color="blue"):
    """
    Given a folium map, route data (includes location names), and a color (str),
    draw markers on the given map

    Parameters:
        f_map : folium map
        route_data : pd.DataFrame
        color : str (e.g., "red", "blue")
    """

    for i in range(len(points)):
        row = points.iloc[i]
        loc_name = row["Name"]
        y, x = row[["Latitude", "Longitude"]]
        address = row["Address"]
        index = points.index[i]
        dropoff, pickup = row[["Weekly_Dropoff_Totes", "Daily_Pickup_Totes"]]
        pickup_type = row["pickup_type"]
        popup_html = f"""
                Index: {index}
                <br>
                Name: {loc_name}
                <br>
                Address: {address}
                <br>
                Dropoff (weekly): {dropoff}
                <br>
                Pickup (daily): {pickup}
                <br>
                Pickup Type: {pickup_type}
                """
        popup = folium.Popup(popup_html, max_width=700)

        folium.Marker(
            (y, x), popup=popup, parse_html=True, icon=folium.Icon(color=color)
        ).add_to(f_map)
    return None
    


if __name__ == "__main__":

    '''
    Table of Contents:
    1. Read config
    2. Parse Config
    3. Read single-truth dataframe and distance matrix
    4. Make a copy of distance matrix filtered to bike-to-truck distances only
    5. Find truck points within config's radius of bike points
    5.1. Mark aggregate points
    6. Convert 5.1's points to bike-servicable points
    7. Prepare dataframes for output
    8. Prepare distance matrices for output
    9. Export everything
    '''

    # 0. experimental variables
    aggs = [11,12,19,49,72,104,147,208]

    # 1. read config
    config = configparser.ConfigParser()
    config.read("../utils/config_inputs.ini")
    cfg = config["convert.to_bikes"]

    # 2. parse config
    truth_df_path = cfg["truth_df_path"]
    truth_dist_df_path = cfg["truth_dist_df_path"]
    location = [float(cfg["Latitude"]), float(cfg["Longitude"])]
    distance_thresh = float(cfg["distance_thresh"])  # in meters
    map_save_path = cfg["map_save_path"]
    truck_df_savepath = cfg["truck_df_savepath"]
    bike_df_savepath = cfg["bike_df_savepath"]
    truck_dist_df_savepath = cfg["truck_dist_df_savepath"]
    bike_dist_df_savepath = cfg["bike_dist_df_savepath"]

    # 3. read single-truth dataframe and single-truth distance matrix
    truth_df = pd.read_csv(truth_df_path)
    truth_dist = pd.read_csv(truth_dist_df_path)

    # 4. filter distance mtrx to distances from bike to truck-served locations
    bike_df = truth_df[truth_df["pickup_type"] == "Bike"]
    bike_indices = bike_df.index.to_list()
    bike_dists = truth_dist.iloc[bike_indices]
    drop_cols = [str(i) for i in bike_indices]
    bike_to_truck_dists = bike_dists.drop(columns=drop_cols)

    # 5. mark truck-served points within {distance_thresh} of bike-served points
    converts = []
    for col in bike_to_truck_dists.columns:
        if min(bike_to_truck_dists[col]) <= distance_thresh and int(col):
            converts.append(int(col))

    # 6. convert marked truck-serviced locations to bike-servicable locations
    converted_truth_df = truth_df.copy()
    converts_df = truth_df.iloc[list(set(converts) - set(aggs))] # for graphing
    bike_agg_df = truth_df.iloc[aggs] # for graphing
    for i in converts:
        if i in aggs:
            converted_truth_df.at[i, "pickup_type"] = "Bike_Aggregate"
        else:
            converts_df.at[i, "pickup_type"] = "Bike"
            converted_truth_df.at[i, "pickup_type"] = "Bike"

    # 7. prepare info dataframes for output
    truck_converted_df = converted_truth_df[
        (converted_truth_df["pickup_type"] == "Truck") &
        (converted_truth_df["pickup_type"] == "Bike_Aggregate")
    ]
    bike_converted_df = converted_truth_df[
        (converted_truth_df["pickup_type"] == "Bike") & 
        (converted_truth_df["pickup_type"] == "Bike_Aggregate")
    ]
    
    # 8. prepare distance matrices for output
    total_inds = {i for i in range(len(truth_df))}
    bike_ind = set(bike_indices + converts)
    truck_ind = sorted(list(total_inds - bike_ind + aggs))
    bike_ind = sorted(list(bike_ind))
    truck_dist_df = truth_dist[[str(i) for i in truck_ind]].iloc[truck_ind]
    bike_dist_df = truth_dist[[str(i) for i in bike_ind]].iloc[bike_ind]

    # 9. export dataframes
    truck_converted_df.to_csv(truck_df_savepath)
    bike_converted_df.to_csv(bike_df_savepath)
    truck_dist_df.to_csv(truck_dist_df_savepath)
    bike_dist_df.to_csv(bike_dist_df_savepath)

    map = folium.Map(location=location, tiles="OpenStreetMap", zoom_start=11)
    add_markers(map, truck_converted_df, "blue")
    add_markers(map, bike_df, "red")
    add_markers(map, converts_df, "green")
    add_markers(map, bike_agg_df, "orange") #  bike_aggs = [11,12,19,49,72,104,147,208]

    map.save(map_save_path)
