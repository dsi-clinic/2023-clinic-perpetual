# Perpetual

# GenerateDistMatrix.py 
  this file will using the location data to get the distsance between each pair of restaurants from mapbox matrix API and generate 
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
