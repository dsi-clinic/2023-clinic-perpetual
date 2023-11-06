"""
This script will call the "cvrp_optimize_routes.py" script
five times for each day of the week. The result will save a folder
of the new trial, containing routing for each day of the week.

To run this script in the terminal, run:

python one_week_loop2.py <arg1> <arg2> <arg3> <arg4> <arg5>

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


def perform_one_week_route():
    """
    This function will perform the cvrp_optimize_routes for
    each day of the week, and save the routes as dataframes for
    each day.

    Inputs:
    Outputs: none (saves the routes for each day in the data folder)
    """

    list_of_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    for day_number, day in enumerate(list_of_days):
        # run the cvrp_optimize_routes simulation for that day
        subprocess.run(
            [
                "python",
                "cvrp2.py",
                str(sys.argv[2]),  # name of location df
                str(sys.argv[3]),  # name of distance matrix df
                str(day_number + 1),
                str(sys.argv[4]),  # num_vehicles
                str(sys.argv[5]),  # num seconds per simulation
                day,
                str(sys.argv[1]),  # trial number
            ]
        )



def main():
    """ """
    os.mkdir("../../data/trial" + str(sys.argv[1]))
    perform_one_week_route()


if __name__ == "__main__":
    main()