# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 08:43:36 2016

@author: thasegawa
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
fname = "TS15_split_20160729_NCB_BBL_Chitra_Event.xlsx"

os.chdir(maindir)

data = pd.read_excel(fname)

# Get lists for wet weather events and locations
ww_list = unique(data['Event'])
loc_list = unique([' '.join(loc.split(' ')[:-1]) for loc in data.columns.values[3:]])

# Create list for columns with quantitative data
totq_colprefix = ' TotQ(MG/15min)'
sanq_colprefix = ' SanQ(MG/15min)'
strmq_colprefix = ' StrmQ(MG/15min)'

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
        subdata = data[(data[totq_col] > 0) & (data['Event'] == ww)]
        
        # Record start and end time
        loc_list.append(loc)
        ww_list.append(ww)
        start_list.append(subdata['Time '].iloc[0])
        end_list.append(subdata['Time '].iloc[-1])
        
# Create output dataframe and export to file
outdf = pd.DataFrame({'Location':   loc_list,
                      'Event':      ww_list,
                      'Start Time': start_list,
                      'End Time':   end_list})[['Location', 'Event', 'Start Time', 'End Time']]
outdf.to_excel("TS15_split_20160729_NCB_BBL_Chitra_Event_Times.xlsx",
               index = False)

