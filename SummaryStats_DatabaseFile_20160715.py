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
    geostd_val = np.exp((series.apply(lambda x: np.log(x/geomean_val)**2).sum()/count_val)**0.5)
    
    return (count_val, nd_val, min_val, max_val, mean_val, std_val, median_val, geomean_val, geostd_val)

def calculateStatistics_All(subdata, datacol, chemical_columns, chemical, units, columns):
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
    geostd_list = []
    for phase in ['Dissolved', 'Solids', 'Whole Water', '% Dissolved', 'Particulates']:
        subdata2 = subdata[subdata['Phase'] == phase]
        phase_list += [phase]*len(chemical_columns)
        for chemical_column in chemical_columns:
            [count_val, nd_val, min_val, max_val, mean_val, std_val, median_val, geomean_val, geostd_val] = calculateStatistics(subdata2, chemical_column)
            chem_list.append(chemical_column)
            count_list.append(count_val)
            nd_list.append(nd_val)
            min_list.append(min_val)
            max_list.append(max_val)
            mean_list.append(mean_val)
            std_list.append(std_val)
            median_list.append(median_val)
            geomean_list.append(geomean_val)
            geostd_list.append(geomean_val)

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
                           'GeoMean': geomean_list,
                           'GeoStd': geostd_list})
    output = output[columns]
    return output
    
def calculateappend(subdata, chemical, group, phase, units, datacol, all_lists):
    # Calculate statistics for all CSOs
    [count_val, nd_val, min_val, max_val, mean_val, std_val, median_val, geomean_val, geostd_val] = calculateStatistics(subdata, datacol)
    
    all_lists['Chemical'].append(chemical)
    all_lists['Sample Group'].append(group)
    all_lists['Phase'].append(phase)
    all_lists['Count'].append(count_val)
    all_lists['ND'].append(nd_val)
    all_lists['Min'].append(min_val)
    all_lists['Max'].append(max_val)
    all_lists['Mean'].append(mean_val)
    all_lists['St Dev'].append(std_val)
    all_lists['Median'].append(median_val)
    all_lists['Geo Mean'].append(geomean_val)
    all_lists['Geo Std'].append(geostd_val)
    
    return all_lists
    
def calculateGroups(data, chemical, phase, units, datacol, all_lists):
    for group in ['All CSOs', 'Big CSOs', 'Small CSOs', 'WWTPs']:
        if group == 'All CSOs':
            subdata = data[(data['Type'] == 'CSO')] 
            all_lists = calculateappend(subdata, chemical, group, phase, units, datacol, all_lists)
        elif group == 'Big CSOs':
            subdata = data[(data['Type'] == 'CSO') & (data['Location'].isin(bigCSO_list))]                          
            all_lists = calculateappend(subdata, chemical, group, phase, units, datacol, all_lists)
        elif group == 'Small CSOs':
            subdata = data[(data['Type'] == 'CSO') & (~data['Location'].isin(bigCSO_list))]                          
            all_lists = calculateappend(subdata, chemical, group, phase, units, datacol, all_lists)
        else:
            subdata = data[(data['Type'] == 'WWTP') & (data['Event'].str.contains('NTC'))]                          
            all_lists = calculateappend(subdata, chemical, group, phase, units, datacol, all_lists)
    
    return all_lists
    
def calculatePhases(data, chemical, phase_list, units, datacol, all_lists, phasecol = 'Phase'):
    for phase in phase_list:
        subdata = data[data[phasecol] == phase]
        if phase == 'On Solids':
            realunits = 'mg/kg'
        else:
            realunits = units
            
        all_lists = calculateGroups(subdata, chemical, phase, realunits, datacol, all_lists)
    
    return all_lists

# =============================================================================

# I/O parameters
maindir = r"C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek"
os.chdir(maindir)
infile = 'NYCDEP - Newtown Creek Wet Weather CSO  WWTP Data by Analyte Grouping_V3.xlsx'

outdir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek\Summary Stats'
suffix = '20160728'
outfile = 'SummaryStats_RemovedOutlier_TSS_{0}.xlsx'.format(suffix)

bigCSO_list = ["NCB-083", "NCQ-077", "NCB-015", "BB-026"]

# Read data
#==============================================================================
# chemical_list = [['TSS',            # chemical Name
#                   'TSS-POC-DOC',    # sheet name
#                   'TSS (mg/L)',     # column name
#                   'mg/L',           # units (solids are always mg/kg)
#                   False],           # phases (False if no phase filter needed)
#                  ['TPAH',
#                   'TPAH',
#                   'TPAH',
#                   'ng/L',
#                   ['Whole Water', 'On Solids']],
#                  ['TPCB',
#                   'TPCB',
#                   'TPCB (SumCongeners)',
#                   'pg/L',
#                   ['Whole Water', 'On Solids']],
#                  ['Copper',
#                   'Metals-DRO-GRO',
#                   'COPPER',
#                   'ug/L',
#                   ['Whole Water', 'On Solids']],
#                  ['Lead',
#                   'Metals-DRO-GRO',
#                   'LEAD',
#                   'ug/L',
#                   ['Whole Water', 'On Solids']],
#                  ['Mercury',
#                   'Metals-DRO-GRO',
#                   'MERCURY',
#                   'ng/L',
#                   ['Whole Water', 'On Solids']]]
#==============================================================================

chemical_list = [['TSS',            # chemical Name
                  'TSS-POC-DOC',    # sheet name
                  'TSS (mg/L)',     # column name
                  'mg/L',           # units (solids are always mg/kg)
                  False]]

all_lists = {'Chemical': [],
             'Sample Group': [],
             'Phase': [],
             'Count': [],
             'ND': [],
             'Min': [],
             'Max': [],
             'Mean': [],
             'St Dev': [],
             'Median': [],
             'Geo Mean': [],
             'Geo Std': []}
columnorder = ['Chemical', 'Sample Group', 'Phase', 'Count', 'ND', 'Min', 'Max', 'Mean', 'St Dev', 'Median', 'Geo Mean', 'Geo Std']
for cheminfo in chemical_list:
    # Parse parameters
    chemname = cheminfo[0]
    sheetname = cheminfo[1]
    datacol = cheminfo[2]
    units = cheminfo[3]
    phase_list = cheminfo[4]
    
    # Read data
    data = pd.read_excel(infile,
                         sheetname = sheetname)

    if phase_list:
        all_lists = calculatePhases(data, chemname, phase_list, units, datacol, all_lists)
    else:
        all_lists = calculateGroups(data, chemname, '', units, datacol, all_lists)

outdata = pd.DataFrame(all_lists)[columnorder]
outdata.to_excel(os.path.join(outdir, outfile),
                 index = False)