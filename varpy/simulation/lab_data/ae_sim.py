#Seismic data simulation (from Andy)
#Simulates poisson process with IOL rate function
#Second column: magnitudes with gr_dist

import numpy as np
from varpy.statistics import rate_funcs, poisson_generator, mags

#########################################
#Functions to simple eq time-magnitude catalogues
def Creep_sim(t_start, t_stop, t0, t1, k1, c, p1, k2, tf, p2, mmin, b):
    if t_stop<t1:
        cat = []
    elif t_start<t1:
        IOL_spikes = iol_poisson_generator(0.0, t_stop-t1, k2, tf, p2)
        MOL_spikes = mol_poisson_generator(0.0, t_stop-t1, k1, c, p1)
        Creep_spikes = np.sort(np.concatenate((IOL_spikes, MOL_spikes))) + t1
        Creep_mags = mags.gr_mags(len(Creep_spikes), b, mmin)
        cat = np.array((np.vstack((Creep_spikes,Creep_mags)).transpose()))
    else:
        IOL_spikes = iol_poisson_generator(t_start-t1, t_stop-t1, k2, tf, p2)
        MOL_spikes = mol_poisson_generator(t_start-t1, t_stop-t1, k1, c, p1)
        Creep_spikes = np.sort(np.concatenate((IOL_spikes, MOL_spikes))) + t1
        Creep_mags = mags.gr_mags(len(Creep_spikes), b, mmin)
        cat = np.array((np.vstack((Creep_spikes,Creep_mags)).transpose()))
    return cat

def Creep_incomp_sim(t_start, t_stop, t0, t1, k1, c, p1, k2, tf, p2, mmin, b, b2):
    #simulate incomplete creep data, using "double GR" distribution
    if t_stop<t1:
        cat = []
    elif t_start<t1:
        IOL_spikes = iol_poisson_generator(0.0, t_stop-t1, k2, tf, p2)
        MOL_spikes = mol_poisson_generator(0.0, t_stop-t1, k1, c, p1)      
        IOL_incomp_spikes = iol_poisson_generator(0.0, t_stop-t1, k2*b2/(np.log(10)*b), tf, p2) #need to check this amplitude correction...
        MOL_incomp_spikes = mol_poisson_generator(0.0, t_stop-t1, k1*b2/(np.log(10)*b), c, p1)
        Creep_spikes = np.concatenate((IOL_spikes, MOL_spikes)) + t1
        Creep_incomp_spikes = np.concatenate((IOL_incomp_spikes, MOL_incomp_spikes)) + t1
        Creep_mags = mags.gr_mags(len(Creep_spikes), b, mmin)
        Creep_incomp_mags = mags.incomp_mags(len(Creep_incomp_spikes), b2, mmin)
        cat_comp = np.array((np.vstack((Creep_spikes,Creep_mags)).transpose()))
        cat_incomp = np.array((np.vstack((Creep_incomp_spikes,Creep_incomp_mags)).transpose()))
        
        cat = np.concatenate((cat_comp, cat_incomp))
        cat = cat[np.argsort(cat[:,0]),:]

    else:
        IOL_spikes = iol_poisson_generator(t_start-t1, t_stop-t1, k2, tf, p2)
        MOL_spikes = mol_poisson_generator(t_start-t1, t_stop-t1, k1, c, p1)
        IOL_incomp_spikes = iol_poisson_generator(t_start-t1, t_stop-t1, k2*b2/b, tf, p2)
        MOL_incomp_spikes = mol_poisson_generator(t_start-t1, t_stop-t1, k1*b2/b, c, p1)
        Creep_spikes = np.concatenate((IOL_spikes, MOL_spikes)) + t1
        Creep_incomp_spikes = np.concatenate((IOL_incomp_spikes, MOL_incomp_spikes)) + t1
        Creep_mags = mags.gr_mags(len(Creep_spikes), b, mmin)
        Creep_incomp_mags = mags.incomp_mags(len(Creep_incomp_spikes), b2, mmin)
        cat_comp = np.array((np.vstack((Creep_spikes,Creep_mags)).transpose()))
        cat_incomp = np.array((np.vstack((Creep_incomp_spikes,Creep_incomp_mags)).transpose()))
        
        cat = np.concatenate((cat_comp, cat_incomp))
        cat = cat[np.argsort(cat[:,0]),:]
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
