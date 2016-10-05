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
    
# Estimate Log Koc
def estLogKoc(logKow):
    logKoc = 0.98 * logKow - 0.32
    return logKoc
    
# =============================================================================

datadir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Gowanus Canal\Koc'
os.chdir(datadir)

# Read data
rawdata = pd.read_excel('KocCalculations.xlsx',
                        sheetname = 'PAHs')

# Remove Dry Weather
rawdata = rawdata[rawdata['DryWet'] == 'Wet']
                     
PAH_list = ['2-METHYLNAPHTHALENE', 'ACENAPHTHENE',
       'ACENAPHTHYLENE', 'ANTHRACENE', 'Benz[a]anthracene',
       'Benzo[a]pyrene', 'Benzo[b]fluoranthene', 'Benzo[ghi]perylene',
       'Benzo[j,k]fluoranthenes', 'CHRYSENE', 'Dibenz[a,h]anthracene',
       'FLUORANTHENE', 'FLUORENE', 'Indeno[1,2,3-cd]pyrene', 'NAPHTHALENE',
       'PHENANTHRENE', 'PYRENE']
       
label_list = ['Gowanus Canal',
              'Newtown Creek',
              'Estimated Koc']
            
c_list = ['r', 'b', 'g', 'y', 'c', 'm', 'k']
       
kow = rawdata.loc[rawdata['Type'] == 'Log Kow'][PAH_list]
#koc = rawdata.loc[rawdata['Type'] != 'Log Kow'].groupby(['Data', 'LocType']).mean()[PAH_list]
koc = rawdata.loc[rawdata['Type'] != 'Log Kow'][PAH_list]

kow = kow.transpose()
kow.columns = ['Log Kow']
koc = koc.transpose()

data = pd.concat([kow, koc], axis = 1)

# Estimate Log Koc from literature Log Kow values
data['Estimated Koc'] = data['Log Kow'].apply(estLogKoc)

label_list = list(data.columns.values)
label_list.remove('Log Kow')

# Plot data
for index, label in enumerate(label_list):
    if type(label) == type((1,2)):
        label_clean = label[0] + " " + label[1]
    else:
        label_clean = label
    plt.scatter(data['Log Kow'],
                data[label],
                c = c_list[index],
                s = 40,
                label = label_clean)

ax = plt.gca()  
# Set axis limits
ax.set_xlim(2, 8)        
ax.set_ylim(2, 8)        

# Create legend
lgd = plt.legend(bbox_to_anchor=(1.02, 1),
                 loc=2,
                 borderaxespad=0.)

# Set axis and plot titles
ax.set_ylabel('Log Koc')
ax.set_xlabel('Log Kow (from Literature)')
title = 'Log Koc/Kow Measurements for PAH'
ax.set_title(title)

# Save figure to pdf
outname = 'LogKocKow_PAH_Loctype.pdf' 
fig = ax.get_figure();
fig.suptitle('')
fig.savefig(outname, bbox_inches='tight')