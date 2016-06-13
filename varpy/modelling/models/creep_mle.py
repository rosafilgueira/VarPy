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
from varpy.statistics.likelihood_functions import mol_negll_og, iol_negll_og, iol_negll_og_tf, creep_negll, creep_negll_tf
from varpy.management.conversion import int2date

def creep_mle(obj1, data_type, m1_output, tmin, t_forc, **kwargs):
    """
    Provides maximum likelihood estimates for the 2 power-law creep model via fmin optimization
    output parameters are [k1, c, p1, k2, tf, p2]
    
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
        
        creep_times = dt_data - tmin
        iol_times = creep_times[creep_times>(2.*t_forc/3.)]-(2.*t_forc/3.)
        mol_times = creep_times[creep_times<t_forc/3.]
        
        m1_output.metadata.append('k1')
        m1_output.metadata.append('c')
        m1_output.metadata.append('p1')
        m1_output.metadata.append('k2')
        m1_output.metadata.append('tf')
        m1_output.metadata.append('p2')
    
        #First guess at transient (MOL) parameters - identical for retro and forecasting modes
        if 'ini_paras' not in kwargs:
            MOL_ini = [50., 0.1, 1.1]
        else:
            ini_paras=kwargs['ini_paras']
            MOL_ini = ini_paras[0:3]

        MOL_opt = fmin(mol_negll_og, MOL_ini, args=(0.0, t_forc/3., mol_times), full_output=1, disp=0)
        MOL_paras = MOL_opt[0]
        
        
        if 'tf' not in kwargs:
            #Forecasting mode
            if 'ini_paras' not in kwargs:
                IOL_ini = [50., (t_forc-tmin)*2., 1.1]
            else:
                ini_paras=kwargs['ini_paras']
                IOL_ini = ini_paras[3:6]
            
            #First guess at accelerating (IOL) parameters
            IOL_opt = fmin(iol_negll_og, IOL_ini, args=(0.0, t_forc/3., iol_times), full_output=1, disp=0)
            IOL_paras = IOL_opt[0]

            #Use first guess parameters as starting values for full creep model optimization
            m1_output.starting_parameters['ini_paras'] = [MOL_paras[0], MOL_paras[1], MOL_paras[2], IOL_paras[0], IOL_paras[1]+(2.*t_forc/3.), IOL_paras[2]]
            opt_output = fmin(creep_negll, m1_output.starting_parameters['ini_paras'], args=(0.0, (t_forc-tmin), creep_times), full_output=1, disp=0)
            m1_output.dataset = opt_output[0]
        
        else:
            #Retrospective mode
            if 'ini_paras' not in kwargs:
                IOL_ini = [50., 1.1]
            else:
                ini_paras=kwargs['ini_paras']
                IOL_ini = ini_paras[3:5]
            tf=kwargs['tf']
            #First guess at accelerating (IOL) parameters
            IOL_opt = fmin(iol_negll_og_tf, IOL_ini, args=(tf-(2.*t_forc/3.), 0.0, t_forc/3., iol_times), full_output=1, disp=0)
            IOL_paras = IOL_opt[0]
            
            #Use first guess parameters as starting values for full creep model optimization
            m1_output.starting_parameters['ini_paras'] = [MOL_paras[0], MOL_paras[1], MOL_paras[2], IOL_paras[0], IOL_paras[1]]
            opt_output = fmin(creep_negll_tf, m1_output.starting_parameters['ini_paras'], args=(tf, 0.0, (t_forc-tmin), creep_times), full_output=1, disp=0)
            opt_paras = opt_output[0] 
            m1_output.dataset = [opt_paras[0], opt_paras[1], opt_paras[2], opt_paras[3], tf, opt_paras[4]]     
        
        m1_output.ll = -opt_output[1]
        m1_output.ft = int(m1_output.dataset[1] + tmin)            
        
        try:
            m1_output.ft = int2date(m1_output.ft)
        except:
            m1_output.ft = m1_output.ft

    else:
        print 'data type not supported by creep_mle model', data_type
#
