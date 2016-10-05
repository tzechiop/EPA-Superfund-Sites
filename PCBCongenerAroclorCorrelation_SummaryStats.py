# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 10:41:11 2016

@author: thasegawa
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

maindir = r"C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek"
outdir = r"C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek\CongenerAroclorCorrelation"

os.chdir(maindir)

aroclor_list = ['1016[c]',
                '1242[d]',
                '1248[e]',
                '1248[f]',
                '1254 “Late”',
                '1254[h]',
                '1260[i]']

# Read CSO data
data = pd.read_excel("DEP_CSO_Censured_Stat_Table_For Manuscript.xlsx",
                     sheetname = 'OS_ROS_stats')
wts = pd.read_excel("Table 4-5 - PCB Congener Compositions in Aroclors.xlsx")

# Specify data columns
measurecol = 'GeoMean'

# Filter data
data = data[(data['N'] > 0) & (data['Parameter'].str.contains('PCB'))]

# Recalculate Frame Weight percents
joined = pd.merge(data, wts, left_on = 'Parameter', right_on = 'PCB')
for aroclor in aroclor_list:
    totwt = joined[aroclor].sum()
    joined[aroclor] = joined[aroclor].apply(lambda x: x/totwt*100)    
wts = joined[['PCB'] + aroclor_list]    


R2_list = []
p_list = []
# Plot XY Scatter for each Aroclor
for aroclor in aroclor_list:
    plotdata = pd.merge(data, wts[wts[aroclor].notnull()], left_on = 'Parameter', right_on = 'PCB')
    
    # Calculate mass fractions
    TPCB = plotdata[measurecol].sum()
    plotdata['Mass Fraction'] = plotdata[measurecol].apply(lambda x: x/TPCB*100)
    
    for index, plottype in enumerate(['Log', 'Linear']):
        xdata = plotdata[aroclor]
        ydata = plotdata['Mass Fraction']
        plt.scatter(xdata,
                    ydata)
        
        ax = plt.gca()
        
        # Set axis limits        
        if plottype == 'Log':
            minval = min(list(xdata[xdata > 0]) + list(ydata[ydata > 0]))
            axismin = 10**np.floor(np.log10(minval))
            ax.set_ylim(axismin, 100)       
            ax.set_xlim(axismin, 100)   
                        
            ax.set_xscale("log", nonposx='clip')
            ax.set_yscale("log", nonposy='clip')
        else:
            axismin = -0.5
            axismax = max([ax.get_xlim()[1], ax.get_ylim()[1]])
            ax.set_ylim(axismin, axismax)       
            ax.set_xlim(axismin, axismax)   

        # Add 1:1 line
        axismax = max([ax.get_ylim()[1], ax.get_xlim()[1]])        
        plt.plot([0, axismax], [0, axismax], c = 'r')
        
        # Find R^2 and p-values
        pearson = pearsonr(xdata, ydata)
        txt = 'R-squared: {0:.3f}'.format(pearson[0])
        txt += '\n'
         if pearson[1] < 0.01:
            txt += 'p-value: {0:.3e}'.format(pearson[1])
        else:
            txt += 'p-value: {0:.2f}'.format(pearson[1])
        
        if plottype == 'Log':
            plt.text(axismin*2, 20, txt)
        else:
            plt.text(3, 10, txt)
        
        # Set axis labels and title
        ax.set_ylabel('Sample Mass Fractions')
        ax.set_xlabel('Aroclor {0} Normalized Percent Weights'.format(aroclor))
        ax.set_title('Mass Fraction Correlation for Geometric Mean of NYC DEP Samples', y=1.03)
        
        # Save figure
        outfname = 'MassFractionCorrelation_GeoMean_{0}{1}_{2}.pdf'.format(index, plottype, aroclor)
        fig = ax.get_figure();
        fig.savefig(os.path.join(outdir, outfname), bbox_inches='tight')
        #fig.savefig(os.path.join(outdir, outfname))
        plt.clf()
        
    # Record correlation values
    R2_list.append(pearson[0])
    p_list.append(pearson[1])

report = pd.DataFrame({'Aroclor': aroclor_list,
                       'R^2':     R2_list,
                       'p-value': p_list})
    
#report.to_excel('report.xlsx',
#                index = False)