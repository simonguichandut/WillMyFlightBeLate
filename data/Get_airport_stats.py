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

airport_data = pd.DataFrame(columns=["ID","Name",
                                     "N_from","N_delayed_from","N_from_2023","N_delayed_from_2023",
                                     "N_to","N_delayed_to","N_to_2023","N_delayed_to_2023"])

airport_ids = pd.read_csv("AIRPORT_ID.csv")
airports_ids_dict = airport_ids.set_index('Code').to_dict()['Description']

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
        df = df[['ORIGIN_AIRPORT_ID','DEST_AIRPORT_ID','DEP_DELAY']]

        # Remove nans
        df = df.dropna()

        # Create delayed column
        df = df.assign(DELAYED=pd.Series(df['DEP_DELAY']>delay_thresh).values.astype(int))
        df = df.drop(columns="DEP_DELAY")

        # Add to airport data
        unique_ids = np.unique(np.concatenate((df['ORIGIN_AIRPORT_ID'], df['DEST_AIRPORT_ID'])))
        for id in unique_ids:

            # Create new row if it's not there
            if id not in airport_data['ID'].values:
                airport_data.loc[len(airport_data)] = [id, airports_ids_dict[id]] + [0 for _ in range(8)]

            # Increment everything

            df_from = df.loc[df['ORIGIN_AIRPORT_ID']==id]
            N_from = len(df_from)
            N_delayed_from = len(df_from.loc[df_from['DELAYED']==1])
            airport_data.loc[airport_data['ID']==id, 'N_from'] += N_from
            airport_data.loc[airport_data['ID']==id, 'N_delayed_from'] += N_delayed_from

            df_to = df.loc[df['DEST_AIRPORT_ID']==id]
            N_to = len(df_to)
            N_delayed_to = len(df_to.loc[df_to['DELAYED']==1])
            airport_data.loc[airport_data['ID']==id, 'N_to'] += N_to
            airport_data.loc[airport_data['ID']==id, 'N_delayed_to'] += N_delayed_to


            if year==2023:
                airport_data.loc[airport_data['ID']==id, 'N_from_2023'] += N_from
                airport_data.loc[airport_data['ID']==id, 'N_delayed_from_2023'] += N_delayed_from
                airport_data.loc[airport_data['ID']==id, 'N_to_2023'] += N_to
                airport_data.loc[airport_data['ID']==id, 'N_delayed_to_2023'] += N_delayed_to

        gc.collect()

# Calculate frac columns
airport_data['delay_frac_from'] = airport_data['N_delayed_from'] / airport_data['N_from']
airport_data['delay_frac_from_2023'] = airport_data['N_delayed_from_2023'] / airport_data['N_from_2023']
airport_data['delay_frac_to'] = airport_data['N_delayed_to'] / airport_data['N_to']
airport_data['delay_frac_to_2023'] = airport_data['N_delayed_to_2023'] / airport_data['N_to_2023']

airport_data = airport_data.drop(columns=['N_delayed_from','N_delayed_from_2023',
                                          'N_delayed_to','N_delayed_to_2023'])

# Sort by N_from, largest to smallest
airport_data.sort_values(by='N_from', ascending=False, inplace=True)

print(airport_data.head(20))
# print('\n')
# print(airport_data['ID'].value_counts())

filename = "airport_stats.csv"
airport_data.to_csv(filename)
