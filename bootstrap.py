# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 08:43:45 2016

@author: thasegawa
"""

import pandas as pd
import numpy as np
from scipy import stats
import random

def calc_geostd(data):
    gmean = stats.mstats.gmean(data)    
    sigma = np.sum([np.log((x/gmean))**2 for x in data])
    geostd = np.exp((sigma/len(data))**0.5)
    return geostd

def bootstrap(data, samplenum, percentile_list, outfname = False, print_bootstrap = False, print_means = False, print_medians = False, print_gmeans = False):
    # Split analysis for datatyp
    numsamples = len(data)
    
    # Run bootstrap
    bootstrap_list = []
    median_list = []
    mean_list = []
    gmean_list = []
    geostd_list = []
    geose_list = []
    for index in range(samplenum):
        bootstrapdata = [random.choice(list(data)) for sample in range(numsamples)]
        
        if print_bootstrap:
            bootstrap_list.append(bootstrapdata)
        
        median_list.append(stats.scoreatpercentile(bootstrapdata, 50))        
        mean_list.append(np.mean(bootstrapdata))
        gmean_list.append(stats.mstats.gmean(bootstrapdata))
        geostd_list.append(calc_geostd(bootstrapdata))
        geose_list.append(calc_geostd(bootstrapdata)/(len(bootstrapdata)**0.5))
        
        
    # Find percentiles
    percentiledict = {}
    for percentilenum in percentile_list:
        percentiledict[str(percentilenum) + ' (Median)'] = stats.scoreatpercentile(median_list, percentilenum)
        percentiledict[str(percentilenum) + ' (Mean)'] = stats.scoreatpercentile(mean_list, percentilenum)
        percentiledict[str(percentilenum) + ' (Geo Mean)'] = stats.scoreatpercentile(gmean_list, percentilenum)
        percentiledict[str(percentilenum) + ' (Geo Std)'] = stats.scoreatpercentile(geostd_list, percentilenum)
        percentiledict[str(percentilenum) + ' (Geo SE)'] = stats.scoreatpercentile(geose_list, percentilenum)
        
        
    # Print data if requested
    if print_bootstrap:
        pd.DataFrame(bootstrap_list).to_excel(print_bootstrap)
        
    if print_means:
        pd.DataFrame(mean_list).to_excel(print_means)
        
    if print_medians:
        pd.DataFrame(median_list).to_excel(print_medians)        
        
    if print_gmeans:
        pd.DataFrame(gmean_list).to_excel(print_gmeans)        
        
    return percentiledict