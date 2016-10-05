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
                  sheetname = 'Symbols_Compare_DEP')
symbol_dict = {'DEP': {}, 'NCG': {}}

for row in zip(s['Location'], s['R'], s['G'], s['B'], s['M']):
    symbol_dict['DEP'][row[0]] = {'c': [row[1], row[2], row[3]],
                                    'm': row[4]}

s = pd.read_excel('DrainageArea_Symbols.xlsx',
                  sheetname = 'Symbols_Compare_NCG')

for row in zip(s['Location'], s['R'], s['G'], s['B'], s['M']):
    symbol_dict['NCG'][row[0]] = {'c': [row[1], row[2], row[3]],
                                  'm': row[4]}

# Import Drainage Area Data
da = pd.read_excel('DrainageArea_Symbols.xlsx',
                   sheetname = 'DrainageArea')


# Set plot parameters
scatterwidth = 10
pointsize = 30

chemical_list = [['TPAH',    'On Solids (max)',  'os_max',     'mg/kg'],
                 ['TPCB',    'On Solids (max)',  'os_max',     'mg/kg'],
                 ['Cu',      'On Solids',        'os',         'mg/kg'],
                 ['Hg',      'On Solids',        'os',         'mg/kg'],
                 ['Lead',    'On Solids',        'os',         'mg/kg']]

# Read data
datasource_dict = {'NCG': {'fname': 'NCG_CSO_Data_FormattedTables_V2.xlsx',
                           'TSS':   {'sheetname': 'conv_d_DataTable',
                                     'colname':   'Total suspended solids (Solid Phase Sample)'},
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
                           'TSS': {'sheetname': 'TSS-POC-DOC',
                                   'colname':   'TSS (mg/L)'},
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
    chemical = iteration[0]
    phase_DEP = iteration[1]
    phase_NCG = iteration[2]
    units = iteration[3]
    
    # Plot DEP data
    datasource = 'DEP'
    data = pd.read_excel(datasource_dict[datasource]['fname'],
                         sheetname = datasource_dict[datasource][chemical]['sheetname'])
                         
    # If appropriate, filter for phase
    if phase_DEP:
        phasecol = datasource_dict[datasource][chemical]['phasecol']
        data = data[data[phasecol] == phase_DEP]
    data = pd.merge(data, da, on = 'Location')
                         
    xcol = 'Drainage Area (acres)'
    ycol = datasource_dict[datasource][chemical]['colname']
    csocol = 'Location'
    
    # Plot data
    for cso, symbol in symbol_dict[datasource].items():
        xdata = data.loc[data[csocol] == cso, xcol].apply(lambda x: x + np.random.randn()*scatterwidth)
        ydata = data.loc[data[csocol] == cso, ycol]
        numpts = len(xdata)
        plt.scatter(xdata,
                    ydata,
                    facecolors = [symbol['c'] for x in range(numpts)],
                    marker = symbol['m'],
                    s = pointsize,
                    label = cso + ' ({0})'.format(datasource))
                    
    max_DEP = data[ycol].max()
                    
    # Plot NCG data
    datasource = 'NCG'
    data = pd.read_excel(datasource_dict[datasource]['fname'],
                         sheetname = datasource_dict[datasource][chemical]['sheetname'])
                         
    # If appropriate, filter for phase
    if phase_NCG:
        phasecol = datasource_dict[datasource][chemical]['phasecol']
        data = data[data[phasecol] == phase_NCG]
    data = pd.merge(data, da, on = 'Location')
                         
    xcol = 'Drainage Area (acres)'
    ycol = datasource_dict[datasource][chemical]['colname']
    csocol = 'Location'
    
    # Plot data
    for cso, symbol in symbol_dict[datasource].items():
        xdata = data.loc[data[csocol] == cso, xcol].apply(lambda x: x + np.random.randn()*scatterwidth)
        ydata = data.loc[data[csocol] == cso, ycol]
        numpts = len(xdata)
        plt.scatter(xdata,
                    ydata,
                    facecolors = [symbol['c'] for x in range(numpts)],
                    marker = symbol['m'],
                    s = pointsize,
                    label = cso + ' ({0})'.format(datasource))    
                    
    max_NCG = data[ycol].max()
    
    # Create Legend
    lgd = plt.legend(bbox_to_anchor=(1.02, 1),
             loc=2,
             borderaxespad=0.,
             prop={'size':9},
             scatterpoints = 1)
    
    # Set axis limits         
    ax = plt.gca()
    ax.set_xlim(-50, 2500)
    ax.set_ylim(0, max([max_DEP, max_NCG])*1.15)        
                
    # Set plot labels
    ax.set_ylabel('{0} ({1})'.format(chemical, units))
    ax.set_xlabel('Drainage Area (acres)')
    if phase_NCG:
        title = '{0} Samples ({1}) for {2} Data'.format(chemical, phase_NCG, datasource)
    else:
        title = '{0} Samples for {2} Data'.format(chemical, phase_NCG, datasource)
    ax.set_title(title)
    
    # Print plot
    if phase_NCG:
        outname = '{3:0>2}{0}_{1}vsDrainageArea_NCGvDEP_{2}.pdf'.format(datasource, chemical, phase_NCG, index + 1)
    else:
        outname = '{2:0>2}{0}_{1}vsDrainageArea_NCGvDEP.pdf'.format(datasource, chemical, index + 1)
    fig = ax.get_figure();
    fig.savefig(os.path.join(outdir, outname), bbox_inches='tight')
    plt.clf()