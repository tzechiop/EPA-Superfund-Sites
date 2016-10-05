# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 11:19:44 2016

@author: thasegawa
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

inpath = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek'
infname = 'TPCB_PointSources.xlsx'

outpath = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek\Homolog Mass Fraction Plots'

os.chdir(inpath)

# Read input data
# Note that homologs are in pg/L
data = pd.read_excel(infname)

# Relevant parameters
typ_list = ['CSO','MS4','Treated Effluent']
homolog_list = ['Monochlorobiphenyl',
                'Dichlorobiphenyl',
                'Trichlorobiphenyl',
                'Tetrachlorobiphenyl',
                'Pentachlorobiphenyl',
                'Hexachlorobiphenyl',
                'Heptachlorobiphenyl',
                'Octachlorobiphenyl',
                'Nonachlorobiphenyl',
                'Decachlorobiphenyl']
tick_list = ['Mono', 'Di', 'Tri', 'Tetra', 'Penta', 'Hexa', 'Hepta', 'Octa', 'Nona', 'Deca']
mgkg_list = [homolog + '_mg/kg' for homolog in homolog_list]

# Calculate mg/kg
for homolog in homolog_list:
    data[homolog + '_mg/kg'] = data[homolog]/data['TSS mg/L']/1000

# Calculate medians
grouped = data.groupby('Type')
medians = grouped.median()[homolog_list + mgkg_list]

# Calculate mass fractions
medians['homolog_sum'] = 0
for homolog in homolog_list:
    medians['homolog_sum'] += medians[homolog]

for homolog in homolog_list:
    medians[homolog] = medians[homolog]/medians['homolog_sum']

# Plot mass fraction data
for typ in typ_list:
    fig, ax = plt.subplots()
    ind = np.arange(len(homolog_list))
    width = 0.6
    bar = ax.bar(ind, medians.loc[typ, homolog_list], width)
    
    # Set y-axis label and title
    ax.set_ylabel('Mass Fraction of Medians')
    ax.set_title('Homolog Mass Fractions for {0}'.format(typ))
    
    # Set y-axis limits, axis ticks and turn on y-axis grid
    ylim = 0.5
    ax.set_ylim(0, ylim)
    ax.yaxis.grid(True)    
    ax.set_yticks(np.arange(0, ylim, ylim/10))
    ax.set_xticks(ind + width/2)
    ax.set_xticklabels(homolog_list, rotation = 45, ha = 'right')
    ax.set_xticks(ind + width/2)
    
    # Save output
    outfname = 'HomologMassFractions_{0}.pdf'.format(typ)
    fig.savefig(os.path.join(outpath, outfname),
                bbox_inches='tight')
    #plt.show()
    plt.clf()
    
# Plot mg/kg data
for typ in typ_list:
    fig, ax = plt.subplots()
    ind = np.arange(len(mgkg_list))
    width = 0.6
    bar = ax.bar(ind, medians.loc[typ, mgkg_list], width)
    
    # Set y-axis label and title
    ax.set_ylabel('Median Solids Concentrations (mg/kg)')
    ax.set_title('Homolog Solids Concentrations for {0}'.format(typ))

    
    # Set y-axis limits, axis ticks and turn on y-axis grid
    ylim = 1
    ax.set_yscale("log", nonposy='clip')
    ax.set_ylim(0.0001, ylim)
    ax.yaxis.grid(True)    
    #ax.set_yticks(np.arange(0, ylim, 0.5))
    ax.set_xticks(ind + width/2)
    ax.set_xticklabels(homolog_list, rotation = 45, ha = 'right')
    ax.set_xticks(ind + width/2)
    
    # Save output
    outfname = 'HomologSolidsConcentration_{0}.pdf'.format(typ)
    #plt.show()
    fig.savefig(os.path.join(outpath, outfname),
                bbox_inches='tight')
    plt.clf()
    
# Plot TEF for WW-12
subdata = data[data['#sys_sample_code'] == 'NTC-NYCDEP-TEF-NC-002-WW12-S']

# Calculate mass frac
massfrac = subdata[homolog_list].transpose()[14]
massfrac = massfrac/massfrac.sum()

# Plot mass fraction data
fig, ax = plt.subplots()
ind = np.arange(len(homolog_list))
width = 0.6
bar = ax.bar(ind, massfrac, width)

# Set y-axis label and title
ax.set_ylabel('Mass Fraction of Medians')
ax.set_title('Homolog Mass Fractions for {0}'.format('NC-002 TEF (WW-12)'))

# Set y-axis limits, axis ticks and turn on y-axis grid
ylim = 0.5
ax.set_ylim(0, ylim)
ax.yaxis.grid(True)    
ax.set_yticks(np.arange(0, ylim, ylim/10))
ax.set_xticks(ind + width/2)
ax.set_xticklabels(homolog_list, rotation = 45, ha = 'right')
ax.set_xticks(ind + width/2)

# Save output
outfname = 'HomologMassFractions_{0}.pdf'.format('NC-002_WW-12_TEF')
fig.savefig(os.path.join(outpath, outfname),
            bbox_inches='tight')
#plt.show()
plt.clf()
    
# Plot mg/kg data
fig, ax = plt.subplots()
ind = np.arange(len(mgkg_list))
width = 0.6
bar = ax.bar(ind, subdata[mgkg_list].transpose()[14], width)

# Set y-axis label and title
ax.set_ylabel('Median Solids Concentrations (mg/kg)')
ax.set_title('Homolog Solids Concentrations for {0}'.format('NC-002 TEF (WW-12)'))

# Set y-axis limits, axis ticks and turn on y-axis grid
ylim = 1
ax.set_yscale("log", nonposy='clip')
ax.set_ylim(0.0001, ylim)
ax.yaxis.grid(True)    
#ax.set_yticks(np.arange(0, ylim, 0.5))
ax.set_xticks(ind + width/2)
ax.set_xticklabels(homolog_list, rotation = 45, ha = 'right')
ax.set_xticks(ind + width/2)

# Save output
outfname = 'HomologSolidsConcentration_{0}.pdf'.format('NC-002_WW-12_TEF')
#plt.show()
fig.savefig(os.path.join(outpath, outfname),
            bbox_inches='tight')
plt.clf()