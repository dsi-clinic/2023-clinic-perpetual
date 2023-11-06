"""
This script will call the "cvrp3.py" script
five times for each day of the week. The result will save a folder
of the new trial, containing routing for each day of the week.

To run this script in the terminal, run:

python one_week_loop3.py <arg1> <arg2> <arg3> <arg4> <arg5>

arg 1 = trial #
arg 2 = name of location df you are using
arg 3 = name of corresponding distance matrix df you are using
arg 4 = num_vehicles
arg 5 = num seconds you want each simulation to run
"""

import os
import subprocess
import sys

import pandas as pd


def get_vehicle_capacity(cluster_number):
    """
    This function

    inputs: cluster_number = the cluster number you are subsetting
                            for given day of the week
    outputs: int =  the vehicle capacity for the one vehicle
                    that will be dropping off totes
    """
    location_df = pd.read_csv("../../data/" + str(sys.argv[2]) + ".csv")

    cluster_only_dropoff = location_df.loc[
        location_df.loc[:, "cluster_number"] == (cluster_number + 1),
        "Weekly_Dropoff_Totes",
    ]

    dropoff_total = sum(cluster_only_dropoff)
    return 150 - int(dropoff_total)


def perform_one_week_route():
    """
    This function will perform the cvrp route optimization for
    each day of the week for the clustered dropoff locations,
    and save the routes as dataframes for
    each day.

    Inputs:
    Outputs: none (saves the routes for each day in the data folder)
    """

    list_of_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    for day_number, day in enumerate(list_of_days):
        # create the folder for the day that will be stored
        os.mkdir("../data/trial" + str(sys.argv[7]) + "/" + str(sys.argv[6]))
        # run the cvrp_optimize_routes simulation for clustered dropoff
        subprocess.run(
            [
                "python",
                "cvrp3.py",
                str(sys.argv[2]),  # name of location df
                str(sys.argv[3]),  # name of distance matrix df
                str(day_number + 1),
                1,  # num_vehicles
                str(sys.argv[5]),  # num seconds per simulation
                day,
                str(sys.argv[1]),  # trial number
                get_vehicle_capacity(day_number),  # vehicle capacity
            ]
        )
        # run the cvrp_optimize_routes simulation for non-clustered points
        subprocess.run(
            [
                "python",
                "cvrp3.py",
                str(sys.argv[2]),  # name of location df
                str(sys.argv[3]),  # name of distance matrix df
                str(day_number + 1),
                str(int(sys.argv[5]) - 1),  # num_vehicles
                str(sys.argv[5]),  # num seconds per simulation
                day,
                str(sys.argv[1]),  # trial number
                150,  # vehicle capacity
            ]
        )


def main():
    """ """
    os.mkdir("../../data/trial" + str(sys.argv[1]))
    # clustered dropoff is route1, all other locations are route2+
    perform_one_week_route()


if __name__ == "__main__":
    main()
