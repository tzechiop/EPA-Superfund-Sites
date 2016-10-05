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

# Initialize dictionary for StrmQ %
strmq_perc = {}

# Create lists for symbols
c_list = ['b', 'r', 'g', 'c', 'm', 'k', 'brown', 'coral', 'dimgray', 'b', 'r', 'g', 'c', 'm', 'k', 'brown', 'coral']
m_list = ['-', '-', '-', '-', '-', '-', '-', '-', '-', '--', '--', '--', '--', '--', '--', '--', '--']

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

# Loop through locations and calculate StrmQ % for each WW event
for loc in ww_dict:
    totq_col = loc + totq_colprefix
    strmq_col = loc + strmq_colprefix
    
    strmq_perc[loc] = []
    data['Strmq_Percent'] = data.apply(lambda x: calcStrmqPercent(x[totq_col],x[strmq_col]), axis = 1)
    
    # Plot Strmq_Percent for each WW event
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ww_list = ww_dict[loc]
    for index, ww in enumerate(ww_list): 
        dataindex = data['Event'] == ww  
        subdata = data[dataindex]
        
        # Remove initial 0 values
        zeroindex = [True]*len(subdata.index)
        trigger = True
        for metaindex, totq in enumerate(subdata[totq_col]):
            if (totq == 0) and (trigger == True):
                zeroindex[metaindex] = False
            else:
                trigger = False
        
        # Remove last 0 values
        trigger = True
        for metaindex, totq in enumerate(reversed(list(subdata[totq_col]))):
            if (totq == 0) and (trigger == True):
                zeroindex[-(metaindex+1)] = False
            else:
                trigger = False  
  
        subdata = subdata[zeroindex]
        
        if len(subdata.index) > 0:
            # Calculate time after start of CSO event
            starttime = subdata['Time (days)'].iloc[0]
            subdata['Time After Start'] = subdata['Time (days)'].apply(lambda x: (x - starttime)*24)
            
            # Plot data
            mask = np.isfinite(list(subdata['Strmq_Percent']))        
            wwindex = int(ww.split('-')[1])-1
            ax1.plot(subdata['Time After Start'].loc[mask],
                     subdata['Strmq_Percent'].loc[mask],
                     label = ww,
                     linestyle = m_list[wwindex],
                     color = c_list[wwindex],
                     marker = 'o',
                     markersize = 2)
    # Add legend
    lgd = plt.legend(bbox_to_anchor=(1.02, 1),
                     loc=2,
                     borderaxespad=0.,
                     prop={'size':9},
                     handlelength = 3)
        
    # Create axis labels and plot title
    title = 'Stormwater Percents by Time for {0} (Data from HDR Model)'.format(loc)
    ax1.set_title(title, y = 1.03)       
    ax1.set_ylabel('Stormwater Pecent (%)')
    ax1.set_xlabel('Hours after start of WW event')
    
    # Set y-tick and x-tick labels
    ymin, ymax = ax1.get_ylim()
    #yticks = np.arange(ymin, ymax+0.0001, 0.05)
    yticks = np.arange(0, 1.01, 0.1)
    yticklabels = ['{0:.0f}%'.format(perc*100) for perc in yticks]
    plt.yticks(yticks, yticklabels)
    
    # Output figure to file
    outfigname = 'TS15_split_20160729_StrmqPercentVsTime_{0}.pdf'.format(loc)
    fig1.savefig(os.path.join(outdir, outfigname), bbox_inches='tight')
    
#==============================================================================
#     # Reduce x axis and output figure again
#     ax1.set_xlim(0, 4)
#     outfigname = 'TS15_split_20160729_StrmqPercentVsTime_{0}_small.pdf'.format(loc)
#     fig1.savefig(os.path.join(outdir, outfigname), bbox_inches='tight')
#     plt.clf()
#==============================================================================

