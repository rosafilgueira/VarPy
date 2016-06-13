#Function to plot rates of earthquakes leading up to the point of eruptions
import matplotlib.pyplot as plt
from numpy import floor, arange, histogram, atleast_2d, linspace, interp, diff, logical_and, ceil
import matplotlib.dates as mdates
from varpy.management import conversion

def rate_plot(obj1, t_inc=None, t_lims=None, lon_lims=None, lat_lims=None, z_lims=None, Mc=None):
    """
    Plot the rate and cumulative number of ecd events with time
    
    Args:
        obj1: a varpy object containing ecd data
        t_inc: the time increment over which to count event rates, default = 1
        t_lims: [t_min, t_max] defining time axis limits
        lon_lims: [lon_min, lon_max] defining x-axis limits        
        lat_lims: [lat_min, lat_max] defining y-axis limits
        z_lims: [z_min, z_max] defining depth range
        Mc: magnitude cut-off
    
    Returns:
        fig1: the resulting plot
    """
    if obj1.type == 'volcanic':
        data = obj1.ecvd.dataset
        header = obj1.ecvd.header     
    else:    
        data = obj1.ecld.dataset
        header = obj1.ecld.header 
    
    if t_lims is not None:
        try:
            t_min=conversion.date2int(t_lims[0])
            t_max=conversion.date2int(t_lims[1])
        except:
            t_min = float(t_lims[0])
            t_max = float(t_lims[1])
            pass
        data = data[logical_and(data[:,header.index('datetime')]>=t_min,data[:,header.index('datetime')]<t_max),:]
    
    if lon_lims is not None:
        data = data[logical_and(data[:,header.index('longitude')]>=lon_lims[0],data[:,header.index('longitude')]<lon_lims[1]),:]
    
    if lat_lims is not None:
        data = data[logical_and(data[:,header.index('latitude')]>=lat_lims[0],data[:,header.index('latitude')]<lat_lims[1]),:] 
    
    if z_lims is not None:
        data = data[logical_and(data[:,header.index('depth')]>=z_lims[0],data[:,header.index('depth')]<z_lims[1]),:] 
    
    if Mc is not None:
        data = data[data[:,header.index('magnitude')]>=Mc,:] 
    
    dt_data = data[:,header.index('datetime')]
    
    if t_lims is None:
        t_min = floor(dt_data.min())
        t_max = ceil(dt_data.max())
        
    if t_inc is None:
        t_inc = 1.0
    
    day_bins = arange(t_min, t_max, t_inc)
    DER, DER_bes = histogram(dt_data, day_bins)
    
    fig1 = plt.figure(1, figsize=(8,6))
    ax1 = fig1.add_subplot(111, axisbg='lightgrey')
    
    if dt_data[0]>693500:
        ax1.bar(mdates.num2date(day_bins[:-1]), DER, width=t_inc, color='darkslategrey', edgecolor='darkslategrey')
        ax1.set_xlabel('Date', fontsize=8)
    else:
        ax1.bar(day_bins[:-1], DER, width=t_inc, color='darkslategrey', edgecolor='darkslategrey')
        ax1.set_xlabel('Day', fontsize=8)    
    
    ax1.set_ylabel('Daily number of earthquakes', fontsize=8)

    ax2 = ax1.twinx()
    
    if dt_data[0]>693500:
        ax2.plot(mdates.num2date(dt_data), arange(len(dt_data))+1, 'k')
    else:
        ax2.plot(dt_data, arange(len(dt_data))+1, 'k')
    
    ax2.set_ylabel('Total earthquakes', fontsize=8)
    ax1.xaxis.set_ticks_position('bottom')
    
    if  hasattr(obj1, 'evd'):
        eruption_starts = atleast_2d(obj1.evd.dataset)[:,obj1.evd.header.index('start_datetime')]
        for i in range(len(eruption_starts)):
            if dt_data[0]>693500:
                ax1.axvline(mdates.num2date(eruption_starts[i]), color='red', linestyle='--')
            else:
                ax1.axvline(eruption_starts[i], color='red', linestyle='--')
    
    ax1.set_xlim(t_min,t_max)
    
    png_name=obj1.figure+'/Daily_earthquake_rates.png'
    eps_name=obj1.figure+'/Daily_earthquake_rates.eps'
    plt.savefig(png_name)
    plt.savefig(eps_name)


def scd_plot(obj1,variable=None):
    fig1 = plt.figure(1, figsize=(8,5))
    ax1 = fig1.add_subplot(111, axisbg='lightgrey')
    
    if obj1.type == 'volcanic':
        for key in obj1.scvd:
            data = obj1.scvd[key].dataset
            
            if data[0,0]>693500:
                ax1.plot(mdates.num2date(data[:,0]), data[:,1]-data[0,1])
            else:
                ax1.plot(data[:,0], data[:,1]-data[0,1])
                
        ax1.set_xlabel('Date', fontsize=8)
        ax1.set_ylabel('Value', fontsize=8)
        
        if hasattr(obj1, 'evd'):
            eruption_starts = atleast_2d(obj1.evd.dataset)[:,obj1.evd.header.index('start_datetime')]
            for i in range(len(eruption_starts)):
                if data[0,0]>693500:
                    ax1.axvline(mdates.num2date(eruption_starts[i]), color='red', linestyle='--')
                else:
                    ax1.axvline(eruption_starts[i], color='red', linestyle='--')
        
        ax1.set_xlim(obj1.ecvd.dataset[:,obj1.ecvd.header=='datetime'].min(),obj1.ecvd.dataset[:,obj1.ecvd.header=='datetime'].max())
         
    else:
        var_column = obj1.scld.header.index(variable)
        var_data = obj1.scld.dataset[:,var_column]
        
        dt_column=obj1.scld.header.index('datetime')
        dt_data = obj1.scld.dataset[:,dt_column]
        
        times = linspace(dt_data[0],dt_data[-1], num = 501)
        vals = interp(times, dt_data, var_data)
        
        midtimes = times[:-1] + diff(times)/2.
        rates = diff(vals)/diff(times)
        
        ax1.plot(midtimes, rates, 'o')
        ax1.set_ylabel(variable + ' rate (/s)', fontsize=8)
        
        ax2 = ax1.twinx()
        ax2.plot(dt_data, var_data-var_data[0])
        ax2.set_xlabel('Time (seconds)', fontsize=8)
            
        ax2.set_ylabel(variable, fontsize=8)
        
        if obj1.scld.dataset[:,obj1.scld.header=='datetime'].min() < obj1.scld.metadata['t1']:
            ax1.axvline(obj1.scld.metadata['t1'], color='red', linestyle='--')
        
        ax1.set_xlim(obj1.scld.dataset[:,obj1.scld.header=='datetime'].min(),obj1.scld.dataset[:,obj1.scld.header=='datetime'].max())
    
    png_name=obj1.figure+'/scd_plot.png'
    eps_name=obj1.figure+'/scd_plot.eps'
    plt.savefig(png_name)
    plt.savefig(eps_name)
