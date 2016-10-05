# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 12:31:48 2016

@author: thasegawa
"""

import os
import pandas as pd

def convertValue(x, newunit = 'mg/kg'):
    conv= {'mg/kg': 10**(-3),
           'ng/kg': 10**(-9),
           'ug/kg': 10**(-6)}
    oldunit = x['target_unit']
    converted_value = x['result_value'] * conv[oldunit] / conv[newunit]
    return converted_value

# ================================================================================

maindir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek'
outdir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek\SedTrapData for GIS'

os.chdir(maindir)

fname = 'NCP2_SedTrapEvents1_9_Compiled_wTotals_wParticulates.xlsx'

data = pd.read_excel(fname)

for chemical in ['PCB-011', 'TPCB (Congeners)']:
    plotdata = data[data['chemical_name'] == chemical]
    
    # Identify units
    units = plotdata['target_unit'].unique()[0]
    
    # Convert units to mg/kg
    datacol = 'converted_value'
    if units == 'pct':
        plotdata[datacol] = plotdata['result_value']
    else:
        plotdata[datacol] = plotdata.apply(convertValue, axis = 1)      
        units = 'mg/kg'
        
    outfname = 'NCP2_SedTrapEvents_{0}.csv'.format(chemical)
    plotdata.to_csv(os.path.join(outdir,outfname),
                    index = False)