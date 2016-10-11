# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 14:38:33 2016

@author: thasegawa
"""

import os
import pandas as pd
from bootstrap import bootstrap
import numpy as np
from scipy import stats

maindir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek\Bootstrap_20161004'
#fname = 'Book1.xlsx'
#sheetname = 'Sheet2'
fname = 'anova.analysis.csv'

# Read main data file
os.chdir(maindir)
#fulldat = pd.read_excel(fname, sheetname)
fulldat = pd.read_csv(fname)

#chem_cols = fulldat.columns.values[6:]
#chem_cols = ['TPAH16/TOC',
#             'TPAH17/TOC']
#chem_cols = ['TPAH16']
       
chem_cols = ['TPAH16',
             'TPCB',
             'Copper',
             'Lead',
             'TOC.pct',
             'BC.pct',
             'Al.pct']

#filtcol = 'type'
filtcol = 'Category'
filt_list = fulldat[filtcol].unique()
filt_list = [filt for filt in filt_list if type(filt) in [str, 'unicode']]
filt_list = sorted(filt_list)

col_list = ['Waterbody',
            'Chemical',
            'N',
            'Actual Mean',
            'Std. Dev.',
            'Actual Median',
            'Min',
            'Max',
            '2.5 (Median)',
            '5 (Median)',
            '95 (Median)',
            '97.5 (Median)',
            '2.5 (Mean)',
            '5 (Mean)',
            '95 (Mean)',
            '97.5 (Mean)']
percentiles_all = pd.DataFrame([], columns = col_list)

#==============================================================================
# for chem in chem_cols:
#     print(chem)
#     values = fulldat[chem]
#     values = values[values.notnull()]
#     percentile_dict = bootstrap(values,
#                                 samplenum = 10000,
#                                 percentile_list = [2.5, 5, 95, 97.5])
#                                 
#     #percentile_dict['Chemical'] = chem
#     #percentile_dict['Waterbody'] = filt
#     percentile_dict['N'] = len(values.index)
#     percentile_dict['Actual Mean'] = np.mean(values)
#     percentile_dict['Std. Dev.'] = np.std(values)
#     percentile_dict['Actual Median'] = stats.scoreatpercentile(values, 50)
#     percentile_dict['Min'] = np.min(values)
#     percentile_dict['Max'] = np.max(values)
#     
#     percentiles_all = percentiles_all.append(pd.DataFrame(percentile_dict, index = [0]), ignore_index = True)
#==============================================================================
        
for chem in chem_cols:
    print(chem)
    for filt in filt_list:
        print(filt)
        values = fulldat[(fulldat[filtcol] == filt)][chem]
        values = values[values.notnull()]
        percentile_dict = bootstrap(values,
                                    samplenum = 10000,
                                    percentile_list = [2.5, 97.5])
                                    
        percentile_dict['Chemical'] = chem
        percentile_dict['Waterbody'] = filt
        percentile_dict['N'] = len(values.index)
        percentile_dict['Actual Mean'] = np.mean(values)
        percentile_dict['Std. Dev.'] = np.std(values)
        percentile_dict['Actual Median'] = stats.scoreatpercentile(values, 50)
        percentile_dict['Min'] = np.min(values)
        percentile_dict['Max'] = np.max(values)
        
        percentiles_all = percentiles_all.append(pd.DataFrame(percentile_dict, index = [0]), ignore_index = True)

percentiles_all = percentiles_all[col_list]
percentiles_all.to_excel('GW_Bootstrap_All_20161011.xlsx')

#==============================================================================
# # Compile tables
# file_list_main = os.listdir()
# 
# file_list = [fname for fname in file_list_main if '_Colocates_Means_v3' in fname]
# for index, fname in enumerate(file_list):
#     df = pd.read_excel(fname)
#     df.columns = [fname.split('_')[-1].split('.')[0]]
#     if index == 0:
#         alldf = df
#     else:
#         alldf = pd.concat([alldf, df], axis = 1)
# alldf.to_excel('GW_Bootstrap_Bootstrapped_20160901_Means.xlsx')
# 
# file_list = [fname for fname in file_list_main if '_Colocates_Medians_v3' in fname]
# for index, fname in enumerate(file_list):
#     df = pd.read_excel(fname)
#     df.columns = [fname.split('_')[-1].split('.')[0]]
#     if index == 0:
#         alldf = df
#     else:
#         alldf = pd.concat([alldf, df], axis = 1)
# alldf.to_excel('GW_Bootstrap_Bootstrapped_20160901.xlsx')
#==============================================================================
