# Perpetual

# GenerateDistMatrix.py 
  input data: includes both indoor and outdoor datas, and one source location
  output data: distance_matrix_{timestamp_str}.npy saved under data file
  this file will using the location data to get the distsance between each pair of restaurants from mapbox matrix API and generate

# Capacity_galveston.py
  run GenerateDistMatrix.py first, the output will stored in the ../data file.
  using both distance_matrices file and capacity_list file (does not include in this branch, but you can find it in the main),
  ortools helped us generates the optimized routes.
  adjust the time constraints, we will get more optimized result.

# RouteWithTime.py
  input data: optimized route data under data file, take a list of csv file from terminal
  output data: duration_df_{i}.csv saved under data file
  this file will using the data and request the time duration between each stop from mapbox direction API and than accumulates all 
  the time plus 5 min picking up or drop up time at each stop.
  
  # GetWayPoint.py
  input data: optimized route data under data file, take a list of csv file  from terminal
  output data: waypoints_df_{i}.csv saved under data file
  this file will using the data and request the waypoints through the route along with the instructions for driving

