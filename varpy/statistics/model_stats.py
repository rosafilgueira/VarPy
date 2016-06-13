# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 12:26:53 2014

@author: abell5
"""

from scipy import stats
from numpy import zeros, histogram
from varpy.statistics import poisson_generator

def model_CoIs(rate_func, params, bins, percentiles=None, n_bs=None):
    
    if percentiles is None:
        percentiles = [5,95]
    
    if n_bs is None:
        n_bs = 500
        
    #Bootstrap model CIs
    rates = zeros((len(bins)-1,n_bs))
    
    for j in range(n_bs):
        spikes = poisson_generator.het_pg(rate_func, bins[0], bins[-1], params)
        rates[:,j], dr_bes_bs = histogram(spikes+bins[0], bins)
    

    coi_l = stats.scoreatpercentile(rates, percentiles[0], axis=1)
    coi_u = stats.scoreatpercentile(rates, percentiles[1], axis=1)

    return coi_l, coi_u
