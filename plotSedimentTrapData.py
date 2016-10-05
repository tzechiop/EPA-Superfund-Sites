# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 16:26:52 2016

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
    
    
    
maindir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek'
outdir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek\Sediment Trap Plots'

os.chdir(maindir)

fname = 'NCP2_SedTrapEvents1_9_Compiled_wTotals_wParticulates.xlsx'

chemical_list = ['TPAH (16)',
                 'TPAH (17)',
                 'TPCB (Congeners)',
                 "Mercury",
                 "Aluminum",
                 "Calcium",
                 "Iron",
                 "Magnesium",
                 "Potassium",
                 "Sodium",
                 "Antimony",
                 "Arsenic",
                 "Barium",
                 "Beryllium",
                 "Cadmium",
                 "Chromium",
                 "Cobalt",
                "Copper",
                 "Lead",
                 "Manganese",
                 "Nickel",
                 "Selenium",
                 "Silver",
                 "Thallium",
                 "Tin",
                 "Vanadium",
                 "Zinc",
                 'PCB-011',
                 'Total Monochlorobiphenyl homologs (U = 0)',
                 'Total Dichlorobiphenyl homologs (U = 0)',
                 'Total Trichlorobiphenyl homologs (U = 0)',
                 'Total Tetrachlorobiphenyl homologs (U = 0)',
                 'Total Pentachlorobiphenyl homologs (U = 0)',
                 'Total Hexachlorobiphenyl homologs (U = 0)',
                 'Total Heptachlorobiphenyl homologs (U = 0)',
                 'Total Octachlorobiphenyl homologs (U = 0)',
                 'Total Nonachlorobiphenyl homologs (U = 0)',
                 'Total Decachlorobiphenyl homologs (U = 0)',
                 'Total solids',
                 "Acenaphthene",
                 "Acenaphthylene",
                 "Anthracene",
                 "Benzo(a)anthracene",
                 "Benzo(a)pyrene",
                 "Benzo(b)fluoranthene",
                 "Benzo(g,h,i)perylene",
                 "Benzo(j,k)fluoranthene",
                 "Chrysene",
                 "Dibenzo(a,h)anthracene and Dibenzo(a,c)anthracene",
                 "Fluoranthene",
                 "Fluorene",
                 "Indeno(1,2,3-c,d)pyrene",
                 "Naphthalene",
                 "Phenanthrene",
                 "Pyrene",
                 "2-Methylnaphthalene"]

data = pd.read_excel(fname)

event_markers = OrderedDict()
event_markers['Event 1'] = 'b'
event_markers['Event 2'] = 'g'
event_markers['Event 3'] = 'r'
event_markers['Event 4'] = 'c'
event_markers['Event 5'] = 'm'
event_markers['Event 6'] = 'y'
event_markers['Event 7'] = 'k'
event_markers['Event 8'] = 'brown'
event_markers['Event 9'] = 'lime'
event_markers['CSO Particulates'] = 'orange'

for chemical in chemical_list:
    plotdata = data[data['chemical_name'] == chemical]

    # Identify units
    units = plotdata['target_unit'].unique()[0]
    
    # Convert units to mg/kg
    if units == 'pct':
        datacol = 'result_value'
    else:
        datacol = 'converted_value'
        plotdata[datacol] = plotdata.apply(convertValue, axis = 1)      
        units = 'mg/kg'
                
    for event, color in event_markers.items():
        indices = plotdata['Event'] == event
        #xdata = plotdata.loc[indices, 'river_stream_mile'].apply(staggerX)
        xdata = plotdata.loc[indices, 'river_stream_mile']
        ydata = plotdata.loc[indices, datacol]
        plt.scatter(xdata,
                    ydata,
                    s = 5,
                    lw = 0,
                    c = color,
                    label = event)
                    
    lgd = plt.legend(bbox_to_anchor=(1.02, 1),
         loc=2,
         borderaxespad=0.,
         prop={'size':9},
         scatterpoints = 1)
         
    # Set plot limits
    ax = plt.gca()
    ax.set_xlim(-0.1, 3.5)
    if chemical != 'Total solids':
        ymin = 10**np.floor(np.log10(plotdata[datacol].min()))
        ymax = 10**np.ceil(np.log10(plotdata[datacol].max()))*1.1
        ax.set_yscale("log", nonposy='clip')
    else:
        ymin = 0
        ymax = 100    
    ax.set_ylim(ymin, ymax)        
    
    # Set axis titles and remove axes title
    title = 'Sediment Trap Measurements by River Mile'.format(chemical)
    ax.set_title(title)       
    ax.set_ylabel('{0} {1}'.format(chemical, units))
    ax.set_xlabel('River Stream Mile (mi)')

    outfname = 'SedimentTrapMeasurements_{0}.pdf'.format(chemical)
    fig = ax.get_figure();
    fig.savefig(os.path.join(outdir, outfname), bbox_inches='tight')
    plt.clf()
            