# Code

* `bike_conversion.py`: Converts truck-serviced points to bike-serviced points when near other bike-serviced points
  * Aggregate pickup/dropoff loads to designated aggregation points
  * Separate .csv outputs into bike-only and truck-only datasets
* `extract_capacity_demands.py`: Extract pickup/dropoff demands for all locations
* `extract_supplementary_info.py`: Extract supplementary info for all locations (to help with visualization)
* `GenerateDistMatrix.py`: Generate distance matrices for any dataset
* `RouteViz.py`: Given a folder/directory of routes, create interactive visualizations (.html).
* `GenerateSingleSourceofTruth.py`: Clean data and create the single source of truth dataframe that will be used for all location points in a given city.
* `RouteWithTime.py`: Calculates total travel time for a given route. It requests time taken to travel between each stop from the Mapbox API, and adds 5 min for each pick-up or drop-off stop and then sums up all these time durations to get the total time taken to travel the given route.
* `GetWayPoint.py`: Requests waypoints on routes, along with the instructions for driving, from the Mapbox API.

### Pipeline

1. bike_conversion.py
2. RouteViz.py
* `complete_feasibility_report.py`: 
  this script interacts with the utils/config.ini file to grab inputs and outputs from the pipeline and update the feasibility report for each new trial 

* `perpetual_pipeline.py`: 
  This is the pipeline for our project.