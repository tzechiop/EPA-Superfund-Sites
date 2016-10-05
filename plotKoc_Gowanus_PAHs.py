# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 11:11:50 2016

@author: thasegawa
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

# Stagger x indices
def staggerX(x, stagger = 0.02, tol = 0.5):
    newx = np.random.normal(x, stagger, size = 1)[0]
    if abs(x - newx) >= tol:
        newx = x
    return newx
    
# =============================================================================

datadir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Gowanus Canal\Koc'
os.chdir(datadir)

# Read data
data = pd.read_excel('KocCalculations.xlsx',
                     sheetname = 'PAHs')

# Remove Dry Weather
data = data[data['DryWet'] == 'Wet']
                     
PAH_list = ['2-METHYLNAPHTHALENE', 'ACENAPHTHENE',
       'ACENAPHTHYLENE', 'ANTHRACENE', 'Benz[a]anthracene',
       'Benzo[a]pyrene', 'Benzo[b]fluoranthene', 'Benzo[ghi]perylene',
       'Benzo[j,k]fluoranthenes', 'CHRYSENE', 'Dibenz[a,h]anthracene',
       'FLUORANTHENE', 'FLUORENE', 'Indeno[1,2,3-cd]pyrene', 'NAPHTHALENE',
       'PHENANTHRENE', 'PYRENE']

cmap = {'CSO': 'r',
        'WWTP': 'b'}
        
mmap = {'CSO': 'o',
        'WWTP': 's'}
        
lmap = {'Gowanus Canal': 0,
        'Newtown Creek': 1}       
        
location_list = ['Gowanus Canal',
                 'Newtown Creek']

for index, PAH in enumerate(PAH_list):
    # Grab logKow and lowKoc data and merge to create plot data
    logKow = data.loc[data['Type'] == 'Log Kow', ['Data', 'LocEvent', 'LocType', PAH]]
    logKoc = data.loc[data['Type'] == 'Log Koc', ['LocEvent', PAH]]
    subdata = pd.merge(logKow, logKoc, on = 'LocEvent')
    
    subdata = subdata.rename(columns = {PAH + '_x': 'Log Kow',
                                        PAH + '_y': 'Log Koc'})
    subdata = subdata[subdata['Log Koc'].notnull()]
                                          
    subdata['Color'] = subdata['Data'].map(cmap)                                          
    subdata['x'] = subdata['Data'].map(lmap)   
    subdata['x'] = subdata['x'].map(staggerX)

#    for loctype in subdata['LocType'].unique():
#        marker = mmap[loctype]
#        idx = (subdata['LocType'] == loctype)
#        plotdata = subdata[idx]
#        plt.scatter(plotdata['x'],
#                    plotdata['Log Koc'],
#                    c = plotdata['Color'],  
#                    marker = marker,
#                    s = 50,
#                    label = loctype)

    for loctype in subdata['LocType'].unique():
        color = cmap[loctype]
        idx = (subdata['LocType'] == loctype)
        plotdata = subdata[idx]
        plt.scatter(plotdata['x'],
                    plotdata['Log Koc'],
                    c = color,  
                    s = 50,
                    label = loctype)
                    
    lgd = plt.legend(bbox_to_anchor=(1.02, 1),
                     loc=2,
                     borderaxespad=0.)
                     
    # Set Xtick labels, ylabel and plot title
    ax = plt.gca()  
    plt.xticks(range(len(location_list)), location_list, rotation = 90)
    title = 'Log Koc Comparison ({0})'.format(PAH)
    ax.set_title(title)       
    ax.set_ylabel('Log Koc')
                        
    outname = 'PAH_KocComparison_{0}.pdf'.format(PAH)
    fig = ax.get_figure();
    fig.suptitle('')
    fig.savefig(outname, bbox_inches='tight')
    
    plt.clf()


    