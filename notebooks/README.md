### Notebook directory

This should contain information about what is done in each notebook

`ORtools_routing_ex.ipynb` : This is a notebook to run the Vehicle Routing Example provided by Google OR Tools.
`mapping_FUE_Galveston.ipynb` : This is a notebook to visulaize the coordinates on the Galveston map using folium.
VRP.ipynb : This notebook was used to run through the Vehicle Routing Problem.
`FUE_Exploration_Galveston.ipynb` : This notebook creates the map visualization for old FUE locations in galveston.
`GAL_Route.ipynb` : This notebook creates the map visualizations of the truck routes created in trial 1 (for the old FUE galveston locations)
`RouteViz.ipynb` : This notebook creates the map visualizations of the truck routes created in trial 1 (for the old FUE galveston locations)
`RouteExperimentation.ipynb` : This notebook experiments with other packages to create the map visualizations of the truck routes created in trial 1 (for the old FUE galveston locations)
`create_full_service_df.ipynb` : This notebook concatonated all the indoor and outdoor locations in galveston. It also opens the distance matrix for all the indoor and outdoor points and saves it as a csv file.
`create_truck_only_df.ipynb` : This notebook subsetted the indoor_outdoor_pts_galv df for truck only service locations. It also subsets the distance matrix for corresponding indeces of truck only locations.
`create_bike_only_df.ipynb` : This notebook subsetted the indoor_outdoor_pts_galv df for bike only service locations. It also subsets the distance matrix for corresponding indeces of bike only locations.
`VRP.ipynb` : This notebook copies and runs the code from Google ORTools' vehicle routing problem
`MappingCAP.ipynb` : This notebook contains an example of how to map routes created using the capacity constraint vehicle routing problem
`separate_dropoff_dfs.ipynb` : This notebook creates 5 subsetted dataframes for each dropoff cluster