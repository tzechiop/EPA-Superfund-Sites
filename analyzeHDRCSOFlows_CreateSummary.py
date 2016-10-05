# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 08:43:36 2016

@author: thasegawa
"""

import os
import pandas as pd
from datetime import datetime
import numpy as np

# Gets unique values in a list without sorting
def unique(l):
    o = []
    for x in l:
        if x not in o:
            o.append(x)
    return o

# Calculate Stormwater Percent with Total Q and Stormwater Q    
def calcStrmqPercent(totq, strmq):
    if (totq > 0) and (strmq > 0):
        strmq_perc = strmq/totq
    elif  (strmq > 0):
        print('Error!! Strmq > 0, but totq == 0 for {0} at {1}'.format(ww, loc))
    else:
        strmq_perc = np.nan
    return strmq_perc
    
# Calculate the delta time from the start time, in hours rounded to 15 minutes
def calcDiffTime(time, starttime):
    delta = (time - starttime)*24
    delta = round(delta*4)/4
    return delta

# Read data
maindir = r"C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek"
outdir = r"C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek\HDR CSO Flow Model"
#fname = "TS15_split_20160729_NCB_BBL_Chitra_Event_Times.xlsx"
fullfname = "TS15_split_20160729_NCB_BBL_Chitra_Event.xlsx"
prcp_fname = "greenpoint.csv"
outfname = "TS15_split_20160729_NCB_BBL_Chitra_Event_Summary.xlsx"

os.chdir(maindir)

#data = pd.read_excel(fname)
fulldata = pd.read_excel(fullfname)
prcp = pd.read_csv(prcp_fname)[['Time', 'accrain']]

# Create list for columns with quantitative data
totq_colprefix = ' TotQ(MG/15min)'
sanq_colprefix = ' SanQ(MG/15min)'
strmq_colprefix = ' StrmQ(MG/15min)'

# Dictionary for WW events and locations
ww_dict = {'NC-015': ['WW-1',
                      'WW-4',
                      'WW-7',
                      'WW-8',
                      'WW-10',
                      'WW-15'],
           'NC-022': ['WW-4',
                      'WW-7'],
           'NC-029': ['WW-9',
                      'WW-14',
                      'WW-16'],
           'NC-077': ['WW-3',
                      'WW-4',
                      'WW-5',
                      'WW-8',
                      'WW-12',
                      'WW-15'],
           'NC-083': ['WW-8',
                      'WW-10',
                      'WW-12',
                      'WW-14'],
           'BB-026': ['WW-1',
                      'WW-4',
                      'WW-7',
                      'WW-8',
                      'WW-9',
                      'WW-10'],
           'BB-009': ['WW-9',
                      'WW-15',
                      'WW-17'],
           'NC-002': ['WW-2',
                      'WW-4',
                      'WW-12',
                      'WW-13'],
           'WWTP-BQ only': ['WW-2',
                            'WW-3',
                            'WW-4',
                            'WW-5',
                            'WW-7',
                            'WW-8',
                            'WW-10',
                            'WW-12',
                            'WW-15']}

# Loop through data and get WW events for each location
loc_list = []
ww_list = []
start_list = []
end_list = []
for loc in ww_dict:
    totq_col = loc + totq_colprefix
    for ww in ww_dict[loc]:
        subdata = fulldata[(fulldata[totq_col] > 0) & (fulldata['Event'] == ww)]
        
        # Record start and end time
        loc_list.append(loc)
        ww_list.append(ww)
        start_list.append(subdata['Time '].iloc[0])
        end_list.append(subdata['Time '].iloc[-1])
        
# Create dataframe
data = pd.DataFrame({'Location':   loc_list,
                     'Event':      ww_list,
                     'Start Time': start_list,
                     'End Time':   end_list})[['Location', 'Event', 'Start Time', 'End Time']]
                            
# Convert precipitation dataset times to datetime and retrieve prcp time range
prcp['Time'] = prcp['Time'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
prcpstart = prcp['Time'].iloc[0]
prcpend = prcp['Time'].iloc[-1]

# Loop through WW events and calculate precipitation
sumprcp_list = []
for loc, event, start, end in zip(data['Location'], data['Event'], data['Start Time'], data['End Time']):
    # Only calculate precipitation if WW start and end times are included in the prcp time range
    if (start >= prcpstart) and (end <= prcpend):
        index = (prcp['Time'] >= start) & (prcp['Time'] <= end)
        sumprcp = prcp['accrain'].loc[index].iloc[:-1].sum()
        
        # Calculate residual precipitation at start of time period assuming constant rain
        prcptime1 = prcp['Time'].loc[prcp['Time'] <= start].iloc[-1]
        prcptime2 = prcp['Time'].loc[prcp['Time'] >= start].iloc[0]
        prcpinterval = prcp['accrain'].loc[prcp['Time'] <= start].iloc[-1]
        interval = (prcptime2 - prcptime1).seconds
        delta = (prcptime2 - start).seconds        
        if interval > 0:
            sumprcp += prcpinterval/interval*delta        
        
        # Calculate residual precipitation at end of time period assuming constant rain        
        prcptime1 = prcp['Time'].loc[prcp['Time'] <= end].iloc[-1]
        prcptime2 = prcp['Time'].loc[prcp['Time'] >= end].iloc[0]
        prcpinterval = prcp['accrain'].loc[prcp['Time'] <= start].iloc[-1]
        interval = (prcptime2 - prcptime1).seconds
        delta = (end - prcptime1).seconds        
        if interval > 0:
            sumprcp += prcpinterval/interval*delta        
    else:
        sumprcp = np.nan
    sumprcp_list.append(sumprcp)

# Loop through locations and calculate StrmQ % for each WW event
strmq_perc_list = []
for loc, event in zip(data['Location'], data['Event']):
    totq_col = loc + totq_colprefix
    strmq_col = loc + strmq_colprefix
    
    index = fulldata['Event'] == event
    totq = fulldata[totq_col].loc[index].sum()
    strmq = fulldata[strmq_col].loc[index].sum()
    
    if (totq > 0) and (strmq > 0):
        strmq_perc_list.append(strmq/totq)
    elif  (strmq > 0):
        print('Error!! Strmq > 0, but totq == 0 for {0} at {1}'.format(event, loc))
    else:
        strmq_perc_list[loc].append(np.nan)
    
# Append precipitation data and StormQ data to original dataset and output
data['Precipitation (in.)'] = sumprcp_list
data['StrmQ Percent'] = strmq_perc_list
data.to_excel(outfname,
              index = False)
        
        
        
        
        
        
        
        
        