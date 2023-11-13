import pandas as pd
import folium
import configparser


def add_markers(f_map, points, color='blue'):
    """
    Given a folium map, route data (includes location names), and a color (str),
    draw markers on the given map

    Parameters:
        f_map : folium map
        route_data : pd.DataFrame
        color : str (e.g., "red", "blue")
    """
    
    icon_size= 100
    for i in range(len(points)):
        y, x = points[["Latitude", "Longitude"]].iloc[i]
        folium.Marker((y,x), popup=points.iloc[i]['Name'], icon=folium.Icon(color=color)).add_to(f_map)
        icon_size = 40
    return None


if __name__ == '__main__':

    # read config
    config = configparser.ConfigParser()
    config.read('../utils/config.ini')
    cfg = config['bike.convert']

    # parse config
    truth_df_path = cfg['truth_df_path']
    truth_dist_df_path = cfg['truth_dist_df_path']
    location = [float(cfg['Latitude']), float(cfg['Longitude'])]
    distance_thresh = float(cfg['distance_thresh']) # in meters
    map_save_path = cfg["map_save_path"]
    truck_df_savepath = cfg["truck_df_savepath"]
    bike_df_savepath = cfg["bike_df_savepath"]
    truck_dist_df_savepath = cfg["truck_dist_df_savepath"]
    bike_dist_df_savepath = cfg["bike_dist_df_savepath"]

    # read single-truth dataframe and single-truth distance matrix
    truth_df = pd.read_csv(truth_df_path)
    truth_dist = pd.read_csv(truth_dist_df_path)

    # filter distance mtrx to distances btwn bike-served and truck-served locations
    bike_indices = truth_df[truth_df["pickup_type"] == 'Bike'].index
    bike_dists = truth_dist.iloc[bike_indices.to_list()]
    drop_cols = [str(i) for i in bike_indices]
    bike_to_truck_dists = bike_dists.drop(columns = drop_cols)

    # note which truck-serviced locations are within {distance_thresh} of bike-serviced locations
    converts = []
    for col in bike_to_truck_dists.columns:
        if min(bike_to_truck_dists[col]) <= distance_thresh:
            converts.append(int(col))

    # convert marked truck-serviced locations to bike-servicable locations
    converted_df = truth_df.copy()
    for i in converts:
        converted_df.at[i, "pickup_type"] = 'Bike'

    # prepare output dataframes
    ## info dataframes
    truck_df = converted_df[converted_df["pickup_type"] == 'Truck']
    bike_df = converted_df[converted_df["pickup_type"] == 'Bike']
    ## distance matrices
    total_inds = {i for i in range(len(truth_df))}
    bike_ind = set(bike_indices.to_list() + converts)
    truck_ind = sorted(list(total_inds - bike_ind))
    bike_ind = sorted(list(bike_ind))
    truck_dist_df = truth_dist[[str(i) for i in truck_ind]].iloc[truck_ind]
    bike_dist_df = truth_dist[[str(i) for i in bike_ind]].iloc[bike_ind]

    # export dataframes
    truck_df.to_csv(truck_df_savepath)
    bike_df.to_csv(bike_df_savepath)
    truck_dist_df.to_csv(truck_dist_df_savepath)
    bike_dist_df.to_csv(bike_dist_df_savepath)
    
    map = folium.Map(location = location, tiles ='OpenStreetMap', zoom_start=11)
    add_markers(map, truck_df, 'blue')
    add_markers(map, bike_df, 'red')
    
    map.save(map_save_path)