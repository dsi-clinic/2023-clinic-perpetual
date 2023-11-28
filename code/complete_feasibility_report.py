'''
complete_feasibility_report.py

This script interacts with the utils/config.ini file to 
grab inputs and outputs from the pipeline and update 
the feasibility report in place for each new trial 

Author: Sarah Walker
'''

import pandas as pd 
import configparser


#open the feasibility file so you can make edits
feasibility_report = pd.read_csv("../output/feasibilityfile.csv")

#create the config object that will interact with the inputs and outputs
config = configparser.ConfigParser()
config.read("path/config_inputs.ini")


# fill in each column in the feasibility file by grabbing 
# the arguments from the config file
# for example... 
feasibility_report["distance_matrix"] = config["optimize google cvrp"]["path_to_distance_matrix"]
feasibility_report["num_routes"] = config["optimize google cvrp"]["num_vehicles"].astype(int)



#save the changes back to the file
feasibility_report.to_csv("../output/feasibilityfile.csv")


## I need to finish this when 
# 1. we edit the feasibilityfile into a readable format
# 2. we have all the config arguments from each team member merged into one file