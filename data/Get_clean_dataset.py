#!/usr/bin/env python
# coding: utf-8

####### Run this code inside the data directory #######

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import gc

'''
Top Airports
10397	Atlanta, GA: Hartsfield-Jackson Atlanta International
13930	Chicago, IL: Chicago O'Hare International
11298	Dallas/Fort Worth, TX: Dallas/Fort Worth International
11292	Denver, CO: Denver International
12892	Los Angeles, CA: Los Angeles International
14107	Phoenix, AZ: Phoenix Sky Harbor International
14771	San Francisco, CA: San Francisco International
11057	Charlotte, NC: Charlotte Douglas International
12266	Houston, TX: George Bush Intercontinental/Houston
12889	Las Vegas, NV: Harry Reid International
14747	Seattle, WA: Seattle/Tacoma International
13487	Minneapolis, MN: Minneapolis-St Paul International
11433	Detroit, MI: Detroit Metro Wayne County
13204	Orlando, FL: Orlando International
10721	Boston, MA: Logan International
12953	New York, NY: LaGuardia
11618	Newark, NJ: Newark Liberty International
12478	New York, NY: John F. Kennedy International
14869	Salt Lake City, UT: Salt Lake City International
11278	Washington, DC: Ronald Reagan Washington National

Top Carriers
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

airports = [10397,13930,11298,11292,12892,14107,14771,11057,12266,12889,14747,13487,11433,13204,10721,12953,11618,12478,14869,11278]
airports = [str(a) for a in airports]
carriers = ["WN","DL","AA","OO","UA","B6","AS","NK","9F"]

Years = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]

# Keeping track of how many flights are being removed
N_tot = 0                # total
N_not_canceled = 0       # remove canceled flights
N_non_na = 0             # remove N/A columns (excluding delay reason columns)
N_slice_orig_airports = 0     # keep only airports listed above as origin
N_slice_dest_airports = 0     # keep only airports listed above as destination
N_slice_carriers = 0     # keep only carriers listed above

all_data = []
for year in Years:

    print(year)
    for month in range(1,13):

        file = './{}/all_data_month{}.csv'.format(year,month)

        try:
            df = pd.read_csv(file)
        except:
            print("File not found ", file)
            continue

        N_tot += len(df)

        # Canceled
        df = df[df['CANCELLED']==0]
        N_not_canceled += len(df)
        df = df.drop(columns = ['CANCELLATION_CODE','CANCELLED'])

        # NaNs
        df = df.dropna(subset=["FL_DATE","OP_UNIQUE_CARRIER","ORIGIN_AIRPORT_ID",
                                    "DEST_AIRPORT_ID","CRS_DEP_TIME","DEP_DELAY","AIR_TIME"])
        N_non_na += len(df)

        # Remaining NaNs are converted to zero
        df = df.fillna(0)

        # Airport
        df = df[df['ORIGIN_AIRPORT_ID'].astype(str).isin(airports)]
        N_slice_orig_airports += len(df)
        
        df = df[df['DEST_AIRPORT_ID'].astype(str).isin(airports)]
        N_slice_dest_airports += len(df)

        # Carrier
        df = df[df['OP_UNIQUE_CARRIER'].astype(str).isin(carriers)]
        N_slice_carriers += len(df)

        # Clean up the CRS_DEP_TIME time column
        df['CRS_DEP_TIME'] = pd.to_datetime(df['CRS_DEP_TIME'].astype(int).astype(str).str.zfill(4), format='%H%M').dt.time

        # Clean up the FL_DATE column and add to it the scheduled departure time
        df['FL_DATE'] = pd.to_datetime(df.apply(lambda row: row.FL_DATE.split()[0], axis=1), format="%m/%d/%Y") + \
                            pd.to_timedelta(df["CRS_DEP_TIME"].astype(str)) - \
                            pd.to_timedelta(df['DEP_DELAY'], unit='m')

        df = df.drop(columns=['CRS_DEP_TIME'])

        # Add the frac_year and frac_day columns
        df['is_leap_year'] = df['FL_DATE'].dt.is_leap_year
        df["FRAC_YEAR"] = (df['FL_DATE'] - pd.to_datetime(df['FL_DATE'].dt.year, format='%Y')) \
                                / pd.to_timedelta(df['is_leap_year'].map({True: 366, False: 365}), unit='D')
        df.drop('is_leap_year', axis=1, inplace=True)

        df['FRAC_DAY'] = (df['FL_DATE'] - df['FL_DATE'].dt.floor('D')) / pd.to_timedelta('1D')

        all_data.append(df)
        gc.collect()

print('\n')
print(f"Total flights read in: {N_tot:,}")
print(f"After removing canceled flights: {N_not_canceled:,}")
print(f"After removing bad columns: {N_non_na:,}")
print(f"After selecting origin airports: {N_slice_orig_airports:,}")
print(f"After selecting destination airports: {N_slice_dest_airports:,}")
print(f"After selecting carriers: {N_slice_carriers:,}")

csv_data = pd.concat(all_data, ignore_index=True)
print(f"Number of flights in final dataset: {len(csv_data):,}")

filename = "clean_data.csv"
csv_data.to_csv(filename)