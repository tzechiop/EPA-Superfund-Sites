# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 13:54:23 2016

@author: thasegawa
"""

import os
import pandas as pd
import numpy as np

def calculate_suspended(TSS, solids, chemical):
    if (~np.isnan(TSS)) and (~np.isnan(solids)):
        if chemical == 'PAH':
            suspended = solids/TSS
        else:
            suspended = solids/TSS/1000
    else:
        suspended = np.nan
    return suspended
    
def calculate_wholewater(dissolved, suspended):
    if np.isnan(dissolved) and np.isnan(suspended):
        value = np.nan
    elif np.isnan(dissolved):
        value = suspended
    elif np.isnan(suspended):
        value = dissolved
    else:
        value = dissolved + suspended
    return value
    
def calculate_percentdissolved(dissolved, wholewater):
    if (~np.isnan(dissolved)) and (~np.isnan(wholewater)):
        value = dissolved/wholewater
    elif np.isnan(dissolved):
        value = 0
    else:
        value = np.nan
    return value

maindir = r"C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek\Summary Stats"
os.chdir(maindir)
chemical = 'PAH'
suffix = 'v3'

sampleidcol = 'dep_{0}s$`#sys_sample_code`'.format(chemical.lower())

# Read data
if chemical == 'PAH':
    data = pd.read_excel(os.path.join(maindir, 'DEP_CSO_WWTP_pah_cast.xlsx'))
else:
    data = pd.read_excel(os.path.join(maindir, 'DEP_CSO_WWTP_pcbs_cast.xlsx'))

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
            
TPCB_list = ["PCB1",
"PCB10",
"PCB103",
"PCB104",
"PCB105",
"PCB106",
"PCB107",
"PCB108",
"PCB11",
"PCB110",
"PCB111",
"PCB112",
"PCB114",
"PCB118",
"PCB12",
"PCB120",
"PCB121",
"PCB122",
"PCB123",
"PCB126",
"PCB127",
"PCB128",
"PCB129",
"PCB130",
"PCB131",
"PCB132",
"PCB133",
"PCB134",
"PCB135",
"PCB136",
"PCB137",
"PCB139",
"PCB14",
"PCB141",
"PCB144",
"PCB145",
"PCB146",
"PCB147",
"PCB148",
"PCB15",
"PCB150",
"PCB152",
"PCB153",
"PCB155",
"PCB156",
"PCB158",
"PCB159",
"PCB16",
"PCB162",
"PCB164",
"PCB165",
"PCB167",
"PCB169",
"PCB17",
"PCB170",
"PCB171",
"PCB172",
"PCB174",
"PCB175",
"PCB176",
"PCB177",
"PCB178",
"PCB179",
"PCB18",
"PCB180",
"PCB181",
"PCB182",
"PCB183",
"PCB184",
"PCB186",
"PCB187",
"PCB188",
"PCB189",
"PCB19",
"PCB190",
"PCB191",
"PCB192",
"PCB194",
"PCB195",
"PCB196",
"PCB197",
"PCB198",
"PCB2",
"PCB20",
"PCB201",
"PCB202",
"PCB203",
"PCB204",
"PCB205",
"PCB206",
"PCB207",
"PCB208",
"PCB209",
"PCB21",
"PCB22",
"PCB23",
"PCB24",
"PCB25",
"PCB26",
"PCB27",
"PCB3",
"PCB31",
"PCB32",
"PCB34",
"PCB35",
"PCB36",
"PCB37",
"PCB38",
"PCB39",
"PCB4",
"PCB40",
"PCB42",
"PCB43",
"PCB44",
"PCB45",
"PCB46",
"PCB48",
"PCB49",
"PCB5",
"PCB50",
"PCB52",
"PCB54",
"PCB55",
"PCB56",
"PCB57",
"PCB58",
"PCB59",
"PCB6",
"PCB60",
"PCB61",
"PCB63",
"PCB64",
"PCB66",
"PCB67",
"PCB68",
"PCB7",
"PCB72",
"PCB73",
"PCB77",
"PCB78",
"PCB79",
"PCB8",
"PCB80",
"PCB81",
"PCB82",
"PCB83",
"PCB84",
"PCB85",
"PCB86",
"PCB88",
"PCB89",
"PCB9",
"PCB90",
"PCB92",
"PCB93",
"PCB94",
"PCB96"]

# Calculate TPAH16 and TPAH17
if chemical == 'PAH':
    data['TPAH16'] = data.apply(lambda x: sum([value for value in x[PAH16_list] if ~np.isnan(value)]), axis = 1)
    data['TPAH17'] = data.apply(lambda x: sum([value for value in x[PAH17_list] if ~np.isnan(value)]), axis = 1)
else:
    data['TPCB'] = data.apply(lambda x: sum([value for value in x[TPCB_list] if ~np.isnan(value)]), axis = 1)

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
data_ww['LocType'] = data_ww[sampleidcol + '_d'].apply(lambda x: 'CSO' if 'CSO' in x else 'WWTP')
data_ww['Location'] = data_ww['LocEvent'].apply(lambda x: x.split('_')[0])
data_ww['Event'] = data_ww['LocEvent'].apply(lambda x: x.split('_')[1])
columns = ['Phase', 'LocType', 'Location', 'Event', 'LocEvent'] + list(chemical_columns)
data_ww = data_ww[columns]

# Append wholewater to original dataset
data = data.append(data_ww)[data_columns]

# Calculate suspended
data_ss = data[data['Phase'] == 'Solids']
for chemical_column in chemical_columns:
    data_ss[chemical_column] = data_ss.apply(lambda x: calculate_suspended(x['TSS'], x[chemical_column], chemical), axis = 1)
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
data_dw['LocType'] = data_dw[sampleidcol + '_d'].apply(lambda x: 'CSO' if 'CSO' in x else 'WWTP')
data_dw['Location'] = data_dw['LocEvent'].apply(lambda x: x.split('_')[0])
data_dw['Event'] = data_dw['LocEvent'].apply(lambda x: x.split('_')[1])
columns = ['Phase', 'LocType', 'Location', 'Event', 'LocEvent'] + list(chemical_columns)
data_dw = data_dw[columns]

# Append % dissolved to original dataset
data = data.append(data_dw)[data_columns]

# Print dataset
data.to_excel('data_{0}_{1}.xlsx'.format(chemical,suffix))