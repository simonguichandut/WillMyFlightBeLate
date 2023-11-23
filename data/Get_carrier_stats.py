#!/usr/bin/env python
# coding: utf-8

####### Run this code inside the data directory #######

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import gc

Years = np.arange(2012,2024,1)
 
exclude_pandemic = True
if exclude_pandemic:
    Years = np.setdiff1d(Years, [2020,2021])

carrier_data = pd.DataFrame(columns=["Code","Name",
                                     "N","N_delayed","N_2023","N_delayed_2023"])

carrier_codes = pd.read_csv("../data/UNIQUE_CARRIERS.csv")
carrier_codes_dict = carrier_codes.set_index('Code').to_dict()['Description']

delay_thresh=15.

for year in Years:
    print(year)

    for month in range(1,13):

        file = './{}/all_data_month{}.csv'.format(year,month)

        try:
            df = pd.read_csv(file)
        except:
            print("File not found ", file)
            continue

        # Remove canceled
        df = df[df['CANCELLED']==0]

        # Select columns
        df = df[['OP_UNIQUE_CARRIER','DEP_DELAY']]

        # Remove nans
        df = df.dropna()

        # Create delayed column
        df = df.assign(DELAYED=pd.Series(df['DEP_DELAY']>delay_thresh).values.astype(int))
        df = df.drop(columns="DEP_DELAY")

        # Add to airport data
        unique_codes = df['OP_UNIQUE_CARRIER'].unique()
        for code in unique_codes:

            # Create new row if it's not there
            if code not in carrier_data['Code'].values:
                carrier_data.loc[len(carrier_data)] = [code, carrier_codes_dict[code]] + [0 for _ in range(4)]

            # Increment everything

            df_car = df.loc[df['OP_UNIQUE_CARRIER']==code]
            N = len(df_car)
            N_delayed = len(df_car.loc[df_car['DELAYED']==1])
            carrier_data.loc[carrier_data['Code']==code, 'N'] += N
            carrier_data.loc[carrier_data['Code']==code, 'N_delayed'] += N_delayed

            if year==2023:
                carrier_data.loc[carrier_data['Code']==code, 'N_2023'] += N
                carrier_data.loc[carrier_data['Code']==code, 'N_delayed_2023'] += N_delayed

        gc.collect()

# Calculate frac columns
carrier_data['delay_frac'] = carrier_data['N_delayed'] / carrier_data['N']
carrier_data['delay_frac_2023'] = carrier_data['N_delayed_2023'] / carrier_data['N_2023']

carrier_data = carrier_data.drop(columns=['N_delayed','N_delayed_2023'])

# Sort by N, largest to smallest
carrier_data.sort_values(by='N', ascending=False, inplace=True)

print(carrier_data.head(10))

filename = "carrier_stats.csv"
carrier_data.to_csv(filename)