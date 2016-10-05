# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 15:12:19 2016

@author: thasegawa
"""

import os
import pandas as pd
import numpy as np

def calculateStatistics(subdata, column):
    series = subdata[column]
    count_val = series.count()
    nd_val = series.isnull().sum()
    min_val = series.min()
    max_val = series.max()
    mean_val = series.mean()
    std_val = series.std()
    median_val = series.median()
    geomean_val = series.prod()**(1/series.count())
    
    return (count_val, nd_val, min_val, max_val, mean_val, std_val, median_val, geomean_val)

def calculateStatistics_All(subdata, columns, chemical_columns, chemical, units):
    phase_list = []
    chem_list = []
    count_list = []
    nd_list = []
    min_list = []
    max_list = []
    mean_list = []
    std_list = []
    median_list = []
    geomean_list = []
    for phase in ['Dissolved', 'Solids', 'Whole Water', '% Dissolved', 'Particulates']:
        subdata2 = subdata[subdata['Phase'] == phase]
        phase_list += [phase]*len(chemical_columns)
        for chemical_column in chemical_columns:
            [count_val, nd_val, min_val, max_val, mean_val, std_val, median_val, geomean_val] = calculateStatistics(subdata2, chemical_column)
            chem_list.append(chemical_column)
            count_list.append(count_val)
            nd_list.append(nd_val)
            min_list.append(min_val)
            max_list.append(max_val)
            mean_list.append(mean_val)
            std_list.append(std_val)
            median_list.append(median_val)
            geomean_list.append(geomean_val)

    output = pd.DataFrame({'Phase': phase_list,
                           'Grouping': [chemical]*len(phase_list),
                           'Parameter': chem_list,
                           'Units': [units]*len(phase_list),
                           'N': count_list,
                           'ND': nd_list,
                           'Min': min_list,
                           'Max': max_list,
                           'Mean': mean_list,
                           'Std Dev': std_list,
                           'Median': median_list,
                           'GeoMean': geomean_list})
    output = output[columns]
    return output

maindir = r"C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek\Summary Stats"
os.chdir(maindir)

# Read data
chemical_list = [['TSS',            # chemical Name
                  'TSS-POC-DOC',    # sheet name
                  'TSS (mg/L)',     # column name
                  'mg/L',           # units (solids are always mg/kg)
                  False],           # phases (False if no phase filter needed)
                 ['TPAH',
                  'TPAH',
                  'TPAH',
                  'ng/L',
                  ['Whole Water', 'On Solids']],
                 ['TPCB',
                  'TPCB',
                  'TPCB (SumCongeners)',
                  'pg/L',
                  ['Whole Water', 'On Solids']],
                 ['Copper',
                  'Metals-DRO-GRO',
                  'COPPER',
                  'ug/L',
                  ['Whole Water', 'On Solids']],
                 ['Lead',
                  'Metals-DRO-GRO',
                  'LEAD',
                  'ug/L',
                  ['Whole Water', 'On Solids']],
                 ['Mercury',
                  'Metals-DRO-GRO',
                  'MERCURY',
                  'ng/L',
                  ['Whole Water', 'On Solids']]]
chemical = 'PCB'
units = 'pg/L'
suffix = 'v3'
data = pd.read_excel(os.path.join(maindir, 'data_{0}_{1}.xlsx'.format(chemical, suffix)))

bigCSO_list = ["NCB-083", "NCQ-077", "NCB-015", "BB-026"]

# Declare columns
columns = ['Phase',
           'Grouping',
           'Parameter',
           'Units',
           'N',
           'ND',
           'Min',
           'Max',
           'Mean',
           'Std Dev',
           'Median',
           'GeoMean']
chemical_columns = data.columns.values[8:]

# Calculate statistics for big CSOs
subdata = data[data['Location'].isin(bigCSO_list)]    
bigCSOs = calculateStatistics_All(subdata, columns, chemical_columns, chemical, units)
bigCSOs.to_excel('stats_bigCSOs_{0}_{1}.xlsx'.format(chemical, suffix))

# Calculate statistics for small CSOs
subdata = data[(~data['Location'].isin(bigCSO_list)) & (data['LocType'] == 'CSO')]    
smallCSOs = calculateStatistics_All(subdata, columns, chemical_columns, chemical, units)
smallCSOs.to_excel('stats_smallCSOs_{0}_{1}.xlsx'.format(chemical, suffix))

# Calculate statistics for all CSOs
subdata = data[data['LocType'] == 'CSO']    
allCSOs = calculateStatistics_All(subdata, columns, chemical_columns, chemical, units)
allCSOs.to_excel('stats_allCSOs_{0}_{1}.xlsx'.format(chemical, suffix))

# Calculate statistics for all WWTPs
subdata = data[data['LocType'] == 'WWTP']    
allWWTPs = calculateStatistics_All(subdata, columns, chemical_columns, chemical, units)
allWWTPs.to_excel('stats_WWTPs_{0}_{1}.xlsx'.format(chemical, suffix))