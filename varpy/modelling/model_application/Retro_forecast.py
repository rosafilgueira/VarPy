# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 14:26:08 2013

@author: abell5
"""
import copy
from numpy import arange, zeros

def retro_forc(obj1, start, finish, inc, model):
    obj2=copy.deepcopy(obj1)
    
    forecast_times = arange(start, finish, inc)
    
    n_forec = len(forecast_times)
    
    #How to specify model? Can we put together a list/dictionary? Stores model location, descriptions, parameters etc...
    #N-paras, location... = Look up model in directory
    
    #Specify output arrays
    #forecast_paras = zeros((n_forec, n_paras))
    #model_lls (or model BICs?)
    
    for i in range(n_forec):
        obj3 = window(obj2, start?, finish?)
        
        forec_paras[:,i], model_lls[i] = model(obj3, start?, finish?)
    
    return forcast_paras, model_lls