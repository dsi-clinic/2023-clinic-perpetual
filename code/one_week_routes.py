"""
This script will call the "cvrp_optimize_routes.py" script
five times for each day of the week. The result will save a folder
of the new trial, containing routing for each day of the week.

To run this script, in the terminal run:

python one_week_routes.py <arg1> <arg2> <arg3> <arg4> <arg5>

arg 1 = trial #
arg 2 = name of location df you are using
arg 3 = name of corresponding distance matrix df you are using
arg 4 = num_vehicles
arg 5 = num seconds you want each simulation to run
"""

import pandas as pd
import os
import subprocess
import sys

def get_starting_load(cluster_number):
    '''
    '''
    location_df = pd.read_csv("../data/" + str(sys.argv[2]) + ".csv")
    
    cluster_only_dropoff = location_df.loc[location_df.loc[:, "cluster_number"]==cluster_number, "Weekly_Dropoff_Totes"]
    
    location_df.loc[0, "Daily_Pickup_Totes"] = sum(cluster_only_dropoff)

    location_df.to_csv("../data/" + str(sys.argv[2])+ ".csv", index=False)


def perform_one_week_route():
    """
    This function will perform the cvrp_optimize_routes for
    each day of the week, and save the routes as dataframes for
    each day.

    Inputs:
    Outputs: none (saves the routes for each day in the data folder)
    """
    # get_clusters()

    list_of_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    for day_number, day in enumerate(list_of_days):
        # run the cvrp_optimize_routes simulation for that day
        get_starting_load(day_number)
        subprocess.run(
            [
                "python",
                "cvrp_optimize_routes.py",
                str(sys.argv[2]),  # name of location df
                str(sys.argv[3]),  # name of distance matrix df
                str(day_number),
                str(sys.argv[4]),  # num_vehicles
                str(sys.argv[5]),  # num seconds per simulation
                day,
                str(sys.argv[1]),#trial number
            ]
        )
    location_df = pd.read_csv("../data/" + str(sys.argv[2]) + ".csv")
    location_df.loc[0, "Daily_Pickup_Totes"] = 0.0 
    location_df.to_csv("../data/" + str(sys.argv[2])+ ".csv", index=False)

def main():
    """ """
    os.mkdir("../data/trial" + str(sys.argv[1]))
    perform_one_week_route()


if __name__ == "__main__":
    main()
