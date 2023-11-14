This directory contains python scripts used in this project's pipeline.

* `GenerateDistMatrix.py`: This is a python script to generate distance matrices for any dataset

* `optimize_cvrp_galv_old.py` : This is a python script to run the capacited vehicle routing problem specific to the 'FUE_Galveston.csv' dataset (note: this only includes pickup routing)

* `capacity_galveston.py` : This is a python script to run the capacited vehicle routing problem specific to the 'FUE_Galveston.csv' dataset (note: this only includes pickup routing)

* `RouteViz.py`: This python script graphs the routing dataframes after they have been generated. 

* `RouteWithTime.py`: This python script collects the waypoints of the routing dataframes.

* `cvrp_galv_dropoff_only.py` : This is a python script to run the capacited vehicle routing problem specific to tracking dropoff capacities only (generalized so you can change arguments specific to your question)

* `cvrp_galv_pickup_only.py` : This is a python script to run the capacited vehicle routing problem specific to tracking pickup capacities only (generalized so you can change arguments specific to your question)



