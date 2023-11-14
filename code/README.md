# Perpetual

# GenerateDistMatrix.py 
  this file will using the location data to get the distsance between each pair of restaurants from mapbox matrix API and generate 
  n * n matrixs.

# GenerateDistMatrix_sep_BT.py 
  this file take in two csv file from terminal and generate two distance matrix under data file
  run the following script in the terminal:
    python /code/GenerateDistMatrix_sep_BT.py <dir/truck_location.csv> <dir/bike_location.csv>
  output file will be generated as follows:
    "../data/generated_distance_matrices/distance_matrix_{timestamp_str}_truck.npy"
    "../data/generated_distance_matrices/distance_matrix_{timestamp_str}_bike.npy"

# GetWaypoint.py
  this file adds waypoints to each route.
  run the following script in the terminal:
    python /code/GetWaypoint.py <dir/route.csv> 
  output file will be generated as follows under the same file of route.csv:
    sys.argv[1] + "_waypoints.csv"

# Capacity_galveston.py
  run GenerateDistMatrix.py first, the output will stored in the ../data file.
  using both distance_matrices file and capacity_list file (does not include in this branch, but you can find it in the main),
  ortools helped us generates the optimized routes.
  adjust the time constraints, we will get more optimized result.

# RouteWithTime.py
  data: optimized route data
  
  this file will using the data and request the time duration between each stop from mapbox direction API and than accumulates all 
  the time plus 5 min picking up or drop up time at each stop.

# waypoints_visualization.py
  this file visualize all the waypoints and pickup/dropoff locations
  run the following script in the terminal:
    python /code/GetWaypoint.py <dir/route_waypoints.csv> 
  output file will be generated as follows under output file as html:
    "../output/map_with_waypoints.html" 
