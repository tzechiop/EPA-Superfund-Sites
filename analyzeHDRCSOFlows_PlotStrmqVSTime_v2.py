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

# Initialize dictionary for StrmQ %
strmq_perc = {}

# Create lists for symbols
c_list = ['b', 'r', 'g', 'c', 'm', 'k', 'brown', 'coral', 'dimgray', 'b', 'r', 'g', 'c', 'm', 'k', 'brown', 'coral']
m_list = ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', '^', '^', '^', '^', '^', '^', '^', '^']

# Loop through locations and calculate StrmQ % for each WW event
for loc in ww_dict:
    totq_col = loc + totq_colprefix
    strmq_col = loc + strmq_colprefix

    # Remove values where TotQ == 0    
    subdata = data[data[totq_col] > 0]
    
    # Calculate StrmQ percent for every row
    subdata['Strmq_Percent'] = data.apply(lambda x: calcStrmqPercent(x[totq_col],x[strmq_col]), axis = 1)    

    # Loop through WW events to create list of dataframes    
    wwdf_list = []
    for ww in ww_list:
        wwdata = subdata[subdata['Event'] == ww]
        
        # Calculate time after start of WW event (in hours)
        if len(wwdata.index) > 0:
            starttime = wwdata['Time (days)'].iloc[0]
            wwdata['Time after start'] = wwdata['Time (days)'].apply(lambda x: calcDiffTime(x, starttime))
            
            wwdf_list.append(pd.DataFrame({ww: list(wwdata['Strmq_Percent'])},
                                          index = list(wwdata['Time after start'])))
    
    # Combine data for all WW events
    wwdf = pd.concat(wwdf_list, axis = 1, join = 'outer')
    
    # ====================== Scatter plot ======================
    # Plot Strmq percentages of WW event
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    for ww in ww_dict[loc]:
        if ww in wwdf.columns.values:
            wwindex = int(ww.split('-')[1])-1
            plotdata = wwdf[ww]
            ax1.scatter(plotdata.index,
                        plotdata,
                        c = c_list[wwindex],
                        marker = m_list[wwindex],
                        s = 10,
                        lw = 0,
                        label = ww)
    
    # Create Legend
    lgd = plt.legend(bbox_to_anchor=(1.02, 1),
                     loc=2,
                     borderaxespad=0.,
                     prop={'size':9},
                     scatterpoints = 1)
                     
    # Create axis labels and plot title
    title = 'Stormwater Percents by Time for {0} (Data from HDR Model)'.format(loc)
    ax1.set_title(title, y = 1.03)       
    ax1.set_ylabel('Stormwater Pecent (%)')
    ax1.set_xlabel('Time after start of WW event (hours)')
    
    # Set y-tick and x-tick labels
    ymin, ymax = ax1.get_ylim()
    #yticks = np.arange(ymin, ymax+0.0001, 0.05)
    yticks = np.arange(0, 1.01, 0.1)
    yticklabels = ['{0:.0f}%'.format(perc*100) for perc in yticks]
    plt.yticks(yticks, yticklabels)
    
    xmin, xmax = ax1.get_xlim()
    xmax = np.ceil(wwdf.index[-1]/2)*2
    xticks = np.arange(0, xmax+0.51, 2)
    ax1.set_xlim(-0.5, xmax)
    plt.xticks(xticks, xticks)

    
    # Output figure to file
    outfigname = 'TS15_split_20160729_StrmqPercentVsTime_{0}_scatter.pdf'.format(loc)
    fig1.savefig(os.path.join(outdir, outfigname), bbox_inches='tight')
    plt.clf()
        
    # ====================== Boxplot ======================
    # Create boxplot for every time delta
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    wwdf_t = wwdf.transpose()
    bp = wwdf_t.boxplot(ax = ax1,
                        widths=0.10,
                        positions = wwdf_t.columns.values)

    # change outline width
    for box in bp['boxes']:
        box.set(linewidth=0.75)
    
    ## change linewidth of the whiskers
    for whisker in bp['whiskers']:
        whisker.set(color = 'b', linewidth=0.75)
    
    ## change linewidth of the caps
    for cap in bp['caps']:
        cap.set(linewidth=0.75)
        
    ## change linewidth of the medians
    for median in bp['medians']:
        median.set(linewidth=0.75)
        
    # Create axis labels and plot title
    title = 'Stormwater Percents by Time for {0} (Data from HDR Model)'.format(loc)
    ax1.set_title(title, y = 1.03)       
    ax1.set_ylabel('Stormwater Pecent (%)')
    ax1.set_xlabel('Time after start of WW event (hours)')
    
    # Set y-tick and x-tick labels
    #ymin, ymax = ax1.get_ylim()
    #yticks = np.arange(ymin, ymax+0.0001, 0.05)
    yticks = np.arange(0, 1.01, 0.1)
    yticklabels = ['{0:.0f}%'.format(perc*100) for perc in yticks]
    plt.yticks(yticks, yticklabels)
    
    xticks = np.arange(0, xmax+0.51, np.ceil(xmax/20)*2)
    ax1.set_xlim(-0.5, xmax)
    plt.xticks(xticks, xticks)

    # Output figure to file
    outfigname = 'TS15_split_20160729_StrmqPercentVsTime_{0}_boxplot.pdf'.format(loc)
    fig1.savefig(os.path.join(outdir, outfigname), bbox_inches='tight')
    plt.clf()
