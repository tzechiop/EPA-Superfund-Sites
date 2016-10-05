# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 08:43:36 2016

@author: thasegawa
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from collections import OrderedDict

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
    
# Function that the data is fit to
def func(x, a, b, c):
    return a * np.exp(-b * x) + c

# Read data
maindir = r"C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek"
outdir = r"C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek\HDR CSO Flow Model - Precipitation Correlation\Hourly"
fname = "TS15_split_20160729_NCB_BBL_Chitra_Event_Summary_Hourly.xlsx"

os.chdir(maindir)

data = pd.read_excel(fname)

colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'coral', 'brown', 'gray']
loc_list = ['BB-009',
            'BB-026',
            'NC-002',
            'NC-015',
            'NC-022',
            'NC-029',
            'NC-077',
            'NC-083']
ww_list = ['WW-1',
           'WW-2',
           'WW-3',
           'WW-4',
           'WW-5',
           'WW-6',
           'WW-7',
           'WW-8',
           'WW-9',
           'WW-10',
           'WW-11',
           'WW-12',
           'WW-13',
           'WW-14',
           'WW-15',
           'WW-16',
           'WW-17']

# Columns
prcpcol = 'Precip (in.)'
strmq_perc_col = 'StrmQ Percent'

# Filter data for WW events with precipitation and strmq percent values
data = data[(data[prcpcol].notnull()) & (data[strmq_perc_col])]

# ============================= Plot By Location =============================
# Plot Scatter Plot By Location
for loc in loc_list:
    subdata = data[data['Location'] == loc]
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)    
    # Plot points for each ww event while calculate R^2 values
    r_dict = OrderedDict()
    r_dict['All Events'] = pearsonr(subdata[prcpcol], subdata[strmq_perc_col])[1]
    for index, ww in enumerate(subdata['Event'].unique()):
        plotdata = subdata[subdata['Event'] == ww]
        ax1.scatter(plotdata[prcpcol],
                    plotdata[strmq_perc_col],
                    c = colors[index],
                    lw = 0,
                    s = 10,
                    label = ww)
        r_dict[ww] = pearsonr(plotdata[prcpcol], plotdata[strmq_perc_col])[1]
    
    # Create Legend
    plt.legend(bbox_to_anchor=(1.02, 1),
               loc=2,
               borderaxespad=0.,
               prop={'size':9},
               scatterpoints = 3)
                     
    # Create axis labels and plot title
    title = 'Stormwater Percentages by Precipitation (HDR CSO Model)'
    ax1.set_title(title)       
    ax1.set_ylabel('Stormwater Pecent (%)')
    ax1.set_xlabel('Precipitation (in.)')
    
    # Set y-tick and x-tick labels
    xmin, xmax = ax1.get_xlim()
    ax1.set_xlim(-0.5/20, 0.5)
    ax1.set_ylim(0,1.05)
    yticks = np.arange(0, 1.01, 0.1)
    yticklabels = ['{0:.0f}%'.format(perc*100) for perc in yticks]
    plt.yticks(yticks, yticklabels)

    # Add text for R^2    
    text = ''
    for event, r in r_dict.items():
        text +='R^2 ({0}) = {1:.3f}\n'.format(event, r)
    plt.text(0.55*0.5, 0.5, text)
    plt.show()
    
    # Output figure to file
    outfigname = "StormwaterPercentByPrecipitation_{0}_Hourly.pdf".format(loc)
    fig1.savefig(os.path.join(outdir, outfigname), bbox_inches='tight')
    plt.clf()