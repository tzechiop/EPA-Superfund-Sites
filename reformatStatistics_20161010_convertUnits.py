# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 12:17:54 2016

@author: thasegawa
"""

import os
import pandas as pd
import glob

# Convert Min, Max, Median and Mean values in dataframe
def convert(data, conv):
    data['Min'] = data['Min']*conv
    data['Max'] = data['Max']*conv
    data['Median'] = data['Median']*conv
    data['Mean'] = data['Mean']*conv
    return data


# Specify inputs
path = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek\Reformat Statistics 20161005'
os.chdir(path)


# Specify data parameters
group_list = ['All_WW_WWTP',
              'AllCSO',
              'GOW_CSO',
              'NTC_CSO']
              
chem_list = [('pah', 'ng/mg', 'mg/kg', 1),
             ('pcbs', 'pg/mg', 'ng/kg', 10**3),
             ('metals', 'ug/mg', 'mg/kg', 10**3),
             ('pests', 'ng/mg', 'ug/kg', 10**3),
             ('dioxs', 'pg/mg', 'ng/kg', 10**3),
             ('vocs', 'ug/L', 'ug/L', 10**0)]
             

# Perform unit conversions on each group of data
for group in group_list:
    print('Formatting data for %s' % group)
    # Compile data for all pollutants
    for index, (chemname, unit1, unit2, conv) in enumerate(chem_list):
        infname = '{0}_OS_{1}.csv'.format(chemname, group)
        data = pd.read_csv(infname, index_col = 0)
        if chemname == 'metals':
            data[data.index == 'MERCURY'] = convert(data[data.index == 'MERCURY'], 1)
            data[data.index != 'MERCURY'] = convert(data[data.index != 'MERCURY'], conv)
        else:
            data = convert(data, conv)
        
        data.to_csv('converted\\{0}_OS_{1}_conv.csv'.format(chemname, group))
    