### Data

This directory contains information for use in this project. 

* `distance_matrix_trial1.csv` : csv of distance matrix for original galveston FUE dataframe
* `distance_matrix_new.npy` : a numpy array of the distance matrix for indoor and outdoor galveston FUEs
* `FUE_Galveston.csv` : csv of original FUE points in Galveston
*  `galveston_indoor_pts.csv` : csv of indoor only service points in galveston
*  `galveston_outdoor_pts.csv` : csv of outdoor only service points in galveston
*  `indoor_outdoor_pts_galv.csv` : csv of concatonated indoor and outdoor service locations in Galveston
*  `indoor_outdoor_distances_galv.csv` : csv of the distance matrix for all indoor and outdoor points in galveston (converted from the npy file "distance_matrix_new.npy")
*  `truck_distances_galv.csv` : csv of the distance matrix of truck only service points in the indoor and outdoor dataframes combined
*  `truck_service_pts_galv.csv` : csv of the truck only service points subsetted from the file "full_service_locations.csv"
*  `truck_pts_galv_cluster_dropoff.csv` : csv of the truck only service locations in galveston including clusters made by dropoffs (i.e. sum of all dropoffs within cluster approximately the same) 
*  `truck_pts_galv_cluster_pickup.csv` : csv of the truck only service locations in galveston including clusters made by pickups (i.e. sum of all pickups within cluster approximately the same) 
* 'trial1': folder that contains the routing files for two trucks in the first trial of the galveston simulation (contains route1.csv and route2.csv files)