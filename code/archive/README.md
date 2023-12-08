
# Code archive


* `optimize_cvrp_galv_old.py` : 
  This is a python script to run the capacited vehicle routing problem specific to the 'FUE_Galveston.csv' (trial 1) dataset (note: this only includes pickup routing)

* `capacitatedVRP.py` : 
  This is a python script to run the capacited vehicle routing problem specific to the 'FUE_Galveston.csv' (trial 1) dataset (note: this only includes pickup routing)

* `Capacity_galveston.py` :
  run GenerateDistMatrix.py first, the output will stored in the ../data file.
  using both distance_matrices file and capacity_list file (does not include in this branch, but you can find it in the main),
  ortools helped us generates the optimized routes.
  adjust the time constraints, we will get more optimized result.


* `ClusteringGAL.py` : 
  This is a python script to create clusters of the Galveston dataset based on pickup or dropoff quantities 

* `cvrp_galv_dropoff_only.py` : 
  This is a python script to run the capacited vehicle routing problem specific to tracking dropoff capacities only (generalized so you can change arguments specific to your question)

* `cvrp_galv_pickup_only.py` : 
  This is a python script to run the capacited vehicle routing problem specific to tracking pickup capacities only (generalized so you can change arguments specific to your question)




