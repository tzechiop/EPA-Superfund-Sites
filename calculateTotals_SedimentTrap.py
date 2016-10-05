# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 16:26:52 2016

@author: thasegawa
"""

import os
import pandas as pd
import numpy as np
import sys

# Function that aggregate total chemicals ('TPAH (16)', 'TPAH (17)' or 'TPCB (Congeners)')
# and appends the results to the input dataframe, returning the compiled dataframe
def calculateTotals(aggchem, data, totalchemical_dict = None, idcol = 'sys_loc_code'):
    if 'TPAH' in aggchem:
        indices = data['chemical_name'].apply(lambda x: True if x in totalchemical_dict[aggchem] else False)
    elif aggchem == 'TPCB (Congeners)':
        indices = data['chemical_name'].apply(lambda x: True if 'PCB-' in x else False)
    else:
        print('Chemical not regonized!!! Aborting script...')
        sys.exit()
    subdata = data[indices]
    units = subdata['target_unit'].unique()
    if len(units) == 1:
        units = units[0]
    else:
        print('More than one unit detected!!! Aborting script...')
        sys.exit()
        
    sumgroup = subdata[[idcol, 'Event', 'result_value']].groupby([idcol, 'Event']).sum()
    meangroup = subdata[[idcol, 'Event', 'river_stream_mile', 'x_coord', 'y_coord', ]].groupby([idcol, 'Event']).mean()
    sys_loc_code_list, event_list = zip(*sumgroup.index)

    data = data.append(pd.DataFrame({'sys_loc_code':      list(sys_loc_code_list),
                                     'Event':             list(event_list),
                                     'result_value':      sumgroup['result_value'],
                                     'chemical_name':     [aggchem]*len(sumgroup.index),
                                     'target_unit':       [units]*len(sumgroup.index),
                                     'x_coord':           meangroup['x_coord'],
                                     'y_coord':           meangroup['y_coord'],
                                     'river_stream_mile': meangroup['river_stream_mile']}))
    return data
    
maindir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek'
outdir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek\Sediment Trap Data'

os.chdir(maindir)

fname = 'NCP2_SedTrapEvents1_9_Compiled.xlsx'

totalchemical_dict = {'TPAH (16)':          ["Acenaphthene",
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
                                             "Pyrene"],
                      'TPAH (17)':          ["Acenaphthene",
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
                                             "2-Methylnaphthalene"]}

data = pd.read_excel(fname)
columns = data.columns.values

# Calculate TPAH (16)
aggchem = 'TPAH (16)'
data = calculateTotals(aggchem, data, totalchemical_dict)
                                                               
# Calculate TPAH (17)
aggchem = 'TPAH (17)'
data = calculateTotals(aggchem, data, totalchemical_dict)

# Calculate TPCB (Congeners)
aggchem = 'TPCB (Congeners)'
data = calculateTotals(aggchem, data)

# Print data
fname = 'NCP2_SedTrapEvents1_9_Compiled_wTotals.xlsx'
data = data[columns]
data.to_excel(fname,
              index = False)