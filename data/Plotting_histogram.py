import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import gc


###### Doing analysis for each airport ####
airports = ['Atlanta', 'Chicago', 'Dallas', 'Denver', 'LA', 'JFK']
year = 2019 #### Change this ####

for airport in airports:
    ###### Loading data for airports ######
    file_name = './{}/{}_{}.csv'.format(year,airport,year)
    data_air = pd.read_csv(file_name)

    ###### Separating cancelled flights #####
    data_not_cancelled = data_air[data_air['CANCELLED']==0]
    data_cancelled = data_air[data_air['CANCELLED']== 1.0]
    data_not_cancelled = data_not_cancelled.drop(columns = ['CANCELLATION_CODE'])
    data_final = data_not_cancelled.dropna()

    ######## Plotting the distribution for Atlanta ############
    fig, axs = plt.subplots(1, 5, figsize=(20, 3))
    
    bins = 20

    dep_delay_time = data_final['DEP_DELAY'].to_numpy()
    axs[0].hist(dep_delay_time, bins=bins, log=True, edgecolor='k', color='blue')
    axs[0].set_xlabel('Minutes')
    axs[0].set_title('Total Delay')
    axs[0].set_ylabel('Count (log)')

    carrier_delay = data_final['CARRIER_DELAY'].to_numpy()
    axs[1].hist(carrier_delay, bins=bins, log=True, edgecolor='k', color='red')
    axs[1].set_xlabel('Minutes')
    axs[1].set_title('Carrier Delay')

    weather_delay = data_final['WEATHER_DELAY'].to_numpy() #### Correlate this with weather data
    axs[2].hist(weather_delay, bins=bins, log=True, edgecolor='k', color='green')
    axs[2].set_xlabel('Minutes')
    axs[2].set_title('Weather Delay')

    nas_delay = data_final['NAS_DELAY'].to_numpy()
    axs[3].hist(nas_delay, bins=bins, log=True, edgecolor='k', color='yellow')
    axs[3].set_xlabel('Minutes')
    axs[3].set_title('NAS Delay')

    sec_delay = data_final['SECURITY_DELAY'].to_numpy()
    axs[4].hist(sec_delay, bins=bins, log=True, edgecolor='k')
    axs[4].set_xlabel('Minutes')
    axs[4].set_title('Security Delay')

    plt.suptitle(airport, y=1.05, fontsize=16) 
    
    oname = '{}_delays_2020.jpg'.format(airport)
    #plt.savefig(oname, dpi=300, bbox_inches='tight')
    plt.show()
    
for airport in airports: 
    ###### Loading data for airports ######
    file_name = './{}/{}_{}.csv'.format(year,airport,year)
    data_air = pd.read_csv(file_name)
    
    ###### Separating cancelled flights #####
    data_not_cancelled = data_air[data_air['CANCELLED']==0]
    data_cancelled = data_air[data_air['CANCELLED']== 1.0]
    data_not_cancelled = data_not_cancelled.drop(columns = ['CANCELLATION_CODE'])
    data_final = data_not_cancelled.dropna()
    
    #### Normalizing by number of flights per month #####
    nflights_mon = []
    for i in range(12):
        month = data_final[data_final['Month']==i+1]
        nflights_mon.append(len(month))
        
    data_month = data_final.groupby('Month').sum()
    data_month['nflights'] = nflights_mon



    fig, axs = plt.subplots(1, 5, figsize=(20, 3))
    plt.subplots_adjust(wspace=0.3)

    axs[0].bar(data_month.index, data_month['DEP_DELAY']/data_month['nflights'], color = 'blue')
    axs[0].set_xlabel('Months')
    axs[0].set_ylabel('Minutes/flight')
    axs[0].set_title('Total Delay')


    axs[1].bar(data_month.index, data_month['CARRIER_DELAY']/data_month['nflights'], color = 'red')
    axs[1].set_xlabel('Months')
    axs[1].set_title('Carrier Delay')


    axs[2].bar(data_month.index, data_month['WEATHER_DELAY']/data_month['nflights'], color = 'green')
    axs[2].set_xlabel('Months')
    axs[2].set_title('Weather Delay')


    axs[3].bar(data_month.index, data_month['NAS_DELAY']/data_month['nflights'], color = 'yellow')
    axs[3].set_xlabel('Months')
    axs[3].set_title('NAS Delay')


    axs[4].bar(data_month.index, data_month['SECURITY_DELAY']/data_month['nflights'])
    axs[4].set_xlabel('Months')
    axs[4].set_title('Security Delay')

    plt.suptitle(airport, y=1.05, fontsize=16)

    plt.show()