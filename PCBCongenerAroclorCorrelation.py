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

# Read CSO data
#data = pd.read_excel("NYCDEP - Newtown Creek Wet Weather CSO & WWTP Data by Analyte Grouping_V2.xlsx",
#                     sheetname = 'TPCB')
data = pd.read_excel("DEP_CSO_Censured_Stat_Table_For Manuscript.xlsx",
                     sheetname = 'OS_ROS_stats')
wts = pd.read_excel("Table 4-5 - PCB Congener Compositions in Aroclors.xlsx")

aroclor_list = ['1016[c]',
                '1242[d]',
                '1248[e]',
                '1248[f]',
                '1254 “Late”',
                '1254[h]',
                '1260[i]']
                
# Filter data
#data = data[(data['Type'] == 'CSO') & (data['Phase'] == 'Whole Water')]
data = data[(data['N'] > 0) & (data['Parameter'].str.contains('PCB'))]

# Perform correlation for each sample ID
data['sampleid'] = data.apply(lambda x: '{0} ({1})'.format(x['Location'], x['Event']), axis = 1)
sampleid_list = list(data['sampleid'])

PCBcol_list = [column for column in data.columns.values if 'PCB' in column]

for sampleid in sampleid_list[:1]:
    # Retrieve data for sample
    PCBvals = data[PCBcol_list].loc[data['sampleid'] == sampleid].transpose()
    PCBvals.columns = ['Measurement']
    PCBvals['PCB'] = PCBvals.index
    
    # Remove NaNs
    PCBvals = PCBvals[PCBvals['Measurement'].notnull()]
    
    # Join Frame weights and sample mass fractions
    joined = pd.merge(PCBvals[['Measurement', 'PCB']], wts, on = 'PCB')
    
    # Plot XY Scatter for each Aroclor
    for aroclor in aroclor_list:
        plotdata = joined[(joined['Measurement'].notnull()) & (joined[aroclor].notnull())]
        
        # Calculate mass fractions
        TPCB = plotdata['Measurement'].sum()
        plotdata['Mass Fraction'] = plotdata['Measurement'].apply(lambda x: x/TPCB*100)
        
        for plottype in ['Log', 'Linear']:
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
    
            # Add 1:1 line
            axismax = max([ax.get_ylim()[1], ax.get_xlim()[1]])        
            plt.plot([0, axismax], [0, axismax], c = 'r')
            
            # Find R^2 and p-values
            pearson = pearsonr(xdata, ydata)
            txt = 'R-squared: {0:.3f}'.format(pearson[0])
            txt += '\n'
            txt += 'p-value: {0:.3e}'.format(pearson[1])
            plt.text(axismin*5, 10, txt)
            
            # Set axis labels and title
            ax.set_ylabel('Sample Mass Fractions')
            ax.set_xlabel('Aroclor {0} Percent Weights'.format(aroclor))
            ax.set_title('Mass Fraction Correlation for {0}'.format(sampleid))
            
            # Save figure
            outfname = 'MassFractionCorrelation_v2_{0}_{1}_{2}.pdf'.format(plottype, sampleid, aroclor)
            fig = ax.get_figure();
            fig.savefig(os.path.join(outdir, outfname), bbox_inches='tight')
            plt.clf()
            
            
        