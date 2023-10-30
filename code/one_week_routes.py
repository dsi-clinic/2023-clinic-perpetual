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
# arg 5 = num seconds you want each simulation to run


# create the folder where you will store the routing for this trial number
os.mkdir("../data/trial" + str(sys.argv[1]))


# def get_clusters():
#     '''
#     source: https://levelup.gitconnected.com/clustering-gps-co-ordinates-forming-regions-4f50caa7e4a1
#     '''
#     locations = location_df.loc[:, ["Name", "Longitude", "Latitude"]]

#     kmeans = KMeans(n_clusters = 5, init ='k-means++')
#     kmeans.fit(locations[locations.columns[1:3]]) # Compute k-means clustering.
#     locations['cluster_number'] = kmeans.fit_predict(locations[locations.columns[1:3]])
#     centers = kmeans.cluster_centers_ # Coordinates of cluster centers.
#     labels = kmeans.predict(locations[locations.columns[1:3]]) # Labels of each point

#     location_df = pd.merge(location_df, locations.loc[:, ["Name", "cluster_number"]], left_on='Name', right_on='Name')

#     location_df.to_csv("../data/" + str(sys.argv[2]) +".csv")



def perform_one_week_route():
    '''
    This function will perform the cvrp_optimize_routes for
    each day of the week, and save the routes as dataframes for 
    each day. 

    Inputs: 
    Outputs: none (saves the routes for each day in the data folder)
    '''
    #get_clusters()

    list_of_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    for day_number, day in enumerate(list_of_days):
        #run the cvrp_optimize_routes simulation for that day
        subprocess.run(["python", "cvrp_optimize_routes.py", 
                             str(sys.argv[2]), #name of location df
                             str(sys.argv[3]), #name of distance matrix df
                             str(day_number), 
                             str(sys.argv[4]), #num_vehicles 
                             str(sys.argv[5]), #num seconds per simulation
                             day,
                             str(sys.argv[1])]) #trial number
        
         

def main():
    '''
    '''
    perform_one_week_route()

if __name__ == "__main__":
    main()




        

