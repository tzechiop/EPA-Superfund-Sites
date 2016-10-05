# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 11:11:50 2016

@author: thasegawa
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import r2_score
from random import randint

# Stagger x indices
def staggerX(x, stagger = 0.02, tol = 0.5):
    newx = np.random.normal(x, stagger, size = 1)[0]
    if abs(x - newx) >= tol:
        newx = x
    return newx
    
# Estimate Log Koc
def estLogKoc(logKow):
    logKoc = 0.98 * logKow - 0.32
    return logKoc
    
# =============================================================================

datadir = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Gowanus Canal\Koc'
os.chdir(datadir)

chemical = 'PCB'
split = 1            # Fraction of dataset used for training
avg = True              # Decide whether to perform regression on averaged values

for chemical in ['PCB', 'PAH']:
    for avg in [True, False]:
        # Read data
        if chemical == 'PAH':
            rawdata = pd.read_excel('KocCalculations_PAH.xlsx',
                                    sheetname = 'PAHs')
        else:
            rawdata = pd.read_excel('KocCalculations_PCB.xlsx',
                                    sheetname = 'PCBs_finalv2')
        rawdata.loc[rawdata['LocType'] == 'WWTP Influent', 'LocType'] = 'WWTP'
        
        # Remove Dry Weather
        rawdata = rawdata[rawdata['DryWet'] == 'Wet']
        
        if chemical == 'PAH':
            chem_list = ['2-METHYLNAPHTHALENE', 'ACENAPHTHENE',
                   'ACENAPHTHYLENE', 'ANTHRACENE', 'Benz[a]anthracene',
                   'Benzo[a]pyrene', 'Benzo[b]fluoranthene', 'Benzo[ghi]perylene',
                   'Benzo[j,k]fluoranthenes', 'CHRYSENE', 'Dibenz[a,h]anthracene',
                   'FLUORANTHENE', 'FLUORENE', 'Indeno[1,2,3-cd]pyrene', 'NAPHTHALENE',
                   'PHENANTHRENE', 'PYRENE']
        else:
            chem_list = ['PCB 1','PCB 2','PCB 3','PCB 4','PCB 5','PCB 6','PCB 7','PCB 8',
            'PCB 9','PCB 10','PCB 11','PCB 12','PCB 14','PCB 15','PCB 16','PCB 17','PCB 18',
            'PCB 19','PCB 20','PCB 21','PCB 22','PCB 23','PCB 24','PCB 25','PCB 26','PCB 27',
            'PCB 31','PCB 32','PCB 35','PCB 36','PCB 37','PCB 38','PCB 39','PCB 40','PCB 42',
            'PCB 43','PCB 44','PCB 45','PCB 46','PCB 48','PCB 49','PCB 50','PCB 52','PCB 54',
            'PCB 55','PCB 56','PCB 57','PCB 58','PCB 59','PCB 60','PCB 61','PCB 63','PCB 64',
            'PCB 66','PCB 67','PCB 68','PCB 72','PCB 73','PCB 77','PCB 78','PCB 79','PCB 80',
            'PCB 81','PCB 82','PCB 83','PCB 84','PCB 85','PCB 86','PCB 88','PCB 89','PCB 90',
            'PCB 92','PCB 93','PCB 94','PCB 96','PCB 103','PCB 104','PCB 105','PCB 107','PCB 108',
            'PCB 110','PCB 111','PCB 114','PCB 118','PCB 120','PCB 121','PCB 126','PCB 127',
            'PCB 128','PCB 129','PCB 130','PCB 131','PCB 132','PCB 133','PCB 134','PCB 135',
            'PCB 136','PCB 137','PCB 139','PCB 141','PCB 144','PCB 145','PCB 146','PCB 147',
            'PCB 148','PCB 150','PCB 152','PCB 153','PCB 155','PCB 156','PCB 158','PCB 159',
            'PCB 162','PCB 164','PCB 165','PCB 167','PCB 170','PCB 171','PCB 172','PCB 174',
            'PCB 175','PCB 176','PCB 178','PCB 179','PCB 180','PCB 181','PCB 182','PCB 183',
            'PCB 184','PCB 187','PCB 188','PCB 189','PCB 190','PCB 191','PCB 194','PCB 195',
            'PCB 196','PCB 197','PCB 198','PCB 201','PCB 202','PCB 203','PCB 204','PCB 205',
            'PCB 206','PCB 207','PCB 208','PCB 209']  
        
        label_list = ['Gowanus Canal',
                      'Newtown Creek',
                      'Estimated Koc']
                    
        c_list = ['r', 'b', 'g', 'y', 'c', 'm', 'k']
        m_list = ['o', 's', '8']
        
        # Create categories
        rawdata['Data_LocType'] = rawdata.apply(lambda x: x['Data'] + '_' + x['LocType'], axis = 1)
        
        # Create dataset
        kow = rawdata.loc[rawdata['Type'] == 'Log Kow'][chem_list]
        kow = kow.transpose()
            
        datatype_list = ['Gowanus Canal_CSO', 'Gowanus Canal_WWTP', 'Newtown Creek_CSO', 'Newtown Creek_WWTP']
        for datatype in datatype_list:  
            # Format data into one dataframe
            if avg:
                koc = rawdata.loc[(rawdata['Type'] != 'Log Kow') & (rawdata['Data_LocType'] == datatype)]
                koc = koc.groupby(['Data', 'LocType']).mean()[chem_list]
            else:
                koc = rawdata.loc[(rawdata['Type'] != 'Log Kow') & (rawdata['Data_LocType'] == datatype)][chem_list]
            df = koc.stack()
            df = pd.DataFrame({'index': df.index, 'koc': df})
            df['chem'] = df['index'].apply(lambda x: x[-1])
            df['kow'] = df['chem'].map(kow.iloc[:,0])
            df = df[['koc','kow']]
        
            # Split dataset
            splitindex = np.round(len(df.index)*split)
            numtrain = splitindex
            numtest = len(df.index) - splitindex
            train = df[['kow','koc']].sample(frac = split, random_state = randint(1,200))
            test = df[['kow','koc']].drop(train.index)
            
            trainX = train['kow'].reshape(len(train.index), 1)
            trainY = train['koc'].reshape(len(train.index), 1)
            
            # Create linear regression object
            regr = linear_model.LinearRegression()
            
            # Train the model using the training sets
            regr.fit(trainX, trainY)
            
            # Plot outputs
            if avg:
                label = 'Averaged Data'
            else:
                label = 'Data'
            plt.scatter(trainX, trainY,  color='red', label = label)
            plt.plot(trainX, regr.predict(trainX), color='blue',
                               linewidth=3,
                               label = 'Regression')
            ax = plt.gca()  
            
            # Set axis limits, axis labels, and plot title
            if chemical == 'PAH':
                ax.set_xlim(2, 8)        
                ax.set_ylim(2, 8)        
            else:
                ax.set_xlim(3, 9)        
                ax.set_ylim(3, 9)        
            ax.set_ylabel('Log Koc')
            ax.set_xlabel('Log Kow (from USGS)')
            title = '{0} {1} - Log Koc Regression for {2}'.format(datatype.split('_')[0],
                                                                  datatype.split('_')[1],
                                                                  chemical)
            ax.set_title(title)
            
            
            # Output text             
            txt = 'y = {0:.3f}*x + {1:.3f}'.format(regr.coef_[0][0], regr.intercept_[0])  
            txt += '\n'
            txt += 'R-squared: {0:.3f}'.format(r2_score(trainY, regr.predict(trainX)))
            if chemical == 'PAH':
                plt.text(2.5, 7, txt)
            else:
                plt.text(3.5, 8, txt)
            
            # Create legend
            lgd = plt.legend(bbox_to_anchor=(1.02, 1),
                             loc=2,
                             borderaxespad=0.)
        
            #plt.show()
            outname = 'KocKowRegression_{0}_Avg{1}_{2}Loctype.pdf'.format(chemical, avg, datatype)
            fig = ax.get_figure();
            fig.suptitle('')
            fig.savefig(outname, bbox_inches='tight')
            plt.clf()
