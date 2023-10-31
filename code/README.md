### Code

This directory contains python scripts used in this project's pipeline. 

* `GenerateDistMatrix.py` : This is a python script to generate distance matrices for any dataset

*  `optimize_cvrp_galv.py` : This is a python script to run the capacited vehicle routing problem specific to the 'FUE_Galveston.csv' dataset (note: this only includes pickup routing)

*  `one_week_routes.py` : This is a python script to create routing for one week of operation (5 different routing schedules for each day of the week), which includes pickup and dropoff

*  `cvrp_optimize_routes.py` : This is a python script to run the capacited vehicle routing problem on any dataset (includes pickup and dropoff in the routing)
