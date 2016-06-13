# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 15:21:49 2012

@author: abell5
"""
#Defines eruption times and parameters 

import numpy as np

def eruptions(sim_len, te, tc_fore, p_fore, k_fore, tc_aft, p_aft, k_aft, t_recharge, k_infl, k_defl):
    t_last = 0.0
    erupt_times = []
    erupt_tes = []
    erupt_t_recharges = []
    
    while (t_last < sim_len):
        #Determine value of te and t_recharge
        te_last = te*np.random.lognormal(mean=0.0, sigma=0.5)
        t_recharge_last = t_recharge*np.random.lognormal(mean=0.0, sigma=0.5)
        
        #Time of eruption = time of last eruption + t_recharge + te
        t_last = t_last + t_recharge_last + te_last  
        
        if t_last < sim_len:
            #Append eruption time parameters
            erupt_times.append(t_last)
            erupt_tes.append(te_last)
            erupt_t_recharges.append(t_recharge_last)
    
    #Create output array and add random model paramter values
    erupt_paras = np.zeros((len(erupt_times),11))
    
    erupt_paras[:,0] = erupt_times
    erupt_paras[:,1] = erupt_tes
    erupt_paras[:,2] = tc_fore*np.ones(len(erupt_times))
    erupt_paras[:,3] = np.random.normal(loc=p_fore, scale=p_fore/20, size=len(erupt_times))
    erupt_paras[:,4] = np.random.normal(loc=k_fore, scale=k_fore/20, size=len(erupt_times))
    erupt_paras[:,5] = tc_aft*np.ones(len(erupt_times))
    erupt_paras[:,6] = np.random.normal(loc=p_aft, scale=p_aft/20, size=len(erupt_times))
    erupt_paras[:,7] = np.random.normal(loc=k_aft, scale=k_aft/20, size=len(erupt_times))
    erupt_paras[:,8] = erupt_t_recharges
    erupt_paras[:,9] = np.random.normal(loc=k_infl, scale=k_infl/20, size=len(erupt_times))
    erupt_paras[:,10] = np.random.normal(loc=k_defl, scale=k_defl/20, size=len(erupt_times))
    
    return erupt_times, erupt_paras