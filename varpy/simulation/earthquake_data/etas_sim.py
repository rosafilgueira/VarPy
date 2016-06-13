#Seismic data simulation (from Andy)
#Simulates poisson process with IOL rate function
#Second column: magnitudes with gr_dist

import numpy as np
from varpy.statistics import rate_funcs, poisson_generator, mags

###################################
def etas(t_start, t_stop, mu, alpha, p, c, k, mmin, b):
    #Generate background events
    bg_spikes = poisson_generator.pg(t_start, t_stop, mu)
    
    cat = np.empty((len(bg_spikes),2))
    cat[:,0] = bg_spikes
    cat[:,1] = mags.gr_mags(len(bg_spikes), b, mmin)

    #Create empty aray for generation information
    cat_meta = np.empty((len(bg_spikes),3))
    cat_meta[:,0] = 0 #generation number
    cat_meta[:,1] = 0 #parent ID
    cat_meta[:,2] = np.arange(len(bg_spikes)) # cluster number
    
    rng = np.random.RandomState()
    rng.seed    
    
    n_it = 0    
    
    while (n_it < np.size(cat, axis=0)):
        event_time = cat[n_it,0]
        event_mag = cat[n_it,1]
        event_gen = cat_meta[n_it,0] + 1
        
        rate_max = rate_funcs.prod(alpha, event_mag, mmin) * rate_funcs.mol_rate(0.0, k, c, p)
        
        spikes = poisson_generator.pg(event_time, t_stop, rate_max)
            
        #uniform random number on 0,1 for each spike
        rn = np.array(rng.uniform(0, 1, len(spikes)))
    
        #instantaneous rate for each spike
        spike_rate = rate_funcs.prod(alpha, event_mag, mmin)*rate_funcs.mol_rate(spikes-event_time, k, c, p)
        thin_spikes = spikes[rn<spike_rate/rate_max]
        
        afters = np.empty((len(thin_spikes),2))
        afters[:,0] = thin_spikes
        afters[:,1] = mags.gr_mags(len(thin_spikes), b, mmin)
        
        afters_meta = np.empty((len(thin_spikes),3))
        afters_meta[:,0] = event_gen
        afters_meta[:,1] = n_it
        afters_meta[:,2] = cat_meta[n_it,2]
        
        cat = np.append(cat, afters, axis=0)
        cat_meta = np.append(cat_meta, afters_meta, axis=0)
        
        n_it = n_it + 1
    
    cat = cat[cat[:,0].argsort()]    
    
    return cat
