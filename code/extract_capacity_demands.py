# produce capacity list from the single-truth dataframe (used for routing)

if __name__ == '__main__':
    # read config
    config = configparser.ConfigParser()
    config.read('../utils/config.ini')
    cfg = config['extract.capacity_demands']

    # parse config
    truth_df_path = cfg['truth_df_path']
    capacity_df_savepath = cfg['capacity_df_savepath']
    
    # read single-truth dataframe
    truth_df = pd.read_csv(truth_df_path)

    # prepare capacity dataframe
    capacities = truth_df[['Daily_Pickup_Totes', 'Weekly_Dropoff_Totes']]

    # save capacity dataframe
    capacities.to_csv(capacity_df_savepath)