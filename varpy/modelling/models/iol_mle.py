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
from numpy import int, logical_and
from scipy.optimize import fmin
from varpy.statistics.likelihood_functions import iol_negll_og, iol_negll_og_tf
from varpy.management.conversion import int2date

def iol_mle(obj1, data_type, m1_output, tmin, t_forc,  **kwargs):
    """
    Provides maximum likelihood estimates for the inverse omori's law via fmin optimization
    output parameters are [k, tf, p]
    
    Args:
        obj1: a varpy object containing event catalogue data
        data_type: ecvd or ecld data
        m1_output: the pre-defined object containing the output data
        tmin: start of period of data for on which forecast is based
        t_forc: time at which forecast is made
        tf: optional value of failure/eruption time parameter
        ini_paras: option initial values of parameters for optimization
    
    Returns:
        updated m1_output
    """
    
    if data_type == 'ecvd' or data_type == 'ecld':
        dt_column=getattr(obj1,data_type).header.index('datetime')
        dt_data = getattr(obj1,data_type).dataset[:,dt_column]
        dt_data = dt_data[logical_and(dt_data>=tmin, dt_data<t_forc)] #Check that times have been filtered appropriately
        
        times = dt_data - tmin
        
        m1_output.metadata['parameters']=['k','tf','p']
        m1_output.metadata['rate_func']=['iol_rate']
        m1_output.metadata['total_func']=['iol_total']
    

        if 'tf' not in kwargs:
            #Forecasting mode
            if 'ini_paras' not in kwargs:
                m1_output.starting_parameters['ini_paras'] = [50., (t_forc-tmin)*2., 1.1]
            else:
                ini_paras=kwargs['ini_paras']
                m1_output.starting_parameters['ini_paras'] = ini_paras
            
            opt_output = fmin(iol_negll_og, m1_output.starting_parameters['ini_paras'] , args=(0.0, (t_forc-tmin), times), full_output=1, disp=0)
            m1_output.dataset = opt_output[0]

        else:
            #Retrospective mode
            if 'ini_paras' not in kwargs:
                m1_output.starting_parameters['ini_paras'] = [50., 1.1]
            else:
                ini_paras=kwargs['ini_paras']
                m1_output.starting_parameters['ini_paras'] = ini_paras

            tf=kwargs['tf'] 
            opt_output = fmin(iol_negll_og_tf, m1_output.starting_parameters['ini_paras'], args=(tf, 0.0, (t_forc-tmin), times), full_output=1, disp=0)
            opt_paras = opt_output[0]
            m1_output.dataset = [opt_paras[0], tf, opt_paras[1]]
        
        m1_output.ll = -opt_output[1]
        m1_output.ft = int(m1_output.dataset[1] + tmin)
                   
        
        try:
            m1_output.ft = int2date(m1_output.ft)
        except:
            m1_output.ft = m1_output.ft

    else:
        print 'data type not supported by iol_mle model', data_type
#
#