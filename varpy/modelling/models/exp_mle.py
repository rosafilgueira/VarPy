# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 11:59:08 2014

@author: abell5
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 09:42:18 2011

@author: Andrew Bell
"""
from numpy import logical_and
from scipy.optimize import fmin
from varpy.statistics.likelihood_functions import exp_negll
    
def exp_mle(obj1, data_type, m1_output, tmin, t_forc, ini_paras=None):
    """
    Provides maximum likelihood estimates for an exponential model via fmin optimization
    output parameters are [k, lambda]
    
    Args:
        obj1: a varpy object containing event catalogue data
        data_type: ecvd or ecld data
        m1_output: the pre-defined object containing the output data
        tmin: start of period of data for on which forecast is based
        t_forc: time at which forecast is made
        ini_paras: option initial values of parameters for optimization
    
    Returns:
        updated m1_output
    """
    
    if data_type == 'ecvd' or data_type == 'ecld':
        dt_column=getattr(obj1,data_type).header.index('datetime')
        dt_data = getattr(obj1,data_type).dataset[:,dt_column]
        dt_data = dt_data[logical_and(dt_data>=tmin, dt_data<t_forc)] #Check that times have been filtered appropriately
        
        times = dt_data - tmin
        
        m1_output.metadata.append('k')
        m1_output.metadata.append('lambda')
        
        if ini_paras == None:
            m1_output.starting_parameters['ini_paras'] = [0.02, 0.005]
        else:
            m1_output.starting_parameters['ini_paras'] = ini_paras
            
        opt_output = fmin(exp_negll, m1_output.starting_parameters['ini_paras'] , args=(0.0, (t_forc-tmin), times), full_output=1, disp=0)
        m1_output.dataset = opt_output[0]
        
        m1_output.ll = -opt_output[1]

    else:
        print 'data type not supported by iol_mle model', data_type
#