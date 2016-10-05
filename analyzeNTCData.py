# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 13:54:39 2016

@author: thasegawa
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Create a LocEvent column that specifies the each sample's location, event, and phase
def createLocEventPhaseCol(data, loccol = 'Location', eventcol = 'Event', phasecol = 'ValueType', newcol = 'Loc-Event-Phase'):
    data[newcol] = data[loccol] + '_' + data[eventcol] + '_' + data[phasecol]
    return data

# Drop the TSS columns
def dropTSSColumn(data, TSScol = 'TSS (mg/L)'):
    data = data.drop(TSScol, 1)
    return data
    
# Organize columns of a dataframe after merging two raw dataframes
def organizeCols(data):
    data = data.drop('Location_y', 1)
    data = data.drop('Event_y', 1)
    data = data.drop('Type_y', 1)
    data = data.rename(columns = {'Location_x': 'Location',
                                  'Event_x': 'Event',
                                  'Type_x': 'Type'})
    return data
   
# Create box plot and print to pdf
#def printBoxPlot(data, = )

# ================================================================================

# Read data
maindir = r"C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek"
fname = "NYCDEP - Newtown Creek Point Sources All Data by Analyte Grouping_Cleaned.xlsx"

os.chdir(maindir)

events = ['WW-1',
          'WW-2',
          'WW-3',
          'WW-4',
          'WW-5',
          'WW-6',
          'WW-7',
          'WW-8',
          'WW-9',
          'WW-10',
          'WW-11',
          'WW-12',
          'WW-13',
          'WW-14',
          'WW-15',
          'WW-16',
          'WW-17']

TSSdata = pd.read_excel(os.path.join(maindir, fname),
                        sheetname = 'TSS-POC-DOC')                        
metalsdata = pd.read_excel(os.path.join(maindir, fname),
                           sheetname = 'Metals-DRO-GRO')
VOCdata = pd.read_excel(os.path.join(maindir, fname),
                        sheetname = 'VOC')
PCDDdata = pd.read_excel(os.path.join(maindir, fname),
                         sheetname = 'PCDD-PCDF')
pestdata = pd.read_excel(os.path.join(maindir, fname),
                         sheetname = 'Pesticides')
TPAHdata = pd.read_excel(os.path.join(maindir, fname),
                         sheetname = 'TPAH')
TPCBdata = pd.read_excel(os.path.join(maindir, fname),
                         sheetname = 'TPCB')
      
# Create Loc-Event column                     
#TSSdata = createLocEventPhaseCol(TSSdata)
metalsdata = createLocEventPhaseCol(metalsdata)
VOCdata = createLocEventPhaseCol(VOCdata)
PCDDdata = createLocEventPhaseCol(PCDDdata)
pestdata = createLocEventPhaseCol(pestdata)
TPAHdata = createLocEventPhaseCol(TPAHdata)
TPCBdata = createLocEventPhaseCol(TPCBdata)

# Drop TSS column
metalsdata = dropTSSColumn(metalsdata)
PCDDdata = dropTSSColumn(PCDDdata)
pestdata = dropTSSColumn(pestdata)
TPAHdata = dropTSSColumn(TPAHdata)
TPCBdata = dropTSSColumn(TPCBdata)

# Merge dataframes
data = pd.merge(PCDDdata, metalsdata, how = 'left', on = 'Loc-Event-Phase')
data = organizeCols(data)

phase_list = ['Whole Water',
              'Suspended',
              'Dissolved',
              'On Solids']
#phase_list = ['Whole Water']
              
type_list = ['CSO', 'WWTP']           
   
data_dict = {0: TSSdata,
             1: metalsdata,
             2: VOCdata,
             3: TPAHdata,
             4: TPCBdata}
             
chem_dict = {'COPPER': 1.,
             'ZINC': 1,
             ' Naphthalene': 2,
             ' BENZENE': 2,
             'TPAH': 3,
             'TPCB (LabReported)': 4,
             'TPCB (SumCongeners)': 4}
#chem_dict = {'TPAH': 3}

units_dict = {'COPPER':                 {'Whole Water': 'ug/L',
                                         'Suspended': 'ug/L',
                                         'Dissolved': 'ug/L',
                                         'On Solids': 'mg/kg'},
              'ZINC':                   {'Whole Water': 'ug/L',
                                         'Suspended': 'ug/L',
                                         'Dissolved': 'ug/L',
                                         'On Solids': 'mg/kg'},
              ' Naphthalene':           {'Whole Water': 'ug/L'},
              ' BENZENE':               {'Whole Water': 'ug/L'},
              'TPAH':                   {'Whole Water': 'ng/L',
                                         'Suspended': 'ng/L',
                                         'Dissolved': 'ng/L',
                                         'On Solids': 'mg/kg'},
              'TPCB (LabReported)':     {'Whole Water': 'pg/L',
                                         'Suspended': 'pg/L',
                                         'Dissolved': 'pg/L',
                                         'On Solids': 'mg/kg'},
              'TPCB (SumCongeners)':    {'Whole Water': 'pg/L',
                                         'Suspended': 'pg/L',
                                         'Dissolved': 'pg/L',
                                         'On Solids': 'mg/kg'}}
             
#group_list = ['Event', 'Location']
group_list = ['Location']

#eventsymbols = {'WW-1': ('r', '+'),
#                'WW-2': ('r', 'v'),
#                'WW-3': ('r', 's'),
#                'WW-4': ('r', 'p'),
#                'WW-5': ('r', '8'),
#                'WW-6': ('r', '*'),
#                'WW-7': ('b', '+'),
#                'WW-8': ('b', 'v'),
#                'WW-9': ('b', 's'),
#                'WW-10': ('b', 'p'),
#                'WW-11': ('b', '8'),
#                'WW-12': ('b', '*'),
#                'WW-13': ('g', '+'),
#                'WW-14': ('g', 'v'),
#                'WW-15': ('g', 's'),
#                'WW-16': ('g', 'p'),
#                'WW-17': ('g', '8')}

event_list = ['WW-1',
              'WW-2',
              'WW-3',
              'WW-4',
              'WW-5',
              'WW-6',
              'WW-7',
              'WW-8',
              'WW-9',
              'WW-10',
              'WW-11',
              'WW-12',
              'WW-13',
              'WW-14',
              'WW-15',
              'WW-16',
              'WW-17']

eventcolors = {'WW-1': 'r',
               'WW-2': 'r',
               'WW-3': 'r',
               'WW-4': 'r',
               'WW-5': 'r',
               'WW-6': 'r',
               'WW-7': 'b',
               'WW-8': 'b',
               'WW-9': 'b',
               'WW-10': 'b',
               'WW-11': 'b',
               'WW-12': 'b',
               'WW-13': 'g',
               'WW-14': 'g',
               'WW-15': 'g',
               'WW-16': 'g',
               'WW-17': 'g'}

eventmarkers = {'WW-1': '^',
                'WW-2': 'v',
                'WW-3': 's',
                'WW-4': 'p',
                'WW-5': '8',
                'WW-6': '*',
                'WW-7': '^',
                'WW-8': 'v',
                'WW-9': 's',
                'WW-10': 'p',
                'WW-11': '8',
                'WW-12': '*',
                'WW-13': '^',
                'WW-14': 'v',
                'WW-15': 's',
                'WW-16': 'p',
                'WW-17': '8'}
                
                


# ============================== Create Box Plots ==============================
for chem, dataindex in chem_dict.items():
    # Split data by chemical and filter data for event and type and NaN values
    data = data_dict[dataindex]
    data = data[data['Event'].isin(events)]
    data = data[data['Type'].isin(type_list)]
    data = data[data[chem].notnull()]
        
    for phase in data['Phase'].unique():
        # Split data by phase
        plotdata = data[data['Phase'] == phase]
        units = units_dict[chem][phase]
        
        for group in group_list:
            # Plot boxplot
            ax = plotdata.boxplot(column = chem,
                                  by = group,
                                  showfliers = False)
            ax.grid(zorder=0)
            groupees = np.sort(plotdata[group].unique())
            for groupeeIndex, groupee in enumerate(groupees):
                y = plotdata[plotdata[group] == groupee][chem].tolist()
                x = [groupeeIndex + 1]*len(y)
                #x = np.random.normal(groupeeIndex + 1, 0.06, size = len(y))
                plt.plot(x, y, 'r.', alpha = 1, zorder = 3)
                                  
            # Rotate tick labels
            for tick in ax.get_xticklabels():
                tick.set_rotation(90)
            
            # Set axis titles and remove axes title
            title = 'Wet Weather Samples grouped by {0}\n{1} ({2})'.format(group, chem, phase)
            ax.set_title(title)
            ax.set_xlabel(group)            
            ax.set_ylabel('Concentration ({0})'.format(units))

            # Use tight layout            
            plt.tight_layout()
            
            # Save figure to pdf
            outname = 'Boxplot_by{0}_{1}_{2}.pdf'.format(group, phase, chem) 
            fig = ax.get_figure();
            
            fig.suptitle('')
            fig.savefig(outname)
            
# ======================= Create Event Scatter Plots =======================
for chem, dataindex in chem_dict.items():
    # Split data by chemical and filter data for event and type and NaN values
    data = data_dict[dataindex]
    data = data[data['Event'].isin(events)]
    data = data[data['Type'].isin(type_list)]
    data = data[data[chem].notnull()]
    
    for phase in data['Phase'].unique():
        units = units_dict[chem][phase]
        
        # Split data by phase
        plotdata = data[data['Phase'] == phase]
        plotdata['colors'] = plotdata['Event'].map(eventcolors)
        plotdata['markers'] = plotdata['Event'].map(eventmarkers)        
        
        # Create numerical column for lcation
        location_list = np.sort(plotdata['Location'].unique())
        location_dict = {location: val + 1 for val, location in enumerate(location_list)}
        plotdata['LocIndex'] = plotdata['Location'].map(location_dict)
        
        # Plot boxplot        
        ax = plotdata.boxplot(column = chem,
                              by = 'Location',
                              showfliers = False)
        ax.grid(zorder=0)
        
        # Plot scatter points                      
        pivotdata = pd.pivot_table(plotdata,
                                   values = chem,
                                   index = 'LocIndex',
                                   columns = 'Event')        
        for plotindex, event in enumerate(event_list):
            if event in pivotdata.columns.values:
                color = eventcolors[event]
                marker = eventmarkers[event]
                plt.scatter(pivotdata.index,
                            pivotdata[event],
                            c = color,
                            marker = marker,
                            s = 40,
                            label = event,
                            zorder = 3)
          
        
        # Add legend and customize x tick labels and y limit
        lgd = plt.legend(bbox_to_anchor=(1.02, 1),
                         loc=2,
                         borderaxespad=0.)
        plt.xticks(range(1, len(location_list)+1), location_list, rotation = 90)
        ymin, ymax = ax.get_ylim()
        ax.set_ylim(0, ymax)        
        
        # Set axis titles and remove axes title
        title = 'Wet Weather Samples grouped by Location and Event\n{0} ({1})'.format(chem, phase)
        ax.set_title(title)       
        ax.set_ylabel('Concentration ({0})'.format(units))

        # Save figure to pdf
        outname = 'Boxplot_byLocationEvent_{0}_{1}.pdf'.format(phase, chem) 
        fig = ax.get_figure();
        fig.suptitle('')
        fig.savefig(outname, bbox_extra_artists=(lgd,), bbox_inches='tight')
            
            
            
            
            
            
            
            
            
            
            