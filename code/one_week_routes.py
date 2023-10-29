"""
This script will ....
"""

import sys
import os
import subprocess

import numpy as np
import pandas as pd
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import seaborn as sns; sns.set()
import csv

# import sys
# arg 1 = trial #
# arg 2 = name of location df you are using
# arg 3 = name of corresponding distance matrix df you are using 
# arg 4 = num_vehicles


# create the folder where you will store the routing for this trial number
os.mkdir("../data/trial" + str(sys.argv[1]))

#load the location df
location_df = pd.read_csv("../data/" + str(sys.argv[2]) +".csv")
    
# load the distance matrix
distance_matrix = np.loadtxt(
        "../data/" + str(sys.argv[3]) + ".csv", delimiter=",", dtype=int
    )


def get_clusters():
    '''
    '''
    locations = location_df.loc[:, ["Name", "Longitude", "Latitude"]]

    kmeans = KMeans(n_clusters = 5, init ='k-means++')
    kmeans.fit(locations[locations.columns[1:3]]) # Compute k-means clustering.
    locations['cluster_number'] = kmeans.fit_predict(locations[locations.columns[1:3]])
    centers = kmeans.cluster_centers_ # Coordinates of cluster centers.
    labels = kmeans.predict(locations[locations.columns[1:3]]) # Labels of each point

    location_df = pd.merge(location_df, locations.loc[:, ["Name", "cluster_number"]], left_on='Name', right_on='Name')

    location_df.to_csv("../data/" + str(sys.argv[2]) +".csv")



def perform_one_week_route():
    '''
    This function will perform the cvrp_optimize_routes for
    each day of the week, and save the routes as dataframes for 
    each day. 

    Inputs: 
    Outputs: none (saves the routes for each day in the data folder)
    '''
    get_clusters()

    list_of_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    for day_number, day in enumerate(list_of_days):
        #run the cvrp_optimize_routes simulation for that day
        # inputs: arg1 = name of the df for tote service locations
        #         arg2 = name of the df of corresponding ditance matrix
        #         arg3 = day_number 
        #         arg4 = number of vehicles
        routes, distances, loads = subprocess.run(["python", "cvrp_optimize_routs.py", 
                             str(sys.argv[2]), 
                             str(sys.argv[3]), 
                             day_number, 
                             int(sys.argv[4])])
        for i in range(len(routes)):
            route_df = location_df.loc[routes[i], :]
            route_df["Cumulative_Distance"] = distances[i]
            route_df["Truck_Load"] = loads[i]
            route_df = route_df.reset_index()
            route_df = route_df.rename(columns={"index": "Original_Index"})
            #create the folder for the day that will be stored
            os.mkdir("../data/trial" + str(sys.argv[1]) + "/" + day)
            #generate the path for the route file
            path = "../data/trial" + str(sys.argv[1]) + "/" + day + "/route" + str(i + 1) + ".csv"
            #save the route file 
            route_df.to_csv(path, index=False)
         
    




        

