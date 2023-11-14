### Data

This directory contains information for use in this project. 

Please make sure to document each source file here.

* `FUE_Galveston.csv` : CSV file containing participating Galveston FUEs & their information

*  `route1.csv` : CSV file containing the route for one of the trucks delivering totes for GAL FUEs

*  `route2.csv` : CSV file containing the route for the second truck delivering totes for GAL FUEs

*galveston_indoor_pts.csv:* This file contains all the FUEs that will serve as both pickup and dropoff locations for the simulation. Perpetual refers to them as indoor points.

*galveston_outdoor_pts.csv:* This file contains all the locations where Perpetual will place a bin. Perpetual refers to them as outdoor points and will only be used for pickup. This dataset also marks whether a location is going to be served by a bike or a truck. The following is the classification for the id of the bins:
- city approved have IDs starting from 1000
- private parking bins have IDs starting from 2000
- park_board bins have IDs starting from 3000

*route1_waypoints.csv:* This file is an example file for Waypoints pulled from mapbox api, file will be changed with the real data, same for route2_waypoints.csv

*distance_matrix_20231029_220129.npy:* updated distance matrix with both indoor and outdoor points

*clustered_data.csv* File containing locations of indoor and outdoor points along with their clusters based on distance of each FUE.

*pickup_totes.csv* File containing the binned indoor and outdoor points of Galveston based on location pickup capacity. 

*dropoff_totes.csv* File containing the binned indoor and outdoor poitns of Galveston based on lcoation's dropoff capacity. 
