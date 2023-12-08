# Code

* `bike_conversion.py`: Converts truck-serviced points to bike-serviced points when near other bike-serviced points
  * Aggregate pickup/dropoff loads to designated aggregation points
  * Separate .csv outputs into bike-only and truck-only datasets

* `GenerateSingleSourceofTruth.py`: 
  This is a python script to clean the data and create the single source of truth dataframe that will be used for all location points in a given city.
* `extract_capacity_demands.py`: extract pickup/dropoff demands for all locations
* `extract_supplementary_info.py`: extract supplementary info for all locations (to help with visualization)
* `GenerateDistMatrix.py`: This is a python script to generate distance matrices for any dataset
* `optimize_cvrp.py`: 
  Performs route optimization using the Google ORTools Capacitated Vehicle Routing Problem algorithm; can be generalized and applied to any locations dataset and any constraint inputs by changing arguments in the utils/config_inputs.ini
* `RouteViz.py`: Given a folder/directory of routes, create interactive visualizations (.html).



* `RouteWithTime.py` :
  data: optimized route data
  
  this file will using the data and request the time duration between each stop from mapbox direction API and than accumulates all 
  the time plus 5 min picking up or drop up time at each stop.

  
* `GetWayPoint.py` :
  data: optimized route data

  this file will using the data and request the waypoints through the route along with the instructions for driving

* `complete_feasibility_report.py` :
  Use this script to add a new row to the output/feasibilityfile.csv which records the inputs and outputs generated from running a new model. This script will interact with the utils/config.ini file to grab inputs and outputs from the pipeline and update the feasibility report for each new trial 
