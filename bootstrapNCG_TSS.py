# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 08:43:45 2016

@author: thasegawa
"""

import os
import pandas as pd
import numpy as np
from scipy import stats
import random

# Specify data parameters
maindir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek'
fname = 'NCG_TSS_forBootstrap.xlsx'
suffix = '4Large'

loccol = 'Loc'
colname = 'TSS mg/L'

os.chdir(maindir)

# Specify bootstrap parameters
bootstrapnum = 10000
percentilenum_list = [95, 97.5, 50, 5, 2.5]

# Read data
data = pd.read_excel(fname,
                     sheetname = suffix)

# Split analysis for datatyp
numsamples = len(data)

# Run bootstrap
bootstrapdata_list = []
mean_list = []
for index in range(bootstrapnum):
    bootstrapdata = [random.choice(list(data[colname])) for sample in range(numsamples)]
    
    bootstrapdata_list.append(bootstrapdata)
    mean_list.append(np.mean(bootstrapdata))
    
# Find percentiles
percentiledict = {}
for percentilenum in percentilenum_list:
    percentiledict[str(percentilenum)] = stats.scoreatpercentile(mean_list, percentilenum)

# Make dataframes from bootstrap data
percentiles = pd.DataFrame(percentiledict,
                           index = [0])
bootstrap = pd.DataFrame(bootstrapdata_list,
                         columns = [str(num) for num in range(numsamples)])
means = pd.DataFrame({'Mean': mean_list})

# Output data to excel file
outfname = 'NCG_TSS_Bootstrap_{0}.xlsx'.format(suffix)
writer = pd.ExcelWriter(outfname)
percentiles.to_excel(writer,
                     sheet_name = 'percentiles',
                     index = False)
bootstrap.to_excel(writer,
                   sheet_name = 'bootstrap data')
means.to_excel(writer,
               sheet_name = 'bootstrap means')
writer.save()