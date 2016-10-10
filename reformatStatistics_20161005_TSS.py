# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 09:39:35 2016

@author: thasegawa
"""

import os
import pandas as pd


# Specify inputs
path = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek\Reformat Statistics 20161005'
infname = 'DEP_conv_cast_data.xlsx'

# Specify relevant parameters
valcol_list = ['TSS', 'DOC', 'POC', '% POC']
unitcol_list = {'TSS': 'mg/L',
                'POC': 'mg/L',
                'DOC': 'mg/L',
                '% POC': '%'}
ID2_list = ['NTC CSO', 'GOW CSO']
ID3_list = ['All CSO', 'All WWTP']
outcols = ['Chemical', 'Units', 'Count', 'Min', 'Max', 'Median', 'Mean']
# Read data
os.chdir(path)
data = pd.read_excel(infname)

# Calculate N, %detect, Min, Max, Median, and Mean
for ID2 in ID2_list:
    subdata = pd.DataFrame(data.groupby('ID2').count()[valcol_list].transpose()[ID2])
    subdata.columns = ['Count']
    subdata['Min'] = data.groupby('ID2').min()[valcol_list].transpose()[ID2]
    subdata['Max'] = data.groupby('ID2').max()[valcol_list].transpose()[ID2]
    subdata['Median'] = data.groupby('ID2').median()[valcol_list].transpose()[ID2]
    subdata['Mean'] = data.groupby('ID2').mean()[valcol_list].transpose()[ID2]
    subdata['Chemical'] = subdata.index
    subdata['Units'] = subdata['Chemical'].map(unitcol_list)
    subdata[outcols].to_excel('GroupedData_Conv_%s.xlsx' % ID2, index = False)
    
for ID3 in ID3_list:
    subdata = pd.DataFrame(data.groupby('ID3').count()[valcol_list].transpose()[ID3])
    subdata.columns = ['Count']
    subdata['Min'] = data.groupby('ID3').min()[valcol_list].transpose()[ID3]
    subdata['Max'] = data.groupby('ID3').max()[valcol_list].transpose()[ID3]
    subdata['Median'] = data.groupby('ID3').median()[valcol_list].transpose()[ID3]
    subdata['Mean'] = data.groupby('ID3').mean()[valcol_list].transpose()[ID3]
    subdata['Chemical'] = subdata.index
    subdata['Units'] = subdata['Chemical'].map(unitcol_list)
    subdata[outcols].to_excel('GroupedData_Conv_%s.xlsx' % ID3, index = False)