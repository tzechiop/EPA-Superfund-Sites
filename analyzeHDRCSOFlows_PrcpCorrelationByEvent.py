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
outdir = r"C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek\HDR CSO Flow Model - Precipitation Correlation"
fname = "TS15_split_20160729_NCB_BBL_Chitra_Event_Summary.xlsx"

os.chdir(maindir)

data = pd.read_excel(fname)

colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'coral', 'brown', 'gray']
ww_markers = ['o', 'v', '^', '8', 's', 'p', '+', 'D', '3', '4']

c_dict = {loc: loc_colors[index] for index, loc in enumerate(data['Location'].unique())}
m_dict = {ww: ww_markers[index] for index, ww in enumerate(data['Event'].unique())}

# Filter data for WW events with precipitation values
data = data[data['Precipitation (in.)'].notnull()]

# ============================= Plot By Location =============================
# Plot Scatter Plot By Location
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
for index, loc in enumerate(data['Location'].unique()):
    plotdata = data[data['Location'] == loc]
    ax1.scatter(plotdata['Precipitation (in.)'],
                plotdata['StrmQ Percent'],
                c = colors[index],
                lw = 0,
                s = 40,
                label = loc)

# Create Legend
lgd = plt.legend(bbox_to_anchor=(1.02, 1),
                 loc=2,
                 borderaxespad=0.,
                 prop={'size':9},
                 handlelength = 3)
                 
# Create axis labels and plot title
title = 'Stormwater Percentages by Precipitation (HDR CSO Model)'
ax1.set_title(title)       
ax1.set_ylabel('Stormwater Pecent (%)')
ax1.set_xlabel('Precipitation (in.)')

# Set y-tick and x-tick labels
xmin, xmax = ax1.get_xlim()
ax1.set_xlim(-0.15, xmax)
ax1.set_ylim(0,1.05)
yticks = np.arange(0, 1.01, 0.1)
yticklabels = ['{0:.0f}%'.format(perc*100) for perc in yticks]
plt.yticks(yticks, yticklabels)
plt.show()

# Output figure to file
outfigname = "StormwaterPercentByPrecipitation_Locations.pdf"
fig1.savefig(os.path.join(outdir, outfigname), bbox_inches='tight')
plt.clf()


# ============================= Plot By Event =============================
# Plot Scatter Plot By Location
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
for index, loc in enumerate(data['Event'].unique()):
    plotdata = data[data['Event'] == loc]
    ax1.scatter(plotdata['Precipitation (in.)'],
                plotdata['StrmQ Percent'],
                c = colors[index],
                lw = 0,
                s = 40,
                label = loc)

# Create Legend
lgd = plt.legend(bbox_to_anchor=(1.02, 1),
                 loc=2,
                 borderaxespad=0.,
                 prop={'size':9},
                 handlelength = 3)
                 
# Create axis labels and plot title
title = 'Stormwater Percentages by Precipitation (HDR CSO Model)'
ax1.set_title(title)       
ax1.set_ylabel('Stormwater Pecent (%)')
ax1.set_xlabel('Precipitation (in.)')

# Set y-tick and x-tick labels
xmin, xmax = ax1.get_xlim()
ax1.set_xlim(-0.15, xmax)
ax1.set_ylim(0,1.05)
yticks = np.arange(0, 1.01, 0.1)
yticklabels = ['{0:.0f}%'.format(perc*100) for perc in yticks]
plt.yticks(yticks, yticklabels)
plt.show()

# Output figure to file
outfigname = "StormwaterPercentByPrecipitation_Events.pdf"
fig1.savefig(os.path.join(outdir, outfigname), bbox_inches='tight')
plt.clf()




