#function to generate poisson events at constant rate
import numpy as np

#####################################
#define 
def pg(t_start, t_stop, rate):
    #set-up random number generator
    rng = np.random.RandomState()
    rng.seed
    
    #Calc expected number of events give PP rate and duration
    n_exp = np.ceil((t_stop-t_start)*rate)
    iets = rng.exponential(1.0/rate, n_exp)
    spikes = t_start + np.add.accumulate(iets)
    
    i = np.searchsorted(spikes, t_stop)
    
    #Add extra spikes if length too short
    extra_spikes = []
    if i==len(spikes):
        # ISI buf overrun
                
        t_last = spikes[-1] + rng.exponential(1.0/rate, 1)[0]
    
        while (t_last<t_stop):
            extra_spikes.append(t_last)
            t_last += rng.exponential(1.0/rate, 1)[0]
                
        spikes = np.concatenate((spikes,extra_spikes))
        #print "ISI buf overrun handled. len(spikes)=%d, len(extra_spikes)=%d" % (len(spikes),len(extra_spikes))
    
    else:
        spikes = np.resize(spikes,(i,))
        #print "len(spikes)=%d" % (len(spikes))
    return spikes