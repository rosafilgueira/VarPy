# -*- coding: utf-8 -*-
"""
Created on Wed Sep 04 15:40:09 2013

@author: ABell
"""
import numpy as np
import varpy.simulation.earthquake_data.eq_sim as EQ #Functions to simulate AE data

#define volcanic rate function
def volc_quakes(sim_len, br, erupt_paras, m_min, b_value):
    quakes = EQ.CR_sim(0.,sim_len, br, m_min, b_value) #Constant rate background events
    
    n_erupt = len(erupt_paras[:,0])
    #loop through all eruptions, generating foreshock and aftershock sequences for each
    for i in range(n_erupt):
        #Create pre-eruption foreshocks using IOL function in fEQ_sim
        forequakes = EQ.IOL_sim(0.0, erupt_paras[i,1], erupt_paras[i,4], erupt_paras[i,1]+erupt_paras[i,2], erupt_paras[i,3], m_min, b_value)
        if i == 0:
            forequakes[:,0] = forequakes[:,0] + erupt_paras[i,8]
        else:
            forequakes[:,0] = forequakes[:,0] + erupt_paras[i-1,0] + erupt_paras[i,8]
        
        #Create post-eruption aftershocks using MOL function in fEQ_sim
        if i < (n_erupt-1):
            afterquakes = EQ.MOL_sim(0.0, erupt_paras[i+1,8], erupt_paras[i,7], erupt_paras[i,5], erupt_paras[i,6], m_min, b_value)
        else:
            afterquakes = EQ.MOL_sim(0.0, sim_len-erupt_paras[i,0], erupt_paras[i,7], erupt_paras[i,5], erupt_paras[i,6], m_min, b_value)
        afterquakes[:,0] = afterquakes[:,0] + erupt_paras[i,0]
        
        #Append foreshocks and aftershocks to catalogue
        quakes = np.vstack((quakes, forequakes))
        quakes = np.vstack((quakes, afterquakes))

    #Sort the catalogue accorgin to time
    quakes = quakes[np.argsort(quakes[:,0],axis=0),:]    
    
    return quakes