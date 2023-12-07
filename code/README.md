# Code

* `GenerateSingleSourceofTruth.py`: 
  This is a python script to clean the data and create the single source of truth dataframe that will be used for all location points in a given city.

* `GenerateDistMatrix.py`: 
  This is a python script to generate distance matrices for any dataset

* `extract_capacity_demands.py` : 
  This python script will collect pickup and dropoff capacities at each location to be used in the routing

* `extract_supplementary_info.py` : 
  This python script will collect and save information from each location that can later be added to the pop-ups on the route mapping


* `RouteWithTime.py` :
  data: optimized route data
  
  this file will using the data and request the time duration between each stop from mapbox direction API and than accumulates all 
  the time plus 5 min picking up or drop up time at each stop.

* `RouteViz.py` :
  data: FUE's in order of route

  this file will graph routes from an order of locations using free libraries and will output routes in HTML format. 

  
* `GetWayPoint.py` :
  data: optimized route data

  this file will using the data and request the waypoints through the route along with the instructions for driving


* `complete_feasibility_report.py`: 
  this script interacts with the utils/config.ini file to grab inputs and outputs from the pipeline and update the feasibility report for each new trial 

* `perpetual_pipeline.py`: 
  This is the pipeline for our project.