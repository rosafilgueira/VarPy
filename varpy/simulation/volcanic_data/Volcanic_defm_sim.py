# -*- coding: utf-8 -*-
"""
Created on Wed Sep 04 15:40:09 2013

@author: ABell
"""
import numpy as np

#define volcanic rate function
def volc_tilt(sim_len, tilt_noise, erupt_paras, sr):
    days = np.arange(0, np.floor(sim_len), sr)
    tilt_rate = np.zeros(len(days))
    n_erupt = len(erupt_paras[:,0])
    
    eruption_no = 0
    
    for i in range(len(days)):
        
        if days[i]<np.floor(erupt_paras[0,8]):
            tilt_rate[i] = 0.0
            
        elif days[i]<np.floor(erupt_paras[0,0]):
            tilt_rate[i] = erupt_paras[0,9]
            
        elif days[i] == np.floor(erupt_paras[0,0]):        
            tilt_rate[i] = -erupt_paras[0,10]
            eruption_no = eruption_no + 1
            
        elif eruption_no == n_erupt:
            tilt_rate[i] = 0.0
            
        elif days[i]<np.floor(erupt_paras[eruption_no,8]) + np.floor(erupt_paras[eruption_no-1,0]):
            tilt_rate[i] = 0.0
            
        elif days[i]<np.floor(erupt_paras[eruption_no,0]):
            tilt_rate[i] = erupt_paras[eruption_no,9]
            
        elif days[i]==np.floor(erupt_paras[eruption_no,0]):
            tilt_rate[i] = -erupt_paras[eruption_no,10]
            eruption_no = eruption_no + 1
    
        
    tilt_rate = tilt_rate + np.random.normal(loc=0, scale=tilt_noise, size=len(days))
    tilt = np.cumsum(tilt_rate).transpose()
    tilt = np.vstack((days,tilt))
    return tilt