"""
This script will run simulations of
Google ORTools' Capacited Vehicles Routing Problem
(CVRP) to determine the optimal number of trucks and
routes to deploy based on a given dataset of locations.

The arguments are:
arg1 = name of the df for tote service locations
arg2 = name of the df of corresponding ditance matrix
arg3 = day_number
arg4 = number of vehicles
arg5 = num seconds of simulation
arg6 = day
arg7 = trial number
arg8 = vehicle_capacity
"""
import sys

import pandas as pd
from ortools.constraint_solver import pywrapcp, routing_enums_pb2


def get_dataframes(df_name, clustered_bool):
    """
    imports the locations df and distance matrix df to be used.
    Needs to subset cluster only and non-cluster only locations
    for each day.

    inputs: df_name = name to the locations dataframe in the data folder
            clustered_bool = boolean for whether the data will be subsetted
                            for cluster only points (True)
                            or non-cluster only points (False)

    outputs: locations_subset, distances_subset
            these are subsetted dataframes (either for cluster or non_cluster)
    """
    # import full locations and distance matrix points from data folder
    location_df = pd.read_csv("../../data/" + df_name + ".csv")
    distance_matrix = pd.read_csv("../../data/" + df_name + ".csv")

    # grab list of indicies for cluster points
    cluster_indices = location_df.loc[
        (location_df.loc[:, "cluster_number"] == sys.argv[3]), :
    ].index.values.tolist()

    num_non_cluster = len(location_df) - len(cluster_indices)

    # subset cluster only points
    if clustered_bool:
        # subset locations_df to cluster indicies and reset index
        location_df = location_df.loc[cluster_indices, :]
        location_df.reset_index(inplace=True, drop=True)

        # select rows and columns in distance matrix to cluster only
        cluster_columns = [str(i) for i in cluster_indices]
        distance_matrix = distance_matrix.loc[cluster_indices, cluster_columns]
        # reset index and columns
        distance_matrix.reset_index(inplace=True, drop=True)
        distance_matrix.columns = [str(i) for i in len(cluster_indices)]

    # subset non-clustered points
    else:
        # drop cluster indicies from locations_df and reset index
        location_df = location_df.drop(cluster_indices, axis=0)
        location_df.reset_index(inplace=True, drop=True)

        # drop cluster rows and columns in distance matrix
        cluster_columns = [str(i) for i in cluster_indices]
        distance_matrix = distance_matrix.drop(cluster_indices, axis=0)
        distance_matrix = distance_matrix.drop(cluster_columns, axis=1)
        # reset index and columns
        distance_matrix.reset_index(inplace=True, drop=True)
        distance_matrix.columns = [str(i) for i in range(num_non_cluster)]

    return location_df, distance_matrix


def get_demands(location_df):
    """
    This function will get the daily number of totes to be
    picked up at every location provided in the df.

    Inputs: location_df = df of all the service locations
                        on the daily truck route
    Outputs: demands_list = a list of the number of totes to be collected
                            at each location daily
                            (in the same order of locations from the df)
    """
    demands_list = []
    for index, row in location_df.iterrows():
        demands_list.append(int(row["Daily_Pickup_Totes"]))

    return demands_list


def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data["num_vehicles"] = int(sys.argv[4])
    data["vehicle_capacities"] = [
        int(sys.argv[8]) for i in range(data["num_vehicles"])
    ]

    # create the subsetted location and distance matrix df
    # depending on whether we are running a cluster only or non-cluster only
    if int(sys.argv[8]) < 150:
        location_df, distance_matrix = get_dataframes(str(sys.argv[1]), True)
    else:
        location_df, distance_matrix = get_dataframes(str(sys.argv[1]), False)

    data["distance_matrix"] = distance_matrix.astype(int)
    data["demands"] = get_demands(location_df)
    data["depot"] = 0
    return data


def save_to_table(data, manager, routing, solution):
    """Save each route to its own dataframe"""
    routes = []
    distances = []
    loads = []
    total_distance = 0
    total_load = 0

    # create a route for each vehicle
    for vehicle_id in range(data["num_vehicles"]):
        route = []
        agg_distances = []
        index = routing.Start(vehicle_id)

        route_distance = 0
        route_load = 0
        truck_load = []
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data["demands"][node_index]

            route.append(node_index)
            truck_load.append(route_load)
            agg_distances.append(route_distance)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )

        route.append(manager.IndexToNode(index))
        truck_load.append(route_load)
        agg_distances.append(route_distance)
        total_distance += route_distance
        total_load += route_load
        routes.append(route)
        distances.append(agg_distances)
        loads.append(truck_load)

    return routes, distances, loads


def make_dataframe(data, manager, routing, solution):
    """use the output of save_to_table to save the dataframe as a
    csv file in the data folder"""
    routes, distances, loads = save_to_table(data, manager, routing, solution)

    if data["vehicle_capacities"][0] < 150:
        df, _ = get_dataframes(str(sys.argv[1]), True)
        route_df = df.loc[routes[0], :]
        route_df["Cumulative_Distance"] = distances[0]
        route_df["Truck_Load"] = loads[0]
        route_df = route_df.reset_index()
        route_df = route_df.rename(columns={"index": "Original_Index"})
        path = (
            "../data/trial"
            + str(sys.argv[7])
            + "/"
            + str(sys.argv[6])
            + "/route1.csv"
        )
        # save the route file
        route_df.to_csv(path, index=False)

    else:
        df, _ = get_dataframes(str(sys.argv[1]), False)
        for i in range(len(routes)):
            route_df = df.loc[routes[i], :]
            route_df["Cumulative_Distance"] = distances[i]
            route_df["Truck_Load"] = loads[i]
            route_df = route_df.reset_index()
            route_df = route_df.rename(columns={"index": "Original_Index"})

            path = (
                "../data/trial"
                + str(sys.argv[7])
                + "/"
                + str(sys.argv[6])
                + "/route"
                + str(i + 2)
                + ".csv"
            )
            # save the route file
            route_df.to_csv(path, index=False)


def main():
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data["demands"][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback
    )
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data["vehicle_capacities"],  # vehicle maximum capacities
        False,  # start cumul to zero
        "Capacity",
    )

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.FromSeconds(int(sys.argv[5]))

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Return solution.
    if solution:
        make_dataframe(data, manager, routing, solution)


if __name__ == "__main__":
    main()
