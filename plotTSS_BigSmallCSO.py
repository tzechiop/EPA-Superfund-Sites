# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 10:13:50 2016

@author: thasegawa
"""


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

def staggerX(x, stagger = 0.01):
    newx = np.random.normal(x, stagger, size = 1)[0]
    return newx


maindir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek'
outdir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek\TSS_BigSmallCSO'
os.chdir(maindir)

# Data sources
datasource = 'NCG'
chemical = 'TSS'
datasource_dict = {'NCG': {'fname': 'NCG_CSO_Data_FormattedTables_V2.xlsx',
                           'TSS':   {'sheetname': 'conv_d_DataTable',
                                     'colname':   'Total suspended solids (Solid Phase Sample)',
                                     'phasecol':  False},
                           'TPAH':  {'sheetname': 'PAHs',
                                     'colname':   'TPAH',
                                     'phasecol': 'phase'},
                           'TPCB':  {'sheetname': 'PCBs',
                                     'colname':   'TPCB (SumCongeners)',
                                     'phasecol': 'phase'},
                           'Cu':    {'sheetname': 'metals',
                                     'colname':   'Copper',
                                     'phasecol': 'phase'},
                           'Hg':    {'sheetname': 'metals',
                                     'colname':   'Mercury',
                                     'phasecol': 'phase'},
                           'Lead':  {'sheetname': 'metals',
                                     'colname':   'Lead',
                                     'phasecol': 'phase'}},
                   'DEP': {'fname': 'NYCDEP - Newtown Creek Wet Weather CSO  WWTP Data by Analyte Grouping_V3.xlsx',
                           'TSS':  {'sheetname': 'TSS-POC-DOC',
                                    'colname':   'TSS (mg/L)',
                                    'phasecol':  False},
                           'TPAH': {'sheetname': 'TPAH',
                                    'colname': 'TPAH',
                                    'phasecol': 'Phase'},
                           'TPCB': {'sheetname': 'TPCB',
                                    'colname': 'TPCB (SumCongeners)',
                                    'phasecol': 'Phase'},
                           'Cu':   {'sheetname': 'Metals-DRO-GRO',
                                    'colname': 'COPPER',
                                    'phasecol': 'Phase'},
                           'Hg':   {'sheetname': 'Metals-DRO-GRO',
                                    'colname': 'MERCURY',
                                    'phasecol': 'Phase'},
                           'Lead': {'sheetname': 'Metals-DRO-GRO',
                                    'colname': 'LEAD',
                                    'phasecol': 'Phase'},
                          }
                  }

# Read chemical data
data = pd.read_excel(datasource_dict[datasource]['fname'],
                     sheetname = datasource_dict[datasource][chemical]['sheetname'])
datacol = datasource_dict[datasource][chemical]['colname']

# Read CSO data
year = 2008
bigCSO_list = ["NCB-083", "NCQ-077", "NCB-015", "BB-026"]
csocol = 'Total Volume (US Mgal)'
csodata = pd.read_excel('CSOyearly comparison 2008-2012-new.xlsx',
                        sheetname = 'Data')
cso_year = csodata[csodata['Year'] == year]
                     
# Join chemical and CSO data
joindata = pd.merge(data, cso_year, on = 'Location')

# Split data based on bigCSO_list
joindata['BigCSO'] = joindata['Location'].apply(lambda x: 'Big CSO' if x in bigCSO_list else 'Small CSO')
joindata['x'] = joindata['BigCSO'].apply(lambda x: 1 if x == 'Big CSO' else 2)
joindata['x'] = joindata['x'].apply(staggerX)

# Plot data based on 
labelCol = 'Phase'
# Create scatter plot
ax = joindata.boxplot(column = datacol,
                      by = 'BigCSO',
                      showfliers = False)
ax.grid(zorder=0)
symbol_dict = {'Big CSO':   {'c': 'r',
                             'm': 'o'},
               'Small CSO': {'c': 'b',
                             'm': 'o'}}

labelCol = 'BigCSO'
xtick_labels = ['Big CSOs', 'Small CSOs']
for label in joindata[labelCol].unique():    
    indices = joindata[labelCol] == label
    plotdata = joindata[indices]
    
    c = symbol_dict[label]['c']
    marker = symbol_dict[label]['m']
    
    plt.scatter(plotdata['x'],
                plotdata[datacol],
                c = [c]*len(plotdata.index),  
                marker = marker,          
                s = 40,
                label = label,
                zorder = 3)
                
# Adjust x-ticks
plt.xticks(range(1, len(xtick_labels) + 1), xtick_labels)
ax = plt.gca()  

# Set y -limits
ymin, ymax = ax.get_ylim()
ax.set_ylim(0, ymax)        

# Set axis titles and remove axes title
title = 'Average TSS by CSO group'
ax.set_title(title)       
ax.set_ylabel('TSS (mg/L)')
xlabel = 'Big CSOs: ' + ', '.join(bigCSO_list)
ax.set_xlabel(xlabel)
fig = ax.get_figure();
fig.suptitle('')

# Perform t-test and add result to plot
bigCSO_TSS = joindata.loc[joindata[labelCol] == 'Big CSO', datacol]
smallCSO_TSS = joindata.loc[joindata[labelCol] == 'Small CSO', datacol]
pval = ttest_ind(bigCSO_TSS,
                 smallCSO_TSS,
                 equal_var=False)[1]
text = 'H_0: TSS(Big CSO) = TSS(Small CSO)\n'
text += 'p = {0:.3f}'.format(pval)
plt.text(0.6, 210, text, horizontalalignment = 'left')

# Save figure to pdf
outname = 'AverageTSSByCSOGroup_{0}BigCSO_{1}Data.pdf'.format(len(bigCSO_list), datasource)
fig.savefig(os.path.join(outdir, outname),
            bbox_inches='tight')






























