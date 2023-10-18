'''
This script will run simulations of Google ORTools' Capacited Vehicles Routing Problem 
(CVRP) to determine the optimal number of trucks and routes to deploy in Galveston.

Run this script in the terminal using:
python optimize_cvrp_galv.py <arg1> <arg2>

The two arguments are: 
arg1 = number of vehicles
arg2 = number of seconds in the time limit
'''

import pandas as pd
import numpy as np
import sys 
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


#import the data 
galveston = pd.read_csv("../data/FUE_Galveston.csv")

#load the distance matrix
distance_matrix = np.loadtxt("../data/distance_matrix_g.csv",
                 delimiter=",", dtype=int)


#import sys
#arg 1 = num_vehicles
#arg 2 = num_seconds



def get_demands(location_df):
    '''
    This function will get the daily number of totes to be picked up at 
    every location provided in the df.

    Inputs: location_df = df of all the service locations on the daily truck route
    Outputs: demands_list = a list of the number of totes to be collected at 
                each location daily (in the same order of locations from the df)
    '''
    demands_list = []
    for index, row in location_df.iterrows():
        demands_list.append(int(row["Daily_Pickup_Totes"]))
    
    return demands_list


def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data["distance_matrix"] = distance_matrix.astype(int)
    data["demands"] = get_demands(galveston)
    data["num_vehicles"] = int(sys.argv[1])
    data["vehicle_capacities"] = [150 for i in range(data["num_vehicles"])]
    data["depot"] = 0
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data["demands"][node_index]
            plan_output += f" {node_index} Load({route_load}) -> "
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        plan_output += f" {manager.IndexToNode(index)} Load({route_load})\n"
        plan_output += f"Distance of the route: {route_distance}m\n"
        plan_output += f"Load of the route: {route_load}\n"
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print(f"Total distance of all routes: {total_distance}m")
    print(f"Total load of all routes: {total_load}")



def save_to_table(data, manager, routing, solution):
    """Save each route to its own dataframe and print solutions on the console."""
    print(f"Objective: {solution.ObjectiveValue()}")
    routes = []
    distances = []
    loads = []
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data["num_vehicles"]):
        route = []
        agg_distances = []
        truck_load = []
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data["demands"][node_index]
            plan_output += f" {node_index} Load({route_load}) -> "
            #route.append({node_index:route_load})
            route.append(node_index)
            truck_load.append(route_load)
            agg_distances.append(route_distance)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
            
        plan_output += f" {manager.IndexToNode(index)} Load({route_load})\n"
        route.append(manager.IndexToNode(index))
        truck_load.append(route_load)
        agg_distances.append(route_distance)
        plan_output += f"Distance of the route: {route_distance}m\n"
        plan_output += f"Load of the route: {route_load}\n"
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
        routes.append(route)
        distances.append(agg_distances)
        loads.append(truck_load)
    print(f"Total distance of all routes: {total_distance}m")
    print(f"Total load of all routes: {total_load}")
    return routes, distances, loads




def make_dataframe(data, manager, routing, solution, df):
    '''use the output of save_to_table to save the dataframe as a 
            csv file in the data folder'''
    routes, distances, loads = save_to_table(data, manager, routing, solution)
    for i in range(len(routes)):
        route_df = df.loc[routes[i], :]
        route_df["Cumulative_Distance"] = distances[i]
        route_df["Truck_Load"] =loads[i]
        route_df = route_df.reset_index()
        route_df = route_df.rename(columns={"index": "Original_Index"})
        
        path = "../data/route" + str(i+1) + ".csv"
        route_df.to_csv(path, index = False)


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

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
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

    # Print solution on console.
    if solution:
        #print_solution(data, manager, routing, solution)
        make_dataframe(data, manager, routing, solution, galveston)
        



if __name__ == "__main__":
    main()