# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 12:17:54 2016

@author: thasegawa
"""

import os
import pandas as pd
import glob

# Format min or median values based on IsMinDetect or IsMedianDetect
def formatValues(data, valcol, detectcol, qual = ['Y', 'YY'], decnum = 4):
    idx = data['Detect'] > 0
    data[valcol][idx] = data[valcol][idx].apply(lambda x: '<{0:.{1}f}'.format(x, decnum) if (type(x) != str) else x)
    idx = data[detectcol].isin(['Y','YY'])
    data[valcol][idx] = data[valcol][idx].apply(lambda x: x[1:])
    
    return data
    
# Format group statistics (i.e., min, max, median, mean) based on presence of detected samples
def formatValues2(data, decnum = 4):
    for valcol in ['Min', 'Max','Median','Mean']:
        idx = (data['Detect'] == 0) & (data['N'] > 0)
        data[valcol][idx] = data[valcol][idx].apply(lambda x: '<{0:.{1}f}'.format(x, decnum) if (type(x) != str) else x)
    
    return data


# Specify inputs
path = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek\Reformat Statistics 20161005'
infname = 'dioxs_OS_All_WW_WWTP.csv'

# Specify data parameters
group_list = ['All_WW_WWTP',
              'AllCSO',
              'GOW_CSO',
              'NTC_CSO']
              
chem_list = [('pah', 'ng/L'),
             ('pcbs', 'pg/L'),
             ('metals', 'ug/L'),
             ('pests', 'ng/L'),
             ('dioxs', 'pg/L'),
             ('vocs', 'ug/L')]
             
print_cols = ['Chemical',
              'Units',
              'N',
              '%detect',
              'Min',
              'Max',
              'Median',
              'Mean']
              
# Read units file
units = pd.read_excel('units.xlsx')
os.chdir(path)

# Perform data formatting on each group of data
for group in group_list:
    print('Formatting data for %s' % group)
    # Compile data for all pollutants
    for index, (chemname, unit) in enumerate(chem_list):
        infname = '{0}_OS_{1}.csv'.format(chemname, group)
        data = pd.read_csv(infname)
        data['Units'] = unit
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
    groupdata[print_cols].to_excel('GroupedData_%s.xlsx' % group,
                                   index = False)
    
    