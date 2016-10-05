# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 11:12:27 2016

@author: thasegawa
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create LocCode column based on sample_code
def createLocCode(sample_code):
    return sample_code[:2]
    
# Create Depth columns based on task_name
def createDepth(task_name):
    if 'Subsurface' in task_name:
        depth  = 'Subsurface'
    else:
        depth = 'Surface'
    return depth
    
# Stagger x indices
def staggerX(x, stagger = 0.10):
    newx = np.random.normal(x, stagger, size = 1)[0]
    return newx
    
# Get location from "Location" column in solids data
def getCSOLocation(location):
    newlocation = location.split(" ")[0]
    return newlocation

maindir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek\PCB-11 Plot'
os.chdir(maindir)

# Create dictionaries
location_dict = {'DK': 'Dutch Kills',
                 'EB': 'East Branch',
                 'EK': 'English Kills',
                 'GC': 'Gerritsen Creek',
                 'HB': 'Head of Bay',
                 'MC': 'Maspeth Creek',
                 'NC': 'Newtown Creek',
                 'SP': 'Spring Creek',
                 'WC': 'Whale Creek',
                 'WE': 'Westchester Creek'}
type_dict = {'DK': 'Newtown Creek (NCG-Phase 1&2)',
             'EB': 'Newtown Creek (NCG-Phase 1&2)',
             'EK': 'Newtown Creek (NCG-Phase 1&2)',
             'GC': 'CSO Waterbodies (NCG)',
             'HB': 'CSO Waterbodies (NCG)',
             'MC': 'Newtown Creek (NCG-Phase 1&2)',
             'NC': 'Newtown Creek (NCG-Phase 1&2)',
             'SP': 'CSO Waterbodies (NCG)',
             'WC': 'Newtown Creek (NCG-Phase 1&2)',
             'WE': 'CSO Waterbodies (NCG)'}
x_dict = {'CSO-Solids': 1,
          'Dutch Kills': 6,
          'East Branch': 7,
          'English Kills': 8,
          'Gerritsen Creek': 2,
          'Head of Bay': 3,
          'Maspeth Creek': 9,
          'Newtown Creek': 10,
          'Spring Creek': 4,
          'Whale Creek': 11,
          'Westchester Creek': 5}
#color_dict = {'Solids': 'r',
#              'Surface': 'r',
#              'Subsurface': 'r'}
marker_dict = {'CSO': 'o',
               'Phase 1': '+',
               'Phase 2': 'x'}
color_dict = {'CSO': 'r',
              'Phase 1': 'g',
              'Phase 2': 'b'}
xtick_labels = [loc for val in range(len(x_dict)) for loc in x_dict if x_dict[loc] == val]

# Read in and clean solids data
solidsdata = pd.read_excel('PCB11_Pointsources.xlsx')
solidsdata = solidsdata[solidsdata['Type'] == 'CSO']
solidsdata = solidsdata[['#sys_sample_code',
                         'PCB11 ng/kg',
                         'PCB11/TPCB']]
solidsdata.columns = ['sample_code',
                      'PCB-11 (ng/kg)',
                      'PCB11/TPCB']
solidsdata['Location'] = 'CSO-Solids'
solidsdata['Type'] = 'Solids\n(NYC-DEP)'      
solidsdata['Depth'] = 'Solids'                     
solidsdata['Phase'] = 'CSO'
                      
# Read in Phase 1 Surface
phase1data_surface = pd.read_excel('PCB 11 Sediments Data_v2.xlsx',
                           sheetname = 'Ph1 Surface Sed')
phase1data_surface = phase1data_surface[['Row Labels',
                                         'PCB-011 (ng/kg)',
                                         'PCB11/TPCB']]
phase1data_surface.columns = ['sample_code',
                              'PCB-11 (ng/kg)',
                              'PCB11/TPCB']
phase1data_surface['LocCode'] = phase1data_surface['sample_code'].map(createLocCode)
phase1data_surface['Location'] = phase1data_surface['LocCode'].map(location_dict)
phase1data_surface['Type'] = phase1data_surface['LocCode'].map(type_dict)
phase1data_surface['Depth'] = 'Surface'
phase1data_surface['Phase'] = 'Phase 1'
phase1data_surface = phase1data_surface.drop('LocCode', 1)

# Read in Phase 1 Subsurface Data
phase1data_subsurface = pd.read_excel('PCB 11 Sediments Data_v2.xlsx',
                                      sheetname = 'Ph1 SubSurface Sed',
                                      skiprows = 2)
phase1data_subsurface = phase1data_subsurface[['sys_loc_code',
                                               'PCB-011 (ng/kg)',
                                               'PCB11/TPCB']]
phase1data_subsurface.columns = ['sample_code',
                                 'PCB-11 (ng/kg)',
                                 'PCB11/TPCB']
phase1data_subsurface['LocCode'] = phase1data_subsurface['sample_code'].map(createLocCode)
phase1data_subsurface['Location'] = phase1data_subsurface['LocCode'].map(location_dict)
phase1data_subsurface['Type'] = phase1data_subsurface['LocCode'].map(type_dict)
phase1data_subsurface['Depth'] = 'Subsurface'
phase1data_subsurface['Phase'] = 'Phase 1'
phase1data_subsurface = phase1data_subsurface.drop('LocCode', 1)

# Read in Phase 2 Surface and Subsurface Data
phase2data = pd.read_excel('PCB 11 Sediments Data_v2.xlsx',
                           sheetname = 'Sheet3',
                           skiprows = 1)
phase2data = phase2data[['sys_loc_code',
                         'subfacility_code',
                         'task_name',
                         'PCB-011 (ng/kg)',
                         'PCB11/TPCB']]
phase2data.columns = ['sample_code',
                      'Location',
                      'task_name',
                      'PCB-11 (ng/kg)',
                      'PCB11/TPCB']
phase2data['LocCode'] = phase2data['sample_code'].map(createLocCode)
phase2data['Type'] = phase2data['LocCode'].map(type_dict)
phase2data['Depth'] = phase2data['task_name'].map(createDepth)
phase2data['Phase'] = 'Phase 2'
phase2data = phase2data.drop(['LocCode', 'task_name'], 1)

# Combine data and create label column
frames = [solidsdata, phase1data_surface, phase1data_subsurface, phase2data]
data = pd.concat(frames)
data['Label'] = data['Phase'] + ' - ' + data['Depth']

# Create X indices
data['x'] = data['Location'].map(x_dict)
data['x_stagger'] = data['x'].map(staggerX)

# Define color and marker
data['Color'] = data['Phase'].map(color_dict)
data['Marker'] = data['Phase'].map(marker_dict)

# Remove subsurface
data = data[data['Depth'] != 'Subsurface']


#===============================
labelCol = 'Phase'
# Create scatter plot
ax = data.boxplot(column = 'PCB-11 (ng/kg)',
                  by = 'x',
                  showfliers = False)
ax.grid(zorder=0)
zorder_dict = {'CSO': 3,
               'Phase 1': 6,
               'Phase 2': 3}
for label in data[labelCol].unique():    
    indices = data[labelCol] == label
    plotdata = data[indices]
    marker = plotdata['Marker'].iloc[0]
    zorder = zorder_dict[label]
    plt.scatter(plotdata['x_stagger'],
                plotdata['PCB-11 (ng/kg)'],
                c = plotdata['Color'].tolist(),  
                marker = marker,          
                s = 40,
                label = label,
                zorder = zorder)
                
# Create legend
lgd = plt.legend(bbox_to_anchor=(1.02, 1),
                 loc=2,
                 borderaxespad=0.)
plt.xticks(range(1, len(xtick_labels) + 1), xtick_labels, rotation = 90)

ax = plt.gca()  

# Set y -limits
ymin, ymax = ax.get_ylim()
ax.set_ylim(0, ymax)        

# Set axis titles and remove axes title
title = 'PCB-11 Sample Measurements'
ax.set_title(title)       
ax.set_ylabel('Concentration (ng/kg)')
ax.set_xlabel('Location')

# Save figure to pdf
outname = 'PCB-11ScatterPlot_20160621_v1.pdf' 
fig = ax.get_figure();
fig.suptitle('')
fig.savefig(outname, bbox_extra_artists=(lgd,), bbox_inches='tight')

# ====================================================
# Plot PCB-11/TPCB Ratio
# Create scatter plot
ax = data.boxplot(column = 'PCB11/TPCB',
                  by = 'x',
                  showfliers = False)
ax.grid(zorder=0)
zorder_dict = {'CSO': 3,
               'Phase 1': 6,
               'Phase 2': 3}
for label in data[labelCol].unique():      
    indices = data[labelCol] == label
    plotdata = data[indices]
    marker = plotdata['Marker'].iloc[0]
    zorder = zorder_dict[label]
    plt.scatter(plotdata['x_stagger'],
                plotdata['PCB11/TPCB'],
                c = plotdata['Color'].tolist(),  
                marker = marker,          
                s = 40,
                label = label,
                zorder = zorder)
                
# Create legend
lgd = plt.legend(bbox_to_anchor=(1.02, 1),
                 loc=2,
                 borderaxespad=0.)
plt.xticks(range(1, len(xtick_labels) + 1), xtick_labels, rotation = 90)

ax = plt.gca()  

# Set y -limits
ymin, ymax = ax.get_ylim()
#ax.set_ylim(0, ymax)        
ax.set_yscale("log", nonposy='clip')
ax.set_ylim(10**(-5), 10**(0))  

# Set axis titles and remove axes title
title = 'PCB-11/TPCB Ratios'
ax.set_title(title)       
ax.set_ylabel('PCB-11/TPCB')
ax.set_xlabel('Location')

# Save figure to pdf
outname = 'PCB-11_TPCB_ScatterPlot_20160621_v2.pdf' 
fig = ax.get_figure();
fig.suptitle('')
fig.savefig(outname, bbox_extra_artists=(lgd,), bbox_inches='tight')

# ==============================================================================

# Create Scatter plot (CSOs only)
solidsdata = pd.read_excel('PCB11_Pointsources.xlsx')
solidsdata = solidsdata[solidsdata['Type'] == 'CSO']
solidsdata['Location'] = solidsdata['Location'].map(getCSOLocation)
solidsdata = solidsdata[['Location',
                         'PCB11 ng/kg',
                         'PCB11/TPCB']]

# Set x index
loc_list = np.sort(solidsdata['Location'].unique())
loc_dict = {loc_list[i]: i+1 for i in range((len(loc_list)))}
solidsdata['x'] = solidsdata['Location'].map(loc_dict)
solidsdata['x_stagger'] = solidsdata['x'].map(lambda x: staggerX(x, 0.04))

# Plot data
ax = solidsdata.boxplot(column = 'PCB11 ng/kg',
                        by = 'x',
                        showfliers = False)
ax.grid(zorder=0)
plt.scatter(solidsdata['x_stagger'],
            solidsdata['PCB11 ng/kg'],  
            s = 40,
            zorder = 3)

# Set x ticks
plt.xticks(range(1, len(loc_list) + 1), loc_list, rotation = 90)

# Set y -limits
ymin, ymax = ax.get_ylim()
ax.set_ylim(0, ymax)        

# Set axis titles and remove axes title
title = 'PCB-11 Sample Measurements for CSO Solids'
ax.set_title(title)       
ax.set_ylabel('Concentration (ng/kg)')
ax.set_xlabel('Location')

# Save figure to pdf
outname = 'PCB-11ScatterPlot_CSOSolids_20160621_v1.pdf' 
fig = ax.get_figure();
fig.suptitle('')
fig.savefig(outname, bbox_inches='tight')

#====================================================================================
# Plot PCB-11/TPCB
# Create Scatter plot (CSOs only)
solidsdata = pd.read_excel('PCB11_Pointsources.xlsx')
solidsdata = solidsdata[solidsdata['Type'] == 'CSO']
solidsdata['Location'] = solidsdata['Location'].map(getCSOLocation)
solidsdata = solidsdata[['Location',
                         'PCB11 ng/kg',
                         'PCB11/TPCB']]

# Set x index
loc_list = np.sort(solidsdata['Location'].unique())
loc_dict = {loc_list[i]: i + 1 for i in range((len(loc_list)))}
solidsdata['x'] = solidsdata['Location'].map(loc_dict)
solidsdata['x_stagger'] = solidsdata['x'].map(lambda x: staggerX(x, 0.04))

# Create scatter plot
ax = solidsdata.boxplot(column = 'PCB11/TPCB',
                        by = 'x',
                        showfliers = False)
ax.grid(zorder=0)
plt.scatter(solidsdata['x_stagger'],
            solidsdata['PCB11/TPCB'],  
            s = 40,
            zorder = 3)
            
# Set x ticks
plt.xticks(range(1, len(loc_list) + 1), loc_list, rotation = 90)

# Set y -limits
ymin, ymax = ax.get_ylim()
ax.set_yscale("log", nonposy='clip')
ax.set_ylim(10**(-3), 10**(0))        
     

# Set axis titles and remove axes title
title = 'PCB-11/TPCB Ratios for CSO Solids'
ax.set_title(title)       
ax.set_ylabel('PCB-11/TPCB')
ax.set_xlabel('Location')

# Save figure to pdf
outname = 'PCB-11_TPCB_ScatterPlot_CSOSolids_20160621_v2.pdf' 
fig = ax.get_figure();
fig.suptitle('')
fig.savefig(outname, bbox_inches='tight')