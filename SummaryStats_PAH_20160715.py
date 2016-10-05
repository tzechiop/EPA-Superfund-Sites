# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 13:54:23 2016

@author: thasegawa
"""

import os
import pandas as pd
import numpy as np

def calculate_suspended(TSS, solids):
    if (~np.isnan(TSS)) and (~np.isnan(solids)):
        suspended = solids/TSS
    else:
        suspended = np.nan
    return suspended
    
def calculate_wholewater(dissolved, suspended):
    if (~np.isnan(dissolved)) and (~np.isnan(suspended)):
        value = dissolved + suspended
    else:
        value = np.nan
    return value
    
def calculate_percentdissolved(dissolved, wholewater):
    if (~np.isnan(dissolved)) and (~np.isnan(wholewater)):
        value = dissolved/wholewater
    else:
        value = np.nan
    return value
    

maindir = r"C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek\Summary Stats"
os.chdir(maindir)

# Read data
data = pd.read_excel(os.path.join(maindir, 'DEP_CSO_WWTP_pah_cast.xlsx'))

bigCSO_list = ["NCB083", "NCQ077", "NCB015", "BB026"]
PAH17_list = ["Naphthalene",
            "2-Methylnaphthalene",
            "Acenaphthylene",
            "Acenaphthene",
            "Fluorene",
            "Anthracene",
            "Phenanthrene",
            "Fluoranthene",
            "Pyrene",
            "Benz[a]anthracene",
            "Chrysene",
            "Benzo[a]pyrene",
            "Benzo[b]fluoranthene",
            "Benzo[j,k]fluoranthenes",
            "Indeno[1,2,3-cd]pyrene",
            "Benzo[ghi]perylene",
            "Dibenz[a,h]anthracene"]
            
PAH16_list = ["Naphthalene",
            "Acenaphthylene",
            "Acenaphthene",
            "Fluorene",
            "Anthracene",
            "Phenanthrene",
            "Fluoranthene",
            "Pyrene",
            "Benz[a]anthracene",
            "Chrysene",
            "Benzo[a]pyrene",
            "Benzo[b]fluoranthene",
            "Benzo[j,k]fluoranthenes",
            "Indeno[1,2,3-cd]pyrene",
            "Benzo[ghi]perylene",
            "Dibenz[a,h]anthracene"]

# Calculate TPAH16 and TPAH17
data['TPAH16'] = data.apply(lambda x: sum([value for value in x[PAH16_list] if ~np.isnan(value)]), axis = 1)
data['TPAH17'] = data.apply(lambda x: sum([value for value in x[PAH17_list] if ~np.isnan(value)]), axis = 1)

# Retrieve columns that include chemical data
data_columns = data.columns.values
chemical_columns = data_columns[8:]

# Calculate whole water
data_d = data[data['Phase'] == 'Dissolved']
data_s = data[data['Phase'] == 'Solids']
data_ww = pd.merge(data_d, data_s, on = 'LocEvent', suffixes = ('_d', '_s'))
for chemical_column in chemical_columns:
    dissolvedColumn = chemical_column + '_d'
    solidsColumn = chemical_column + '_s'
    data_ww[chemical_column] = data_ww.apply(lambda x: calculate_wholewater(x[dissolvedColumn], x[solidsColumn]), axis = 1)
data_ww['Phase'] = ['Whole Water']*len(data_ww.index)
columns = ['Phase', 'LocEvent'] + list(chemical_columns)
data_ww = data_ww[columns]

# Append wholewater to original dataset
data = data.append(data_ww)[data_columns]

# Calculate suspended
data_ss = data[data['Phase'] == 'Solids']
for chemical_column in chemical_columns:
    data_ss[chemical_column] = data_ss.apply(lambda x: calculate_suspended(x['TSS'], x[chemical_column]), axis = 1)
data_ss['Phase'] = ['Particulates']*len(data_ss.index)

# Append suspended to original dataset
data = data.append(data_ss)[data_columns]

# Calculate % dissolved
data_dissolved = data[data['Phase'] == 'Dissolved']
data_wholewater = data[data['Phase'] == 'Whole Water']
data_dw = pd.merge(data_dissolved, data_wholewater, on = 'LocEvent', suffixes = ('_d', '_ww'))
for chemical_column in chemical_columns:
    dissolvedColumn = chemical_column + '_d'
    wholewaterColumn = chemical_column + '_ww'
    data_dw[chemical_column] = data_dw.apply(lambda x: calculate_percentdissolved(x[dissolvedColumn], x[wholewaterColumn]), axis = 1)
data_dw['Phase'] = ['% Dissolved']*len(data_dw.index)
columns = ['Phase', 'LocEvent'] + list(chemical_columns)
data_dw = data_dw[columns]

# Append % dissolved to original dataset
data = data.append(data_dw)[data_columns]

# Print dataset
data.to_csv('data.csv')