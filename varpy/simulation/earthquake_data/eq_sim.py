#Seismic data simulation (from Andy)
#Simulates poisson process with IOL rate function
#Second column: magnitudes with gr_dist

import numpy as np
from varpy.statistics import rate_funcs, poisson_generator, mags

#########################################
#Functions to simple eq time-magnitude catalogues
def IOL_sim(t_start, t_stop, k, tf, p, mmin, b):
    IOL_spikes = iol_poisson_generator(t_start, t_stop, k, tf, p)
    IOL_mags = mags.gr_mags(len(IOL_spikes), b, mmin)
    cat = np.array((np.vstack((IOL_spikes,IOL_mags)).transpose()))
    return cat
    
def MOL_sim(t_start, t_stop, k, c, p, mmin, b):
    MOL_spikes = mol_poisson_generator(t_start, t_stop, k, c, p)
    MOL_mags = mags.gr_mags(len(MOL_spikes), b, mmin)
    cat = np.array((np.vstack((MOL_spikes,MOL_mags)).transpose()))
    return cat

def Exp_sim(t_start, t_stop, k, lam, mmin, b):
    Exp_spikes = exp_poisson_generator(t_start, t_stop, k, lam)
    Exp_mags = mags.gr_mags(len(Exp_spikes), b, mmin)
    cat = np.array((np.vstack((Exp_spikes,Exp_mags)).transpose()))
    return cat   

def CR_sim(t_start, t_stop, rate, mmin, b):
    CR_spikes = poisson_generator.pg(t_start, t_stop, rate)
    CR_mags = mags.gr_mags(len(CR_spikes), b, mmin)
    cat = np.array((np.vstack((CR_spikes,CR_mags)).transpose()))
    return cat


#########################################
#Apply thinning approach to generate heterogeneous PP according to IOL rate function
def iol_poisson_generator(t_start, t_stop, k, t_finish, p):
    #set-up random number generator
    rng = np.random.RandomState()
    rng.seed
    
    #Calculate max rate (here always at t_stop)
    rate_max = rate_funcs.iol_rate(t_stop, k, t_finish, p)
    
    #generate spikes for hom. poisson process at maximum rate
    spikes = poisson_generator.pg(t_start, t_stop, rate_max)
    #uniform random number on 0,1 for each spike
    rn = np.array(rng.uniform(0, 1, len(spikes)))
    
    #instantaneous rate for each spike
    spike_rate = rate_funcs.iol_rate(spikes, k, t_finish, p)
    
    het_spikes = spikes[rn<spike_rate/rate_max]
    
    return het_spikes

#Apply thinning approach to generate heterogeneous PP according to EXP rate function
def exp_poisson_generator(t_start, t_stop, k, lam):
    #set-up random number generator
    rng = np.random.RandomState()
    rng.seed
    
    #Calculate max rate (here always at t_stop)
    rate_max = rate_funcs.exp_rate(t_stop, k, lam)
    
    #generate spikes for hom. poisson process at maximum rate
    spikes = poisson_generator.pg(t_start, t_stop, rate_max)
    #uniform random number on 0,1 for each spike
    rn = np.array(rng.uniform(0, 1, len(spikes)))
    
    #instantaneous rate for each spike
    spike_rate = rate_funcs.exp_rate(spikes, k, lam)
    
    het_spikes = spikes[rn<spike_rate/rate_max]
    
    return het_spikes

#Apply thinning approach to generate heterogeneous PP according to MOL rate function
def mol_poisson_generator(t_start, t_stop, k, c, p):
    #set-up random number generator
    rng = np.random.RandomState()
    rng.seed
    
    #Calculate max rate (here always at t_stop)
    rate_max = rate_funcs.mol_rate(t_start, k, c, p)
    #generate spikes for hom. poisson process at maximum rate
    spikes = poisson_generator.pg(t_start, t_stop, rate_max)
    
    #uniform random number on 0,1 for each spike
    rn = np.array(rng.uniform(0, 1, len(spikes)))
    
    #instantaneous rate for each spike
    spike_rate = rate_funcs.mol_rate(spikes, k, c, p)
    
    het_spikes = spikes[rn<spike_rate/rate_max]
    
    return het_spikes
