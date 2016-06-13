#function to generate poisson events at constant rate
from numpy import random, ceil, add, searchsorted, concatenate, resize, array
from varpy.statistics import rate_funcs
from scipy.optimize import fminbound

#####################################
def pg(t_start, t_stop, rate):
    #set-up random number generator
    rng = random.RandomState()
    rng.seed
    
    #Calc expected number of events give PP rate and duration
    n_exp = ceil((t_stop-t_start)*rate)
    iets = rng.exponential(1.0/rate, n_exp)
    spikes = t_start + add.accumulate(iets)
    
    i = searchsorted(spikes, t_stop)
    
    #Add extra spikes if length too short
    extra_spikes = []
    if i==len(spikes):
        # ISI buf overrun
                
        t_last = spikes[-1] + rng.exponential(1.0/rate, 1)[0]
    
        while (t_last<t_stop):
            extra_spikes.append(t_last)
            t_last += rng.exponential(1.0/rate, 1)[0]
                
        spikes = concatenate((spikes,extra_spikes))
        #print "ISI buf overrun handled. len(spikes)=%d, len(extra_spikes)=%d" % (len(spikes),len(extra_spikes))
    
    else:
        spikes = resize(spikes,(i,))
        #print "len(spikes)=%d" % (len(spikes))
    return spikes


def het_pg(rate_func, t_start, t_stop, params):
    #set-up random number generator
    rng = random.RandomState()
    rng.seed
    
    #Ude fminbound to find maximum rate between t_start and t_stop
    opt_output = fminbound(lambda x,p: -getattr(rate_funcs, rate_func[0])(x,p), 0, t_stop-t_start, args=(params,), full_output=1, disp=0)   
    rate_max = -opt_output[1]

    #generate spikes for hom. poisson process at maximum rate
    spikes = pg(0, t_stop-t_start, rate_max)
    
    #uniform random number on 0,1 for each spike
    rn = array(rng.uniform(0, 1, len(spikes)))
    
    #instantaneous rate for each spike
    spike_rate = getattr(rate_funcs, rate_func[0])(spikes, params)
    
    het_spikes = spikes[rn<spike_rate/rate_max]

    return het_spikes