### Data

This directory contains information for use in this project. 

Please make sure to document each source file here.

*galveston_indoor_pts.csv:* This file contains all the FUEs that will serve as both pickup and dropoff locations for the simulation. Perpetual refers to them as indoor points.

*galveston_outdoor_pts.csv:* This file contains all the locations where Perpetual will place a bin. Perpetual refers to them as outdoor points and will only be used for pickup. This dataset also marks whether a location is going to be served by a bike or a truck. The following is the classification for the id of the bins:
- city approved have IDs starting from 1000
- private parking bins have IDs starting from 2000
- park_board bins have IDs starting from 3000


* `generated_distance_matrices` : folder that contains the distance matrices generated for galveston data 
* `FUE_Galveston.csv` : csv of original FUE points in Galveston
*  `indoor_outdoor_pts_galv.csv` : csv of concatonated indoor and outdoor service locations in Galveston
*  `indoor_outdoor_distances_galv.csv` : csv of the distance matrix for all indoor and outdoor points in galveston (converted from the npy file "distance_matrix_new.npy")

*  `bike_distances_galv.csv` : csv of the distance matrix of bike only service points in the indoor and outdoor dataframes combined
*  `bike_service_pts_galv.csv` : csv of the bike only service points subsetted from the file "indoor_outdoor_pts_galv.csv"
*  `truck_pts_galv_cluster_dropoff.csv` : csv of the truck only service locations in galveston including clusters made by dropoffs (i.e. sum of all dropoffs within cluster approximately the same) 
*  `truck_pts_galv_cluster_pickup.csv` : csv of the truck only service locations in galveston including clusters made by pickups (i.e. sum of all pickups within cluster approximately the same) 

