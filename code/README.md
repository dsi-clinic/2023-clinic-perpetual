
This directory contains python scripts used in this project's pipeline.

* `GenerateDistMatrix.py`: This is a python script to generate distance matrices for any dataset

* `optimize_cvrp_galv_old.py` : This is a python script to run the capacited vehicle routing problem specific to the 'FUE_Galveston.csv' dataset (note: this only includes pickup routing)

* `capacity_galveston.py` : This is a python script to run the capacited vehicle routing problem specific to the 'FUE_Galveston.csv' dataset (note: this only includes pickup routing)

* `RouteViz.py`: This python script graphs the routing dataframes after they have been generated. 

* `RouteWithTime.py`: This python script collects the waypoints of the routing dataframes.

* `cvrp_galv_dropoff_only.py` : This is a python script to run the capacited vehicle routing problem specific to tracking dropoff capacities only (generalized so you can change arguments specific to your question)

* `cvrp_galv_pickup_only.py` : This is a python script to run the capacited vehicle routing problem specific to tracking pickup capacities only (generalized so you can change arguments specific to your question)


# Perpetual

# GenerateDistMatrix.py 
  this file will using the location data to get the distsance between each pair of restaurants from mapbox matrix API and generate
  second updated version concatenated both indoor and outdoor data 
  n * n matrixs.

# Capacity_galveston.py
  run GenerateDistMatrix.py first, the output will stored in the ../data file.
  using both distance_matrices file and capacity_list file (does not include in this branch, but you can find it in the main),
  ortools helped us generates the optimized routes.
  adjust the time constraints, we will get more optimized result.

# RouteWithTime.py
  data: optimized route data
  
  this file will using the data and request the time duration between each stop from mapbox direction API and than accumulates all 
  the time plus 5 min picking up or drop up time at each stop.
  
  # GetWayPoint.py
  data: optimized route data
  
  this file will using the data and request the waypoints through the route along with the instructions for driveing

