# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 10:58:54 2016

@author: thasegawa
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as color

maindir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek'
outdir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek\TSSvsDrainage'
os.chdir(maindir)
                  
# Create dictionary for scatter plot symbols
s = pd.read_excel('DrainageArea_Symbols.xlsx',
                  sheetname = 'Symbols_DEP')
symbol_dict = {}
index = 0
for row in zip(s['Location'], s['R'], s['G'], s['B'], s['M']):
    symbol_dict[row[0]] = {'c': [row[1], row[2], row[3]],
                           'm': row[4]}

# Import Drainage Area Data
da = pd.read_excel('DrainageArea_Symbols.xlsx',
                   sheetname = 'DrainageArea')


# Set data parameters
datasource = 'DEP'
chemical = 'TPAH'
phase = 'On Solids'
units = 'mg/kg'

#==============================================================================
# chemical_list = [['DEP',     'TSS',     False,         'mg/L'],
#                  ['DEP',     'TPAH',    'On Solids',   'mg/kg'],
#                  ['DEP',     'TPAH',    'Whole Water', 'ng/L'],
#                  ['DEP',     'TPCB',    'On Solids',   'mg/kg'],
#                  ['DEP',     'TPCB',    'Whole Water', 'ng/L'],
#                  ['DEP',     'Cu',      'On Solids',   'mg/kg'],
#                  ['DEP',     'Cu',      'Whole Water', 'ug/L'],
#                  ['DEP',     'Hg',      'On Solids',   'mg/kg'],
#                  ['DEP',     'Hg',      'Whole Water', 'ng/L'],
#                  ['DEP',     'Lead',    'On Solids',   'mg/kg'],
#                  ['DEP',     'Lead',    'Whole Water', 'ug/L']]
#==============================================================================
chemical_list = [['DEP',     'TSS',     False,         'mg/L']]


# Read data
datasource_dict = {'NCG': {'fname': 'NCG_TSS_wDrainage.xlsx',
                           'TSS':   {'sheetname': 'TSSData',
                                     'colname':   'TSS mg/L'
                                    }
                          },
                   'DEP': {'fname': 'NYCDEP - Newtown Creek Wet Weather CSO  WWTP Data by Analyte Grouping_V3.xlsx',
                           'TSS': {'sheetname': 'TSS-POC-DOC',
                                   'colname':   'TSS (mg/L)'
                                  },
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

for index, iteration in enumerate(chemical_list):
    datasource = iteration[0]
    chemical = iteration[1]
    phase = iteration[2]
    units = iteration[3]
    data = pd.read_excel(datasource_dict[datasource]['fname'],
                         sheetname = datasource_dict[datasource][chemical]['sheetname'])
                         
    # If appropriate, filter for phase
    if phase:
        phasecol = datasource_dict[datasource][chemical]['phasecol']
        data = data[data[phasecol] == phase]
    data = pd.merge(data, da, on = 'Location')
                         
    xcol = 'Drainage Area (acres)'
    ycol = datasource_dict[datasource][chemical]['colname']
    csocol = 'Location'
    
    # Plot data
    for cso, symbol in symbol_dict.items():
        xdata = data.loc[data[csocol] == cso, xcol]
        ydata = data.loc[data[csocol] == cso, ycol]
        numpts = len(xdata)
        plt.scatter(data.loc[data[csocol] == cso, xcol],
                    data.loc[data[csocol] == cso, ycol],
                    facecolors = [symbol['c'] for x in range(numpts)],
                    marker = symbol['m'],
                    s = 60,
                    label = cso)
                    
    # Create Legend
    lgd = plt.legend(bbox_to_anchor=(1.02, 1),
             loc=2,
             borderaxespad=0.,
             scatterpoints = 1)
    
    # Set axis limits         
    ax = plt.gca()
    ax.set_xlim(0, 2500)
    ax.set_ylim(0, data[ycol].max()*1.15)        
                
    # Set plot labels
    ax.set_ylabel('{0} ({1})'.format(chemical, units))
    ax.set_xlabel('Drainage Area (acres)')
    if phase:
        title = '{0} Samples ({1}) for {2} Data'.format(chemical, phase, datasource)
    else:
        title = '{0} Samples for {2} Data'.format(chemical, phase, datasource)
    ax.set_title(title)
    
    # Print plot
    if phase:
        outname = '{3:0>2}{0}_{1}vsDrainageArea_{2}_NoOutlier_20160728.pdf'.format(datasource, chemical, phase, index + 1)
    else:
        outname = '{2:0>2}{0}_{1}vsDrainageArea_NoOutlier_20160728.pdf'.format(datasource, chemical, index + 1)
    fig = ax.get_figure();
    fig.savefig(os.path.join(outdir, outname), bbox_inches='tight')
    plt.clf()