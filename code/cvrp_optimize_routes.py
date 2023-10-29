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
"""

import sys

import numpy as np
import pandas as pd
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

#load the location df
location_df = pd.read_csv("../data/" + str(sys.argv[1]) +".csv")
    
# load the distance matrix
distance_matrix = np.loadtxt(
        "../data/" + str(sys.argv[2]) + ".csv", delimiter=",", dtype=int
    )


def get_pickup_demands(location_df):
    """
    This function will get the daily number of totes to be
    picked up at every location provided in the df.

    Inputs: location_df = df of all the service locations
                        on the daily truck route
    Outputs: pickup_demands = a list of the number of totes to be collected
                            at each location daily
                            (in the same order of locations from the df)
    """
    pickup_demands = []
    for index, row in location_df.iterrows():
        pickup_demands.append(int(row["Daily_Pickup_Totes"]))

    return pickup_demands


def get_dropoff_demands(location_df, cluster_number):
    '''
    This function will get the number of totes to be
    dropped off at specified locations for the 
    given day.

    Inputs: location_df = df of all the service locations
                        on the daily truck route
            cluster_number = day of dropoff service
    Outputs: dropoff_demands = a list of the number of totes to be dropped off
                            at each location daily (will be 0 at the locations
                            which are not receiving totes that day)
                            (in the same order of locations from the df)
    '''
    dropoff_demands = []
    for index, row in location_df.iterrows():
        if row["cluster_number"] == cluster_number:
            dropoff_demands.append(int(row["Weekly_Dropoff_Totes"]))
        else:
            dropoff_demands.append(0)

    return dropoff_demands


def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data["distance_matrix"] = distance_matrix.astype(int)
    data["pickup_demands"] = get_pickup_demands(location_df)
    data["dropoff_demands"] = get_dropoff_demands(location_df, int(sys.argv[3]))
    data["num_vehicles"] = int(sys.argv[5])
    data["vehicle_capacities"] = [150 for i in range(data["num_vehicles"])]
    data["depot"] = 0
    return data


#comment out all lines pertaining to the print statements
def save_to_table(data, manager, routing, solution):
    """Save each route to its own dataframe"""
    #print(f"Objective: {solution.ObjectiveValue()}")
    routes = []
    distances = []
    loads = []
    total_distance = 0
    total_load = 0

    #create a route for each vehicle
    for vehicle_id in range(data["num_vehicles"]):
        route = []
        agg_distances = []
        index = routing.Start(vehicle_id)
        #plan_output = f"Route for vehicle {vehicle_id}:\n"
        route_distance = 0
        route_load = sum(dropoff_demands)
        truck_load = []
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data["pickup_demands"][node_index]
            route_load -= data["dropoff_demands"][node_index]
            #plan_output += f" {node_index} Load({route_load}) -> "
            route.append(node_index)
            truck_load.append(route_load)
            agg_distances.append(route_distance)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )

        #plan_output += f" {manager.IndexToNode(index)} Load({route_load})\n"
        route.append(manager.IndexToNode(index))
        truck_load.append(route_load)
        agg_distances.append(route_distance)
        #plan_output += f"Distance of the route: {route_distance}m\n"
        #plan_output += f"Load of the route: {route_load}\n"
        #print(plan_output)
        total_distance += route_distance
        total_load += route_load
        routes.append(route)
        distances.append(agg_distances)
        loads.append(truck_load)
    #print(f"Total distance of all routes: {total_distance}m")
    #print(f"Total load of all routes: {total_load}")
    return routes, distances, loads



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
        True,  # start cumul to zero
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
    search_parameters.time_limit.FromSeconds(int(sys.argv[2]))

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Return solution.
    if solution:
        # print_solution(data, manager, routing, solution)
        routes, distances, loads = save_to_table(data, manager, routing, solution)
        return routes, distances, loads


if __name__ == "__main__":
    main()
