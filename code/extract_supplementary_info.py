# produce supplementary info about point (used for the map popups)

import configparser

import pandas as pd

if __name__ == "__main__":
    # read config
    config = configparser.ConfigParser()
    config.read("../utils/config.ini")
    cfg = config["extract.supp_info"]

    # parse config
    truth_df_path = cfg["truth_df_path"]
    supp_info_df_savepath = cfg["supp_info_df_savepath"]

    # read single-truth dataframe
    truth_df = pd.read_csv(truth_df_path)

    # prepare supp_info dataframe
    supp_info = truth_df[
        [
            "Name",
            "Daily_Pickup_Totes",
            "Weekly_Dropoff_Totes",
            "category",
            "Address",
            "location_type",
            "pickup_type",
        ]
    ]

    # save supp_info dataframe
    supp_info.to_csv(supp_info_df_savepath)
