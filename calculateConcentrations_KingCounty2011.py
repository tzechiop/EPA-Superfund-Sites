# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 13:16:22 2016

@author: thasegawa
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 16:26:52 2016

@author: thasegawa
"""

import os
import pandas as pd
import sys

# Function that aggregate total chemicals ('TPAH (16)', 'TPAH (17)' or 'TPCB (Congeners)')
# and appends the results to the input dataframe, returning the compiled dataframe
def calculateTotals(aggchem, data, totalchemical_dict = None, datacol = 'result_value', chemcol = 'chemical_name', idcol = 'sys_loc_code', unitscol = 'target_unit'):
    if aggchem in totalchemical_dict:
        indices = data[chemcol].apply(lambda x: True if x in totalchemical_dict[aggchem] else False)
    else:
        print('Chemical not regonized!!! Aborting script...')
        sys.exit()
    subdata = data[indices]
    units = subdata[unitscol].unique()
    if len(units) == 1:
        units = units[0]
    else:
        print('More than one unit detected!!! Aborting script...')
        sys.exit()
        
    sumgroup = subdata[[idcol, datacol]].groupby([idcol]).sum()
    sys_loc_code_list = sumgroup.index

    data = pd.DataFrame({'sys_loc_code':      list(sys_loc_code_list),
                         'result_value':      sumgroup[datacol],
                         'chemical_name':     [aggchem]*len(sumgroup.index),
                         'target_unit':       [units]*len(sumgroup.index)})
    return data
    
# ==============================================================================
# Read in TPAH and TPCB lists
maindir = r'# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 16:26:52 2016

@author: thasegawa
"""

import os
import pandas as pd
import sys

# Function that aggregate total chemicals ('TPAH (16)', 'TPAH (17)' or 'TPCB (Congeners)')
# and appends the results to the input dataframe, returning the compiled dataframe
def calculateTotals(aggchem, data, totalchemical_dict = None, datacol = 'result_value', chemcol = 'chemical_name', idcol = 'sys_loc_code', unitscol = 'target_unit'):
    if aggchem in totalchemical_dict:
        indices = data[chemcol].apply(lambda x: True if x in totalchemical_dict[aggchem] else False)
    else:
        print('Chemical not regonized!!! Aborting script...')
        sys.exit()
    subdata = data[indices]
    units = subdata[unitscol].unique()
    if len(units) == 1:
        units = units[0]
    else:
        print('More than one unit detected!!! Aborting script...')
        sys.exit()
        
    sumgroup = subdata[[idcol, datacol]].groupby([idcol]).sum()
    sys_loc_code_list = sumgroup.index

    data = pd.DataFrame({'sys_loc_code':      list(sys_loc_code_list),
                         'result_value':      sumgroup[datacol],
                         'chemical_name':     [aggchem]*len(sumgroup.index),
                         'target_unit':       [units]*len(sumgroup.index)})
    return data
    
# ==============================================================================
# Read in TPAH and TPCB lists
maindir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Chemical Lists'
os.chdir(maindir)
totalchemical_dict = {}

with open('TPAH16_2011KingCountySediments.txt', 'r') as f:
    totalchemical_dict['TPAH (16)'] = [chemical.strip() for chemical in f.readlines()]

with open('TPAH17_2011KingCountySediments.txt', 'r') as f:
    totalchemical_dict['TPAH (17)'] = [chemical.strip() for chemical in f.readlines()]

# Read in EDD Data    
maindir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek'
outdir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek'

os.chdir(maindir)

fname = 'CompiledTable_2011KingCountySediments.xlsx'

data = pd.read_excel(fname)
data = data[data['STATION_NAME'] == 'Newtown Creek Influent']
data['UNIQID'] = data.apply(lambda x: x['SAMP_ID'] + '_' + x['ANALYSIS_METH'],axis = 1)
columns = data.columns.values

# Calculate TPAH (16)
aggchem = 'TPAH (16)'
newdata = calculateTotals(aggchem, data, totalchemical_dict, datacol = 'RESULT', chemcol = 'PARAM', idcol = 'UNIQID', unitscol = 'UNIT')
                                                               
# Calculate TPAH (17)
aggchem = 'TPAH (17)'
newdata = newdata.append(calculateTotals(aggchem, data, totalchemical_dict, datacol = 'RESULT', chemcol = 'PARAM',idcol = 'UNIQID', unitscol = 'UNIT'))

# Calculate TPCB (Congeners)
aggchem = 'TPCB (Congeners)'
newdata = newdata.append(calculateTotals(aggchem, data, totalchemical_dict, datacol = 'RESULT', chemcol = 'PARAM',idcol = 'UNIQID', unitscol = 'UNIT'))

# Print data
fname = 'CARP_V_HRL_RESULTS_NOQC_NCCSO_Totals.xlsx'
#newdata = newdata[columns]
newdata.to_excel(fname,
                 index = False)'
os.chdir(maindir)
totalchemical_dict = {}

with open('TPAH16_CARP.txt', 'r') as f:
    totalchemical_dict['TPAH (16)'] = [chemical.strip() for chemical in f.readlines()]

with open('TPAH17_CARP.txt', 'r') as f:
    totalchemical_dict['TPAH (17)'] = [chemical.strip() for chemical in f.readlines()]

with open('TPCBCongener_CARP.txt', 'r') as f:
    totalchemical_dict['TPCB (Congeners)'] = [chemical.strip() for chemical in f.readlines()]

# Read in EDD Data    
maindir = r'C:\CARP_UI_Data'
outdir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek'

os.chdir(maindir)

fname = 'CARP_V_HRA_RESULTS_VAL_NOQC.xlsx'

data = pd.read_excel(fname)
data = data[data['STATION_NAME'] == 'Newtown Creek Influent']
data['UNIQID'] = data.apply(lambda x: x['SAMP_ID'] + '_' + x['ANALYSIS_METH'],axis = 1)
columns = data.columns.values

# Calculate TPAH (16)
aggchem = 'TPAH (16)'
newdata = calculateTotals(aggchem, data, totalchemical_dict, datacol = 'RESULT', chemcol = 'PARAM', idcol = 'UNIQID', unitscol = 'UNIT')
                                                               
# Calculate TPAH (17)
aggchem = 'TPAH (17)'
newdata = newdata.append(calculateTotals(aggchem, data, totalchemical_dict, datacol = 'RESULT', chemcol = 'PARAM',idcol = 'UNIQID', unitscol = 'UNIT'))

# Calculate TPCB (Congeners)
aggchem = 'TPCB (Congeners)'
newdata = newdata.append(calculateTotals(aggchem, data, totalchemical_dict, datacol = 'RESULT', chemcol = 'PARAM',idcol = 'UNIQID', unitscol = 'UNIT'))

# Print data
fname = 'CARP_V_HRL_RESULTS_NOQC_NCCSO_Totals.xlsx'
#newdata = newdata[columns]
newdata.to_excel(fname,
                 index = False)