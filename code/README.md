### Code

This directory contains python scripts used in this project's pipeline. 

* `GenerateDistMatrix.py` : This is a python script to generate distance matrices for any dataset

*  `optimize_cvrp_galv.py` : This is a python script to run the capacited vehicle routing problem specific to the 'FUE_Galveston.csv' dataset (note: this only includes pickup routing)

*  `one_week_routes.py` : This is a python script to create routing for one week of operation (5 different routing schedules for each day of the week), which includes pickup and dropoff (note: calls the file cvrp_optimize_routes.py)

*  `cvrp_optimize_routes.py` : This is a python script to run the capacited vehicle routing problem on any dataset (includes pickup and dropoff in the routing)

*  add_mg_pickup_150capacity (folder): this folder contains the scripts with modifications to the one week routing script (called one_week_loop1.py) and the optimize cvrp script (called cvrp1.py) to test the Google OR-Tools pickup + dropoff simulation with the following idea: 1. setting the "pickup" at moody gardens to be the total dropoff load for the day (where vehicle capacity = 150), 2. generating demands for each location to be the sum of pickup - dropoff

*  cluster_after_routing (folder): this folder contains the scripts with modifications to the optimize cvrp script (called routing_no_clusters.py) to test the Google OR-Tools pickup + dropoff simulation with the following idea: 1. find optimal routing for pickup only, 2. after these pickup-only routes are made, we can assign clusters for each truck based on the dropoff capacities present in each route [Note: demands are pickup only]

*  divide_starting_capacities (folder): this folder contains the scripts with modifications to the one week routing script (called one_week_loop2.py) and the optimize cvrp script (called cvrp2.py) to test the Google OR-Tools pickup + dropoff simulation with the following idea: 1. sum the total dropoff load in a given cluster, 2. set each truck's vehicale capacity to be 150 - (dropoff load/num_trucks) (i.e. vehicle capacity is decreased by starting load that will contain dropoffs, and the dropoff load is divided evenly among all trucks) [Note: demands are pickup only]

*  separating_cluster_noncluster (folder): this folder contains the scripts with modifications to the one week routing script (called one_week_loop3.py) and the optimize cvrp script (called cvrp3.py) to test the Google OR-Tools pickup + dropoff simulation with the following idea: 1. subset the locations df and distance matrix to cluster only and all non-clustered locations for each day, 2. run the cvrp routing algorithm separately, where one truck will perform routing for all clustered locations (which will perform pickup and dropoff), and the ohter trucks will perform routing for all locations not in the cluster (pickup only) [Note: demands are pickup only]

*  showYiran: this folder contains the scripts with Google OR-Tools' CVRP code copied and executed exactly from the internet (called google_cvrp.py) and another file that copies the same code, but only changes the elements where the locations_data and distance_matrix are created (I imported the datasets for our old Galveston locations) [Note: these scripts are meant to be a test to demonstrate that the time argument in Google's code is breaking down when we try to apply our own examples]
