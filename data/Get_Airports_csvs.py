#!/usr/bin/env python
# coding: utf-8

####### Run this code inside the data directory #######

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gc

airport_ids = [10397, 11298, 11292, 13930, 12892, 12478]
airports = ['Atlanta', 'Dallas', 'Denver', 'Chicago','LA', 'JFK']
'''
10397 - Atlanta, GA: Hartsfield-Jackson Atlanta International
11298 - Dallas/Fort Worth, TX: Dallas/Fort Worth International
11292 - Denver, CO: Denver International
13930 - Chicago, IL: Chicago O'Hare International
12892 - Los Angeles, CA: Los Angeles International
12478 - New York, NY: John F. Kennedy International
'''

def get_airport_csvs(year):
    Air_dfs = []
    for j in range(len(airports)):
        #print(airport_ids[j])
        for i in range(12):
            csv_file = './{}/all_data_month{}.csv'.format(year,i+1)
            data = pd.read_csv(csv_file)
            data = data[data['ORIGIN_AIRPORT_ID']== airport_ids[j]]
            data['Month'] = i+1
            Air_dfs.append(data)
            gc.collect()

        Air = pd.concat(Air_dfs, ignore_index=True)
        savefile = './{}/{}.csv'.format(year,airports[j])
        print(savefile)
        Air.to_csv(savefile)

#get_airport_csvs(2020)

for year in range(2012,2023):
    get_airport_csvs(year)
