# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 12:17:54 2016

@author: thasegawa
"""

import os
import pandas as pd
from math import log10, floor

# function to format with less than sign
def lessthan(x, sigfig = 3):
    rounded = round(x, -int(floor(log10(x))) + sigfig - 1)
    if log10(rounded) >= log10(100):
        rounded = int(rounded)
    if x < 10:
        deci = abs(floor(log10(x))) + sigfig - 1
        string = '<{0:.{1}f}'.format(rounded, deci)
    else:
        string = '<{0}'.format(rounded)
    return string


# Format min or median values based on IsMinDetect or IsMedianDetect
def formatValues(data, valcol, detectcol, qual = ['Y', 'YY'], sigfig = 3):
    idx = data['Detect'] > 0
    data[valcol][idx] = data[valcol][idx].apply(lambda x: lessthan(x) if (type(x) != str) and (abs(x) != float('Inf'))  and (x != float('NaN')) else x)
    idx = data[detectcol].isin(['Y','YY'])
    data[valcol][idx] = data[valcol][idx].apply(lambda x: x[1:])
    
    return data
    
# Format group statistics (i.e., min, max, median, mean) based on presence of detected samples
def formatValues2(data, decnum = 4):
    for valcol in ['Min', 'Max','Median','Mean']:
        idx = (data['Detect'] == 0) & (data['N'] > 0) & (data[valcol].notnull())
        data[valcol][idx] = data[valcol][idx].apply(lambda x: lessthan(x) if (type(x) != str) and (abs(x) != float('Inf')) and (x != float('NaN')) else x)
        idx = ((data['Detect'] != 0) | (data['N'] == 0)) & (data[valcol].notnull())
        data[valcol][idx] = data[valcol][idx].apply(lambda x: lessthan(x)[1:] if (type(x) != str) and (abs(x) != float('Inf')) and (x != float('NaN')) else x)
        
    return data


# Specify inputs
path = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek\Reformat Statistics 20161005'
os.chdir(path)

# Specify data parameters
group_list = ['All_WW_WWTP',
              'AllCSO',
              'GOW_CSO',
              'NTC_CSO']
              
chem_list = [('pah', 'mg/mg', 'mg/kg', 10**6),
             ('pcbs', 'pg/mg', 'ng/kg', 10**3),
             ('metals', 'ug/mg', 'mg/kg', 10**3),
             ('pests', 'mg/mg', 'ug/kg', 10**9),
             ('dioxs', 'pg/mg', 'ng/kg', 10**3),
             ('vocs', 'ug/L', 'ug/L', 10**0)]
             
print_cols = ['Chemical',
              'Units',
              'N',
              '%detect',
              'Min',
              'Max',
              'Median',
              'Mean']

# Perform data formatting on each group of data
for group in group_list:
    print('Formatting data for %s' % group)
    # Compile data for all pollutants
    for index, (chemname, unit1, unit2, conv) in enumerate(chem_list):
        infname = 'converted\\{0}_OS_{1}_conv.csv'.format(chemname, group)
        data = pd.read_csv(infname)
        data['Units'] = unit2
        if index == 0: 
            groupdata = data
        else:
            groupdata = pd.concat([groupdata, data])

    # Retrieve units from units file and reconcile any missing units
    groupdata = groupdata.rename(columns = {groupdata.columns.values[0]: 'Chemical'})
    
    # Check to see if there are any values (other than 'Y' or 'YY') that marks min/median detects
    print("\tValues for 'IsMinDetect' in {0}: {1}".format(group, groupdata['IsMinDetect'].unique()))
    print("\tValues for 'IsMedianDetect' in {0}: {1}".format(group, groupdata['IsMedianDetect'].unique()))
    
    # Format Min and Median Values
    groupdata = formatValues(groupdata, 'Min', 'IsMinDetect')
    groupdata = formatValues(groupdata, 'Median', 'IsMedianDetect')
    
    # Format group statistics based on presence of detect (i.e., N)
    groupdata = formatValues2(groupdata)

    # Calculate percent detected
    groupdata['%detect'] = groupdata['Detect']/groupdata['N']*100
    idx = groupdata['%detect'].notnull()    
    groupdata['%detect'][idx] = groupdata['%detect'][idx].apply(lambda x: '{0:.0f}%'.format(x))

    # Output data
    groupdata[print_cols].to_excel('GroupedData_Chems_%s_Converted.xlsx' % group,
                                   index = False)
    
    