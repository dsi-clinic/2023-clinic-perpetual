### Notebook directory


`create_full_service_df.ipynb` : This notebook concatonated all the indoor and outdoor locations in galveston. It also opens the distance matrix for all the indoor and outdoor points and saves it as a csv file.
`create_truck_only_df.ipynb` : This notebook subsetted the indoor_outdoor_pts_galv df for truck only service locations. It also subsets the distance matrix for corresponding indeces of truck only locations.
`create_bike_only_df.ipynb` : This notebook subsetted the indoor_outdoor_pts_galv df for bike only service locations. It also subsets the distance matrix for corresponding indeces of bike only locations.
`GurobiGal.ipynb` : notebook to build model and run routing example using the Gurobi optimizer (for Galveston indoor and outdoor locations)
