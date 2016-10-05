# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 16:50:27 2016

@author: thasegawa
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np

# Specify data parameters
maindir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek'
outdir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek\Normality Test'
fname = 'NCG_TSS_forBootstrap.xlsx'
suffix_list = ['allCSOs', '4Large', '3Large', 'small_4Large', 'small_3Large']

os.chdir(maindir)

# Q-Q plot
for suffix in suffix_list:
    data = pd.read_excel(fname,
                         sheetname = suffix)
    stats.probplot(data['TSS mg/L'], plot = plt)
                                
    ax = plt.gca()  
    plotname = 'QQPlot_NCG_TSS_{0}.pdf'.format(suffix)
    fig = ax.get_figure();
    fig.suptitle('')
    fig.savefig(os.path.join(outdir, plotname), bbox_inches='tight')
    plt.clf()

# Q-Q plot for log values
for suffix in suffix_list:
    data = pd.read_excel(fname,
                         sheetname = suffix)
    data['log TSS'] = data['TSS mg/L'].apply(lambda x: np.log10(x))
    stats.probplot(data['log TSS'], plot = plt)
                                
    ax = plt.gca()  
    plotname = 'QQPlot_NCG_logTSS_{0}.pdf'.format(suffix)
    fig = ax.get_figure();
    fig.suptitle('')
    fig.savefig(os.path.join(outdir, plotname), bbox_inches='tight')
    plt.clf()

# Perform Normal Test
for suffix in suffix_list:
    data = pd.read_excel(fname,
                         sheetname = suffix)
    result = stats.shapiro(data['TSS mg/L'])
    print('Normality Test result for {0}: {1:.2f}'.format(suffix, result[1]))

# Perform Normal Test
for suffix in suffix_list:
    data = pd.read_excel(fname,
                         sheetname = suffix)
    data['log TSS'] = data['TSS mg/L'].apply(lambda x: np.log10(x))
    result = stats.shapiro(data['log TSS'])
    print('Normality Log  Test result for {0}: {1:.2f}'.format(suffix, result[1]))