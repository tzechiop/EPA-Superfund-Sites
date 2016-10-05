# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 08:43:36 2016

@author: thasegawa
"""

import os
import pandas as pd
import numpy as np
from collections import OrderedDict
import matplotlib.pyplot as plt

# Gets unique values in a list without sorting
def unique(l):
    o = []
    for x in l:
        if x not in o:
            o.append(x)
    return o

# Read data
maindir = r"C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek"
fname = "TS15_split_20160729_NCB_BBL_Chitra_Event.xlsx"
outfname = "TS15_split_20160729_StrmqPercent.xlsx"
outfigname = "TS15_split_20160729_StrmqPercent.pdf"

os.chdir(maindir)

data = pd.read_excel(fname)

# Get lists for wet weather events and locations
ww_list = unique(data['Event'])
loc_list = unique([' '.join(loc.split(' ')[:-1]) for loc in data.columns.values[3:]])

# Create list for columns with quantitative data
totq_colprefix = ' TotQ(MG/15min)'
sanq_colprefix = ' SanQ(MG/15min)'
strmq_colprefix = ' StrmQ(MG/15min)'

# Initialize dictionary for StrmQ %
strmq_perc = {}

# Loop through locations and calculate StrmQ % for each WW event
for loc in loc_list:
    totq_col = loc + totq_colprefix
    strmq_col = loc + strmq_colprefix
    
    strmq_perc[loc] = []
    for ww in ww_list:        
        index = data['Event'] == ww
        totq = data[totq_col].loc[index].sum()
        strmq = data[strmq_col].loc[index].sum()
        
        if (totq > 0) and (strmq > 0):
            strmq_perc[loc].append(strmq/totq)
        elif  (strmq > 0):
            print('Error!! Strmq > 0, but totq == 0 for {0} at {1}'.format(ww, loc))
        else:
            strmq_perc[loc].append(np.nan)

outdf = pd.DataFrame(strmq_perc,
                     index = ww_list)
outdf = outdf[loc_list]
outdf.to_excel(outfname)

# ================================= Plotting =================================
# Create lists for symbosl
c_list = ['b', 'r', 'g', 'c', 'm', 'k', 'b', 'r', 'g', 'c', 'm', 'k']
m_list = ['-', '-', '-', '-', '-', '-', '--', '--', '--', '--', '--', '--']

# Create Line plot
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
xval = np.arange(len(ww_list))
for index, loc in enumerate(loc_list):
    mask = np.isfinite(list(outdf[loc]))
    ax1.plot(xval[mask], outdf[loc].loc[mask], label = loc, linestyle = m_list[index], color = c_list[index])

# Create Legend
lgd = plt.legend(bbox_to_anchor=(1.02, 1),
                 loc=2,
                 borderaxespad=0.,
                 prop={'size':9},
                 handlelength = 3)
                 
# Create axis labels and plot title
title = 'Stormwater Percents for HDR Model'
ax1.set_title(title)       
ax1.set_ylabel('Stormwater Pecent (%)')
ax1.set_xlabel('')

# Set y-tick and x-tick labels
plt.xticks(np.arange(len(ww_list)), ww_list, rotation = 'vertical')
ax1.set_ylim(0.2,1)
ax1.set_yticklabels(['{0:.0f}%'.format(perc) for perc in np.arange(20,101,10)])

# Output figure to file
fig1.savefig(outfigname, bbox_inches='tight')
plt.clf()