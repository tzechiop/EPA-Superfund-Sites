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
fname = "TS15_split_20160729_NCB_BBL_Chitra_Event_Times.xlsx"
prcp_fname = "greenpoint.csv"
outfname = "TS15_split_20160729_NCB_BBL_Chitra_Event_TimeswPrcp.xlsx"

os.chdir(maindir)

data = pd.read_excel(fname)
prcp = pd.read_csv(prcp_fname)[['Time', 'accrain']]

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
    
# Append precipitation data to original dataset and output
data['Precipitation (in.)'] = sumprcp_list
data.to_excel(outfname,
              index = False)
        
# 
        
        
        
        
        
        
        
        
        