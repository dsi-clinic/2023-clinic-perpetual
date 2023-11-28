#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 01:17:30 2023

@author: genie_god
"""

import ast
import configparser

import pandas as pd


def generate_single_source_of_truth():
    # Initialize the parser
    config = configparser.ConfigParser()
    # Read the config file
    # Take file name from config
    config.read("../utils/config_inputs.ini")
    file_name_indoor = config["original data source"]["indoor"]
    file_name_outdoor = config["original data source"]["outdoor"]

    # read indoor and outdoor data file
    df_indoor = pd.read_csv(file_name_indoor)
    df_outdoor = pd.read_csv(file_name_outdoor)

    # update location_type and pickup_type for each dataset
    df_indoor.loc[:, "location_type"] = "indoor"
    df_indoor.loc[:, "pickup_type"] = "truck"
    df_outdoor.loc[:, "Daily_Pickup_Totes"] = 1.0
    df_outdoor.loc[:, "Weekly_Dropoff_Totes"] = 0.0
    df_outdoor.loc[:, "location_type"] = "outdoor"

    # prepare data for analyze
    df_outdoor = df_outdoor.rename(
        columns={"longitude": "Longitude", "latitude": "Latitude"}
    )

    # add tote number info
    # when the indoor and oudoor df don't have pickup/dropoff totes number
    if "Weekly_Dropoff_Totes" not in df_indoor.columns:
        old_galveston = pd.read_csv("../data/FUE_Galveston.csv")
        galveston_sub = old_galveston.loc[
            :, ["Name", "Weekly_Dropoff_Totes", "Daily_Pickup_Totes"]
        ]
        df_indoor = pd.merge(df_indoor, galveston_sub, on="Name", how="left")

    # add source loacation
    source_location = ast.literal_eval(config["original data source"]["source"])

    df_source = pd.DataFrame(
        {"Longitude": [source_location[0]], "Latitude": [source_location[1]]}
    )

    single_source_truth = pd.concat([df_source, df_indoor, df_outdoor])

    # Save single_source to a file
    filename = "../data/single_source_of_truth.csv"
    single_source_truth.to_csv(filename, index=False)

    # Ensure the 'Matrix Dir' section exists
    if "original data source" not in config:
        config["original data source"] = {}

    # Assign the filename to the single_source_of_truth section
    config["original data source"]["single_source_of_truth"] = filename

    # Write the configuration to an INI file
    with open("../utils/config_inputs.ini", "w") as configfile:
        config.write(configfile)

    print(f"single source of truth generated under the file {filename}")
