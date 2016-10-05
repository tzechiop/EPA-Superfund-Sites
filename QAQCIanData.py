# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 14:26:06 2016

@author: thasegawa
"""

import os
import pandas as pd
import numpy as np

def splitData(data, chemname = False, locname = False, eventname = False, typename = False):
    
    if chemname:
        data = data[data['chemical_name'].notnull()]
        data = data[data['chemical_name'] == chemname]    
    if locname:
        data = data[data['Location'].notnull()]
        data = data[data['Location'].str.contains(locname)]
    if eventname:
        data = data[data['Event'].notnull()]
        data = data[data['Event'].str.contains(eventname)]
    if typename:
        data = data[data['Type'].notnull()]
        data = data[data['Type'].str.contains(typename)]
    
    print('Returning {0} rows...'.format(len(data.index)))
    return data
    
def trimCol(data):
    data = data[['#sys_sample_code',
                 'chemical_name',
                 'Location',
                 'Event',
                 'Type',
                 'result_value',
                 'result_unit']]
    return data
    
def organizeTable(data, colnames = ['chemical_name', 'Type', 'Event', 'Location']):
    data = data.sort_values(colnames)
    return data

maindir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek'
fname = 'Book2.xlsx'

data = pd.read_excel(os.path.join(maindir, fname))
subdata = data[data['detect_flag'] == 'Y']
subdata = subdata[subdata['reportable_result'] == 'Yes']
subdata = subdata[subdata['result_type_code'].isin(['CAL','TRG'])]


chemname = "POC"
locname = 'WW-15'
eventname = 'BB-009'
#typename = 'CSO'

subdata1 = splitData(subdata, chemname, locname, eventname)
subdata1 = trimCol(subdata1)
subdata1 = organizeTable(subdata1)
print(subdata1)