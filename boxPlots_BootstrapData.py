# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 12:04:41 2016

@author: thasegawa
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

path = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek\Bootstrap_20161004'
os.chdir(path)

fname_base = 'TPAH16RefAreaRatio_BootstrapMedians_R_{0}_20161012.csv'

studyarea_list = ['Canal - Lower',
                  'Canal - Middle',
                  'Canal - Upper',
                  'NTC Mainstem (No TB)',
                  'NTC Tributaries',
                  'NTC Turning Basin']
xticklabels = ['Canal -\nLower',
                  'Canal -\nMiddle',
                  'Canal -\nUpper',
                  'NTC Mainstem\n(No TB)',
                  'NTC\nTributaries',
                  'NTC\nTurning Basin']

# Read in data                    
for index, studyarea in enumerate(studyarea_list):
    newdata = pd.read_csv(fname_base.format(studyarea), header = None)
    if index == 0:
        data = newdata
        data.columns = [studyarea]
    else:
        data[studyarea] = newdata.ix[:,0]
    
# Plot data
data.boxplot()

# Set axis and title options
ax = plt.gca()  
title = 'Study Area and Reference Site Ratio for TPAH16'
ax.set_title(title)       
ax.set_ylabel('TPAH16 Ratio')
ax.set_yscale("log", nonposy='clip')
plt.xticks(range(1,len(xticklabels)+1), xticklabels, rotation = 90, ha = 'right')
                    
outname = 'StudyAreaRefSiteRatio_TPAH16.pdf'
outname = 'StudyAreaRefSiteRatio_TPAH16_log.pdf'
fig = ax.get_figure();
fig.suptitle('')
fig.savefig(outname, bbox_inches='tight')