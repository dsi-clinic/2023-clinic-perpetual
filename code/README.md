# Code

* `GenerateDistMatrix.py`: This is a python script to generate distance matrices for any dataset

# RouteWithTime.py
  data: optimized route data
  
  this file will using the data and request the time duration between each stop from mapbox direction API and than accumulates all 
  the time plus 5 min picking up or drop up time at each stop.
  
# GetWayPoint.py
  data: optimized route data
  
  this file will using the data and request the waypoints through the route along with the instructions for driveing


* `RouteViz.py`: This python script graphs the routing dataframes after they have been generated. 

* `RouteWithTime.py`: This python script collects the waypoints of the routing dataframes.

* `optimize_cvrp.py` : This is a python script to run the capacited vehicle routing problem for locations dataframe (generalized so you can change arguments such as: pickup or dropoff, number of vehicles, vehicle capacity, path where to save routing dataframes, input dataframe, input distance matrix)


* `complete_feasibility_report.py`: this script interacts with the utils/config.ini file to grab inputs and outputs from the pipeline and update the feasibility report for each new trial 


