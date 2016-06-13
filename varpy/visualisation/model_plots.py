#Function to plot rates of earthquakes leading up to the point of eruptions
import matplotlib.pyplot as plt
from numpy import linspace, floor, ceil

from varpy.statistics import rate_funcs
from varpy.management import conversion
from varpy.visualisation import rate_plots

def model_plot(obj1, data_type, model_name, t_inc=None, t_lims=None):
    if data_type is 'ecvd' or 'ecld':
        
        #1. Determine t_min and t_max - check these aren't stored in model information...
        if t_lims is not None:
            try:
                t_min=conversion.date2int(t_lims[0])
                t_max=conversion.date2int(t_lims[1])
            except:
                t_min = float(t_lims[0])
                t_max = float(t_lims[1])
                pass
        else:
            if obj1.type == 'volcanic':
                data = obj1.ecvd.dataset
                header = obj1.ecvd.header     
            else:    
                data = obj1.ecld.dataset
                header = obj1.ecld.header
            
            dt_data = data[:,header.index('datetime')] 
              
            t_min = floor(dt_data.min())
            t_max = ceil(dt_data.max())
        
        #2. Plot the underlying rate/total graph using "rate_plots" - still need to confirm this works
        #Seems unnecessary to repeat same plotting code here.
        fig = rate_plots.ecd_rate_plot(obj1, t_inc=None, t_lims=None, Save=None)
        
        #3. Get the axes from fig to modify with new series - how best to do this?
        axes = fig.get_axes()
        ax1 = axes[0]
        ax2 = axes[1]
        
        #4. Create series of times between t_max, t_min to evaulate model rate, totals
        times = linspace(t_min, t_max, 500)
        
        
        for model in getattr(obj1,data_type).models.keys():
            
            m0=getattr(obj1,data_type).models[model].outputs

            for m1 in m0:
                #5. For each model, get rate, total function name
                rate_func =  m1.metadata['rate_func']
                total_func = m1.metadata['total_func']
                
                #6. For each model, get parameters
                params = m1.dataset
                
                #7. Determine, plot rates
                #Check that the correct "daily rate" are reported...
                rates = getattr(rate_funcs, rate_func[0])(times-t_min, params)
                ax1.plot(times, rates, '-')            
                
                #8. Determine, plot totals
                totals = getattr(rate_funcs, total_func[0])(times-t_min, 0., params)
                ax2.plot(times, totals, '-')
            
            #9. Legend
         
    else:
        #Alternative for SCVD, SCLD data?
        print 'SCLD and SCVD data not currently supported'
    
    ax1.set_xlim(t_min, t_max)
    
    png_name=obj1.figure+'/model_plot.png'
    eps_name=obj1.figure+'/model_plot.eps'
    plt.savefig(png_name)
    plt.savefig(eps_name)
#

