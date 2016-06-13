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
#MLEs for event catalogue/Poisson process m1_outputs 
#Power-law based forecast (tf-unknown)- Rosa-1

from numpy import int
import scipy.optimize as opt
from varpy.statistics import likelihood_functions
from varpy.management import conversion

def iol_mle(obj1, data_type, m1_output, tmin, tmax, tf=None, paras=None):

  if data_type == 'ecvd' or data_type == 'scvd':
    
    dt_column=getattr(obj1,data_type).header.index('datetime')
    dt_data = getattr(obj1,data_type).dataset[:,dt_column]
    times = dt_data - tmin
    
    m1_output.metadata.append('k')
    m1_output.metadata.append('tf')
    m1_output.metadata.append('p')
    

    if tf == None:
      
      m1_output.starting_parameters['IOL_ini'] = [50., (tmax-tmin)*2., 1.1]
      m1_output.starting_parameters['IOL_opt'] = opt.fmin(likelihood_functions.iol_negll_og, m1_output.starting_parameters['IOL_ini'] , args=(0.0, (tmax-tmin), times), full_output=1, disp=0)
      m1_output.dataset = m1_output.starting_parameters['IOL_opt'][0]
      m1_output.ll =  m1_output.starting_parameters['IOL_opt'][1]
      m1_output.ft = int(m1_output.dataset[1] + tmin)
      

      try:  
        
        m1_output.ft = conversion.int2date(m1_output.ft)
        
      except:
        
        m1_output.ft = m1_output.ft
        

    else:
      m1_output.starting_parameters['IOL_ini'] = [50., 1.1] 
      m1_output.starting_parameters['IOL_opt'] = opt.fmin(likelihood_functions.iol_negll_og_tf, m1_output.starting_parameters['IOL_ini'], args=(tf, 0.0, (tmax-tmin), times), full_output=1, disp=0)
      m1_output.dataset = m1_output.starting_parameters['IOL_opt'][0]
      m1_output.ll = -m1_output.starting_parameters['IOL_opt'][1]
      m1_output.ft = None

  else:
    print 'data type not supported by m1_output', data_type
    

def hyp_mle(obj1, data_type, m1_output, tmin, tmax, tf=None, paras=None):

  if data_type == 'ecvd' or data_type == 'scvd':
   
    dt_column=getattr(obj1,data_type).header.index('datetime')
    dt_data = getattr(obj1,data_type).dataset[:,dt_column]
    times = dt_data - tmin
    #m1_output.ft = None
  
    m1_output.metadata.append('k')
    m1_output.metadata.append('tf')
    m1_output.metadata.append('p')
    
    if tf == None:
      
      m1_output.starting_parameters['HYP_ini'] = [50., (tmax-tmin)*2.]
     
      m1_output.starting_parameters['HYP_opt'] = opt.fmin(likelihood_functions.iol_negll_og_p, m1_output.starting_parameters['HYP_ini'], args=(paras, 0.0, (tmax-tmin), times), full_output=1, disp=0)
   
      m1_output.dataset = m1_output.starting_parameters['HYP_opt'][0]
      
      
      m1_output.ll = -m1_output.starting_parameters['HYP_opt'][1]
      m1_output.ft = int(m1_output.dataset[1] + tmin)
      
      try:
        
        m1_output.ft = conversion.int2date(m1_output.ft)
      except:
        
        m1_output.ft = m1_output.ft
          
    else:
      m1_output.starting_parameters['HYP_ini'] = [50.]
      m1_output.starting_parameters['HYP_opt'] = opt.fmin(likelihood_functions.iol_negll_og_p,  m1_output.starting_parameters['HYP_ini'], args=([tf, paras], 0.0, (tmax-tmin), times), full_output=1, disp=0)
      m1_output.dataset = m1_output.starting_parameters['HYP_opt'][0]
      m1_output.ll = -m1_output.starting_parameters['HYP_opt'][1]   
  else:
      print 'data type not supported by m1_output', data_type


def exp_mle(obj1, data_type, m1_output, tmin, tmax, tf=None, paras=None):

  if data_type == 'ecvd' or data_type == 'ecld':
    dt_column=getattr(obj1,data_type).header.index('datetime')
    dt_data = getattr(obj1,data_type).dataset[:,dt_column]
    times = dt_data - tmin
    
    m1_output.starting_parameters['EXP_ini'] = [0.02, 0.005]

    m1_output.starting_parameters['EXP_opt'] = opt.fmin(likelihood_functions.exp_negll, m1_output.starting_parameters['EXP_ini'], args=(0.0, (tmax-tmin), times), full_output=1, disp=0)
    m1_output.dataset = m1_output.starting_parameters['EXP_opt'][0]
    m1_output.ll = -m1_output.starting_parameters['EXP_opt'][1]


    m1_output.metadata.append('k')
    m1_output.metadata.append('tf')
    m1_output.metadata.append('p')
  
  else:
    print 'data type not supported by model'
        

def cr_mle(obj1, data_type, m1_output, tmin, tmax, tf=None, paras=None):
  if data_type == 'ecvd' or data_type == 'ecld':
              
      dt_column=getattr(obj1,data_type).header.index('datetime')
      dt_data = getattr(obj1,data_type).dataset[:,dt_column]
      
      times = dt_data - tmin
      
      m1_output.starting_parameters['CR_ini'] = [1.0]
      
      m1_output.starting_parameters['CR_opt'] = opt.fmin(likelihood_functions.cr_negll, m1_output.starting_parameters['CR_ini'], args=(0.0, (tmax-tmin), times), full_output=1, disp=0)
      m1_output.dataset = m1_output.starting_parameters['CR_opt'][0]
      m1_output.ll = -m1_output.starting_parameters['CR_opt'][1]
      m1_output.metadata.append('k')
      m1_output.metadata.append('tf')
      m1_output.metadata.append('p')
      
  else:
      print 'data type not supported by model'

def creep_mle(obj1, data_type, m1_output, tmin, tmax, tf=None, paras=None):
  if data_type == 'ecvd' or data_type == 'ecld':
    dt_column=getattr(obj1,data_type).header.index('datetime')
    dt_data = getattr(obj1,data_type).dataset[:,dt_column]


    creep_times = getattr(obj1,data_type)[logical_and(dt_data>tmin, dt_data<tmax)] - tmin
    iol_times = creep_times[creep_times>(2.*tmax/3.)]-(2.*tmax/3.)
    mol_times = creep_times[creep_times<tmax/3.]
    m1_output.metadata.append('k')
    m1_output.metadata.append('tf')
    m1_output.metadata.append('p')

    #Transient (MOL) parameters identical for retro and pro modes
    MOL_ini = [40., 0.1, 1.1]
    MOL_opt = opt.fmin(likelihood_functions.mol_negll_og, MOL_ini, args=(0.0, tmax/3., mol_times), full_output=1, disp=0)
    MOL_paras = MOL_opt[0]
    if tf == None:
        #Run in forecasting mode
        IOL_ini = [40., (tmax-tmin)*2., 1.1]
        IOL_opt = opt.fmin(likelihood_functions.iol_negll_og_tf, IOL_ini, args=(0.0, tmax/3., iol_times), full_output=1, disp=0)
        IOL_paras = IOL_opt[0]

        m1_output.starting_parameters['CREEP_ini'] = [MOL_paras[0], MOL_paras[1], MOL_paras[2], IOL_paras[0], IOL_paras[1], IOL_paras[2]+(2.*tmax/3.)]
        m1_output.starting_parameters['CREEP_opt'] = opt.fmin(likelihood_functions.creep_negll_tf, m1_output.starting_parameters['CREEP_ini'], args=(0.0, (tmax-tmin), creep_times), full_output=1, disp=0)
        m1_output.dataset= m1_output.starting_parameters['CREEP_opt']
        m1_output.dataset = [m1_output.dataset[0], m1_output.dataset[1], m1_output.dataset[2], m1_output.dataset[3], tf, m1_output.dataset[4]]
        m1_output.ll = -m1_output.starting_parameters['CREEP_opt'][1]
        
        m1_output.ft = int(IOL_paras[1] + tmin)
        
        try:
            m1_output.ft = conversion.int2date(m1_output.ft)
        except:
            m1_output.ft = m1_output.ft
            pass

    else:
        #Run in retrospective mode
        IOL_ini = [40., 1.1]
        IOL_opt = opt.fmin(likelihood_functions.iol_negll_og_tf, IOL_ini, args=(tf-(2.*tmax/3.), 0.0, tmax/3., iol_times), full_output=1, disp=0)
        IOL_paras = IOL_opt[0]

        m1_output.starting_parameters['CREEP_ini'] = [MOL_paras[0], MOL_paras[1], MOL_paras[2], IOL_paras[0], IOL_paras[1]]
        m1_output.starting_parameters['CREEP_opt'] = opt.fmin(likelihood_functions.creep_negll_tf, m1_output.starting_parameters['CREEP_ini'], args=(tf, 0.0, (tmax-tmin), creep_times), full_output=1, disp=0)
        m1_output.dataset = m1_output.starting_parameters['CREEP_opt']
        m1_output.dataset = [m1_output.dataset[0], m1_output.dataset[1], m1_output.dataset[2], m1_output.dataset[3], tf, m1_output.dataset[4]]
        m1_output.ll = -m1_output.starting_parameters['CREEP_opt'][1]
        
        m1_output.ft = None

   
    
