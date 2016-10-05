# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 09:51:45 2016

@author: thasegawa
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
from collections import OrderedDict

def convertValue(x, newunit = 'mg/kg'):
    conv= {'mg/kg': 10**(-3),
           'ng/kg': 10**(-9),
           'ug/kg': 10**(-6)}
    oldunit = x['target_unit']
    converted_value = x['result_value'] * conv[oldunit] / conv[newunit]
    return converted_value
    
def plotData(eventdata, outdir, units, chemical, eventx, eventy, suffix = ''):
    xdata = eventdata['converted_value_x']
    ydata = eventdata['converted_value_y']
    plt.scatter(xdata,
                ydata,
                s = 10,
                lw = 0,
                zorder = 3)
         
    # Set plot limits
    ax = plt.gca()
    if units != 'pct':
        mindata = min(xdata.min(),ydata.min())
        maxdata = max(xdata.max(),ydata.max())
        minaxis = 10**np.floor(np.log10(mindata))*0.9
        maxaxis = 10**np.ceil(np.log10(maxdata))*1.1
        ax.set_yscale("log", nonposy='clip')
        ax.set_xscale("log", nonposy='clip')
    else:
        minaxis = 0
        maxaxis = 20    
    ax.set_ylim(minaxis, maxaxis)        
    ax.set_xlim(minaxis, maxaxis) 

    plt.plot([minaxis, maxaxis], [minaxis, maxaxis], color='r', linestyle='-', linewidth=0.5, zorder = 1)       
    
    # Set axis titles and remove axes title
    title = 'Sediment Trap Measurements {0} vs {1}'.format(eventx, eventy)
    ax.set_title(title)       
    ax.set_ylabel('{0} during {1} ({2})'.format(chemical, eventy, units))
    ax.set_xlabel('{0} during {1} ({2})'.format(chemical, eventx, units))

    outfname = 'SedimentTrapMeasurements_{0}_{1}_{2}vs{3}.pdf'.format(suffix, chemical, eventx, eventy)
    fig = ax.get_figure();
    fig.savefig(os.path.join(outdir, outfname), bbox_inches='tight')
    plt.clf()

# =============================================================================

maindir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek'
outdir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek\Sediment Trap Plots Round vs Round'

os.chdir(maindir)

fname = 'NCP2_SedTrapEvents1_9_Compiled_wTotals_wParticulates.xlsx'

#==============================================================================
# chemical_list = ['TPAH (17)',
#                  'TPCB (Congeners)',
#                  "Mercury",
#                  "Copper",
#                  "Lead",
#                  "Acenaphthene",
#                  "Acenaphthylene",
#                  "Anthracene",
#                  "Benzo(a)anthracene",
#                  "Benzo(a)pyrene",
#                  "Benzo(b)fluoranthene",
#                  "Benzo(g,h,i)perylene",
#                  "Benzo(j,k)fluoranthene",
#                  "Chrysene",
#                  "Dibenzo(a,h)anthracene and Dibenzo(a,c)anthracene",
#                  "Fluoranthene",
#                  "Fluorene",
#                  "Indeno(1,2,3-c,d)pyrene",
#                  "Naphthalene",
#                  "Phenanthrene",
#                  "Pyrene",
#                  "2-Methylnaphthalene"]
#==============================================================================

chemical_list = ['Total organic carbon']

data = pd.read_excel(fname)

datacols = ['Location', 'Event', 'chemical_name', 'converted_value', 'target_unit']

for index, chemical in enumerate(chemical_list):
    plotdata = data[data['chemical_name'] == chemical]
    
    # Identify units
    units = plotdata['target_unit'].unique()[0]
    
    # Convert units to mg/kg
    datacol = 'converted_value'
    if units == 'pct':
        plotdata[datacol] = plotdata['result_value']
    else:
        plotdata[datacol] = plotdata.apply(convertValue, axis = 1)      
        units = 'mg/kg'
    
    # Retrieve data for each event
    event1 = plotdata[plotdata['Event'] == 'Event 1']
    event3 = plotdata[plotdata['Event'] == 'Event 3']
    event6 = plotdata[plotdata['Event'] == 'Event 6']
    event9 = plotdata[plotdata['Event'] == 'Event 9']
    
    # Retrieve location for each sample
    event1['Location'] = event1['sys_loc_code'].apply(lambda x: x.split('-')[0])
    event3['Location'] = event3['sys_loc_code'].apply(lambda x: x.split('-')[0])
    event6['Location'] = event6['sys_loc_code'].apply(lambda x: x.split('-')[0])
    event9['Location'] = event9['sys_loc_code'].apply(lambda x: x.split('-')[0])
    
    # Join events
    event1vs3 = pd.merge(event1[datacols], event3[datacols], on = 'Location')
    event3vs6 = pd.merge(event3[datacols], event6[datacols], on = 'Location')
    event3vs9 = pd.merge(event3[datacols], event9[datacols], on = 'Location')
    event6vs9 = pd.merge(event6[datacols], event9[datacols], on = 'Location')
                
    plotData(event1vs3, outdir, units, chemical, eventx = 'Event 1', eventy = 'Event 3', suffix = '{:0>2}'.format(index))
    plotData(event3vs6, outdir, units, chemical, eventx = 'Event 3', eventy = 'Event 6', suffix = '{:0>2}'.format(index))
    plotData(event3vs9, outdir, units, chemical, eventx = 'Event 3', eventy = 'Event 9', suffix = '{:0>2}'.format(index))
    plotData(event6vs9, outdir, units, chemical, eventx = 'Event 6', eventy = 'Event 9', suffix = '{:0>2}'.format(index))












































