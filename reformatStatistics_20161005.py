# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 12:17:54 2016

@author: thasegawa
"""

import os
import pandas as pd

path = r'C:\Users\thasegawa\Documents\68 NYC DEP Papers\05 Data\Newtown Creek\Reformat Statistics 20161005'
infname = 'dioxs_OS_All_WW_WWTP.csv'

group_list = ['All_WW_WWTP',
              'AllCSO',
              'GOW_CSO',
              'NTC_CSO']

os.chdir(path)
data = pd.read_csv(infname)
data = data.rename(columns = {data.columns.values[0]: 'Chemical'})