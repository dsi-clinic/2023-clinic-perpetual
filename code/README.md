# Code

* `bike_conversion.py`: Converts truck-serviced points to bike-serviced points when near other bike-serviced points
  * Aggregate pickup/dropoff loads to designated aggregation points
  * Separate .csv outputs into bike-only and truck-only datasets
* `extract_capacity_demands.py`: extract pickup/dropoff demands for all locations
* `extract_supplementary_info.py`: extract supplementary info for all locations (to help with visualization)
* `GenerateDistMatrix.py`: This is a python script to generate distance matrices for any dataset
* `RouteViz.py`: Given a folder/directory of routes, create interactive visualizations (.html).

# RouteWithTime.py
  data: optimized route data
  
  this file will using the data and request the time duration between each stop from mapbox direction API and than accumulates all 
  the time plus 5 min picking up or drop up time at each stop.
  
  # GetWayPoint.py
  data: optimized route data
  
  this file will using the data and request the waypoints through the route along with the instructions for driveing

### Pipeline

1. bike_conversion.py
2. RouteViz.py