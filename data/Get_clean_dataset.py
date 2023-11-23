#!/usr/bin/env python
# coding: utf-8

####### Run this code inside the data directory #######

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import gc

'''
Airports
10397 - Atlanta, GA: Hartsfield-Jackson Atlanta International
11298 - Dallas/Fort Worth, TX: Dallas/Fort Worth International
11292 - Denver, CO: Denver International
13930 - Chicago, IL: Chicago O'Hare International
12892 - Los Angeles, CA: Los Angeles International
12478 - New York, NY: John F. Kennedy International

Carriers
WN	Southwest Airlines Co.
DL	Delta Air Lines Inc.
AA	American Airlines Inc.
OO	SkyWest Airlines Inc.
UA	United Air Lines Inc.
B6	JetBlue Airways
AS	Alaska Airlines Inc.
NK	Spirit Air Lines
9F	Frontier Airlines Inc.
'''

airports = {'10397':"ATL", '11298':"DFW", '11292':"DEN",
            '13930':"ORD", '12892':"LAX", '12478':"JFK"}

carriers = {'AA':"American", 'DL':"Delta", 'WN':"SouthWest",
            'UA':"United", 'AS':"Alaska", 'B6':"JetBlue",
            'NK':"Spirit", 'AC':"Air Canada", 'WS':"WestJet", 'Y4':"Volaris"}

Years = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]

# Keeping track of how many flights are being removed
N_tot = 0                # total
N_non_na = 0             # remove N/A columns (excluding delay reason columns)
N_not_canceled = 0       # remove canceled flights
N_slice_airports = 0     # keep only airports listed above as origin
N_slice_carriers = 0     # keep only carriers listed above
N_good_sums = 0          # Remove if |sum(delays) - total_delay| > threshold. Do this only if slice_good_sums = True

# slice_good_sums = True
slice_good_sums = False

if slice_good_sums:
    delay_sum_threshold = 10

all_data = []
for year in Years:
# for year in Years[:1]:

    print(year)
    for month in range(1,13):

        file = './{}/all_data_month{}.csv'.format(year,month)

        try:
            data = pd.read_csv(file)
        except:
            print("File not found ", file)
            continue

        N_tot += len(data)

        data = data.dropna(subset=["FL_DATE","OP_UNIQUE_CARRIER","ORIGIN_AIRPORT_ID",
                                    "DEST_AIRPORT_ID","CRS_DEP_TIME","DEP_DELAY","AIR_TIME"])
        N_non_na += len(data)

        # Remaining NaNs are converted to zero
        data = data.fillna(0)

        # Canceled
        data = data[data['CANCELLED']==0]
        N_not_canceled += len(data)
        data = data.drop(columns = ['CANCELLATION_CODE','CANCELLED'])

        # Airport
        data = data[data['ORIGIN_AIRPORT_ID'].astype(str).isin(airports.keys())]
        N_slice_airports += len(data)

        # Carrier
        data = data[data['OP_UNIQUE_CARRIER'].astype(str).isin(carriers.keys())]
        N_slice_carriers += len(data)

        # Sum delay check
        if slice_good_sums:
            sum_delay = data['CARRIER_DELAY'] + data['WEATHER_DELAY'] \
                        + data['NAS_DELAY'] + data['SECURITY_DELAY']
            dt = sum_delay - data['DEP_DELAY']
            data = data.loc[abs(dt) < delay_sum_threshold]
            N_good_sums += len(data)

            # Histogram check
            # plt.hist(dt,bins=np.linspace(-200,100,100))
            # plt.axvline(delay_sum_threshold)
            # plt.axvline(-delay_sum_threshold)
            # new_dt = dt[abs(dt) < delay_sum_threshold]
            # plt.hist(new_dt,bins=np.linspace(-200,100,100),alpha=0.5)
            # plt.show()
            # break

        # Clean up the CRS_DEP_TIME time column
        data['CRS_DEP_TIME'] = pd.to_datetime(data['CRS_DEP_TIME'].astype(int).astype(str).str.zfill(4), format='%H%M').dt.time

        # Clean up the FL_DATE column and add to it the scheduled departure time
        data['FL_DATE'] = pd.to_datetime(data.apply(lambda row: row.FL_DATE.split()[0], axis=1), format="%m/%d/%Y") + \
                            pd.to_timedelta(data["CRS_DEP_TIME"].astype(str)) - \
                            pd.to_timedelta(data['DEP_DELAY'], unit='m')

        data = data.drop(columns=['CRS_DEP_TIME'])

        # Add the frac_year column
        data['is_leap_year'] = data['FL_DATE'].dt.is_leap_year
        data["FRAC_YEAR"] = (data['FL_DATE'] - pd.to_datetime(data['FL_DATE'].dt.year, format='%Y')) \
                                / pd.to_timedelta(data['is_leap_year'].map({True: 366, False: 365}), unit='D')
        data.drop('is_leap_year', axis=1, inplace=True)


        # FRAC_DAY

        all_data.append(data)
        gc.collect()

print('\n')
print(f"Total flights read in: {N_tot:,}")
print(f"After removing bad columns: {N_non_na:,}")
print(f"After removing canceled flights: {N_not_canceled:,}")
print(f"After selecting airports: {N_slice_airports:,}")
print(f"After selecting carriers: {N_slice_carriers:,}")

if slice_good_sums:
    print(f"After removing bad delay sums: {N_good_sums:,}")

csv_data = pd.concat(all_data, ignore_index=True)
print(f"Number of flights in final dataset: {len(csv_data):,}")

filename = "clean_data"
if slice_good_sums:
    filename += "_good_sums_" + str(delay_sum_threshold)
filename += ".csv"

csv_data.to_csv(filename)