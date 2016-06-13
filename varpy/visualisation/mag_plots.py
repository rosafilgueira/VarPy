#Function to plot rates of earthquakes leading up to the point of eruptions
import matplotlib.pyplot as plt
from varpy.statistics import mags
import matplotlib.dates as mdates
from varpy.management import conversion
from numpy import logical_and, floor, ceil, log10

def mf_plot(obj1, y_lims=None, mag_lims=None, lon_lims=None, lat_lims=None, z_lims=None):
    """
    Plots the magnitude frequency distribution (discrete and cumulative), showing completeness estimates
    
    Args:
        obj1: a varpy object containing 
        y_lims: [y_min, y_max] defining y-axis limits
        mag_lims: [mag_min, mag_max] defining magntiude axis limits
        lon_lims: [lon_min, lon_max] defining x-axis limits        
        lat_lims: [lat_min, lat_max] defining y-axis limits
        z_lims: [z_min, z_max] defining depth range
    
    Returns:
        fig1: a png image of the resulting plot
    """    
    if obj1.type == 'volcanic':
        data = obj1.ecvd.dataset
        header = obj1.ecvd.header     
    else:    
        data = obj1.ecld.dataset
        header = obj1.ecld.header 
        
    if lon_lims is not None:
        data = data[logical_and(data[:,header.index('longitude')]>=lon_lims[0],data[:,header.index('longitude')]<lon_lims[1]),:]
    
    if lat_lims is not None:
        data = data[logical_and(data[:,header.index('latitude')]>=lat_lims[0],data[:,header.index('latitude')]<lat_lims[1]),:] 
    
    if z_lims is not None:
        data = data[logical_and(data[:,header.index('depth')]>=z_lims[0],data[:,header.index('depth')]<z_lims[1]),:] 
    
    mag_data = data[:,header.index('magnitude')]
    
    if mag_lims is None:
        mag_lims = [mag_data.min(), mag_data.max()]
    
    if y_lims is None:
        y_lims = [0,10**ceil(log10(len(mag_data)))]
    
    GFT = mags.mc_GFT(mag_data, 0.1, 0.1)
    MBS = mags.mc_mbs(mag_data, 0.1, 0.1)
    
    mc_maxc = mags.mc_maxc(mag_data, 0.1, 0.1)
    mc_GFT = GFT.Mc_GFT
    mc_mbs = MBS.Mc_mbs
    
    fmd = mags.fmd(mag_data,0.1, 0.1) 
    
    fig1 = plt.figure(1, figsize=(8,6))
    
    ax1 = fig1.add_subplot(111,axisbg='lightgrey')
    ax1.semilogy(fmd.m_bins, fmd.dis_mf, 'bs')
    ax1.semilogy(fmd.m_bins, fmd.cum_mf, 'r^')
    ax1.axvline(mc_maxc, color='red', ls = '--')
    ax1.axvline(mc_GFT, color='green', ls = '--')
    ax1.axvline(mc_mbs, color='blue', ls = '--')

    ax1.set_ylim(y_lims[0], y_lims[1])
    ax1.set_xlim(mag_lims[0], mag_lims[1])
    ax1.set_xlabel('Magnitude', fontsize=8)
    ax1.set_ylabel('Frequency', fontsize=8)
    
    png_name=obj1.figure+'/MF_plot.png'
    eps_name=obj1.figure+'/MF_plot.eps'
    plt.savefig(png_name)
    plt.savefig(eps_name)


def mag_mc_plot(obj1, colour=None, y_lims=None, t_lims=None, lon_lims=None, lat_lims=None, z_lims=None):
    """
    Plot the evolution of magntiudes with time, and show completeness magnitudes
    
    Args:
        obj1: a varpy object containing 
        variable: the ecvd variable to plot as a function of time
        colour: variable to define colour scale
        y_lims: [y_min, y_max] defining y-axis limits
        t_lims: [t_min, t_max] defining time axis limits
        lon_lims: [lon_min, lon_max] defining x-axis limits        
        lat_lims: [lat_min, lat_max] defining y-axis limits
        z_lims: [z_min, z_max] defining depth range
    
    Returns:
        fig1: a png image of the resulting plot
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
    
    dt_data = data[:,header.index('datetime')]
    mag_data = data[:,header.index('magnitude')]
    
    if t_lims is None:
        t_min = floor(dt_data.min())
        t_max = ceil(dt_data.max())
    
    if y_lims is None:
        y_lims = [mag_data.min(), mag_data.max()]
    
    c_val = 'blue' #default
    if colour is not None:
        cvar_column = header.index(colour)
        c_val = data[:,cvar_column]
   
    GFT = mags.mc_GFT(mag_data, 0.1, 0.1)
    MBS = mags.mc_mbs(mag_data, 0.1, 0.1)
    
    mc_maxc = mags.mc_maxc(mag_data, 0.1, 0.1)
    mc_GFT = GFT.Mc_GFT
    mc_mbs = MBS.Mc_mbs
    
    fig1 = plt.figure(1, figsize=(8,6))
    ax1 = fig1.add_subplot(111,axisbg='lightgrey')
    
    if dt_data[0]>693500:
        ax1.scatter(mdates.num2date(dt_data), mag_data, marker='o', s=9, c=c_val, edgecolor='none')
        ax1.set_xlabel('Date', fontsize=8)
    else:
        ax1.scatter(dt_data, mag_data, marker='o', s=9, c='blue', edgecolor='none')
        ax1.set_xlabel('Day', fontsize=8)
    
    ax1.set_ylabel('Magnitude', fontsize=8)
    ax1.xaxis.set_ticks_position('bottom')
    ax1.set_xlim(t_min,t_max)
    ax1.set_ylim(y_lims[0],y_lims[1])

    ax1.axhline(mc_maxc, color='red', ls = '--')
    ax1.axhline(mc_GFT, color='green', ls = '--')
    ax1.axhline(mc_mbs, color='blue', ls = '--')
    
    png_name=obj1.figure+'/M_time_plot.png'
    eps_name=obj1.figure+'/M_time_plot.eps'
    plt.savefig(png_name)
    plt.savefig(eps_name)
#

def mag_spike_plot(obj1, colour=None, y_lims=None, t_lims=None, lon_lims=None, lat_lims=None, z_lims=None):
    """
    Plot the evolution of magntiudes with time as spikes
    
    Args:
        obj1: a varpy object containing 
        variable: the ecvd variable to plot as a function of time
        colour: variable to define colour scale
        y_lims: [y_min, y_max] defining y-axis limits
        t_lims: [t_min, t_max] defining time axis limits
        lon_lims: [lon_min, lon_max] defining x-axis limits        
        lat_lims: [lat_min, lat_max] defining y-axis limits
        z_lims: [z_min, z_max] defining depth range
    
    Returns:
        fig1: a png image of the resulting plot
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
    
    dt_data = data[:,header.index('datetime')]
    mag_data = data[:,header.index('magnitude')]
    
    if t_lims is None:
        t_min = floor(dt_data.min())
        t_max = ceil(dt_data.max())
    
    if y_lims is None:
        y_lims = [mag_data.min(), mag_data.max()]
    
    c_val = 'blue' #default
    if colour is not None:
        cvar_column = header.index(colour)
        c_val = data[:,cvar_column]
    
    fig1 = plt.figure(1, figsize=(8,6))
    ax1 = fig1.add_subplot(111,axisbg='lightgrey')
    
    if dt_data[0]>693500:
        ax1.vlines(mdates.num2date(dt_data), y_lims[0], mag_data, color=c_val)
        ax1.scatter(mdates.num2date(dt_data), mag_data, marker='o', s=15, c='none', edgecolor=c_val)
        ax1.set_xlabel('Date', fontsize=8)
    else:
        ax1.vlines(dt_data, y_lims[0], mag_data, color=c_val)
        ax1.scatter(dt_data, mag_data, marker='o', s=15, c='none', edgecolor=c_val)
        ax1.set_xlabel('Day', fontsize=8)
    
    ax1.set_ylabel('Magnitude', fontsize=8)
    ax1.xaxis.set_ticks_position('bottom')
    ax1.set_xlim(t_min,t_max)
    ax1.set_ylim(y_lims[0],y_lims[1])
    
    png_name=obj1.figure+'/M_spike_plot.png'
    eps_name=obj1.figure+'/M_spike_plot.eps'
    plt.savefig(png_name)
    plt.savefig(eps_name)
#

def bstab_plot(obj1, y_lims=None, mag_lims=None, lon_lims=None, lat_lims=None, z_lims=None):
    """
    Plot the variation in b-value with cut-off magnitude of an ecd catalogue
    
    Args:
        obj1: a varpy object containing 
        variable: the ecvd variable to plot as a function of time
        colour: variable to define colour scale
        mag_lims: [mag_min, mag_max] defining y-axis limits
        lon_lims: [lon_min, lon_max] defining x-axis limits        
        lat_lims: [lat_min, lat_max] defining y-axis limits
        z_lims: [z_min, z_max] defining depth range
    
    Returns:
        fig1: a png image of the resulting plot
    """      
    if obj1.type == 'volcanic':
        data = obj1.ecvd.dataset
        header = obj1.ecvd.header     
    else:    
        data = obj1.ecld.dataset
        header = obj1.ecld.header 
        
    if lon_lims is not None:
        data = data[logical_and(data[:,header.index('longitude')]>=lon_lims[0],data[:,header.index('longitude')]<lon_lims[1]),:]
    
    if lat_lims is not None:
        data = data[logical_and(data[:,header.index('latitude')]>=lat_lims[0],data[:,header.index('latitude')]<lat_lims[1]),:] 
    
    if z_lims is not None:
        data = data[logical_and(data[:,header.index('depth')]>=z_lims[0],data[:,header.index('depth')]<z_lims[1]),:] 
    
    mag_data = data[:,header.index('magnitude')]
    
    if mag_lims is None:
        mag_lims = [mag_data.min(), mag_data.max()]
    
    if y_lims is None:
        y_lims = [0.5,2.5]
   
    GFT = mags.mc_GFT(mag_data, 0.1, 0.1)
    MBS = mags.mc_mbs(mag_data, 0.1, 0.1)
    
    mc_maxc = mags.mc_maxc(mag_data, 0.1, 0.1)
    mc_GFT = GFT.Mc_GFT
    mc_mbs = MBS.Mc_mbs
    
    fig1 = plt.figure(1, figsize=(8,6))
    ax1 = fig1.add_subplot(111,axisbg='lightgrey')

    ax1.errorbar(MBS.Mco, MBS.bi, yerr=MBS.unc, )

    ax1.axhline(1.0, color='darkgrey', ls = '--')
    ax1.axvline(mc_maxc, color='red', ls = '--')
    ax1.axvline(mc_GFT, color='green', ls = '--')
    ax1.axvline(mc_mbs, color='blue', ls = '--')
    
    ax1.set_xlabel('Magntiude cut-off', fontsize=8)
    ax1.set_ylabel('b-value', fontsize=8)
    ax1.set_ylim(y_lims[0], y_lims[1])
    ax1.set_xlim(mag_lims[0], mag_lims[1])
    
    png_name=obj1.figure+'/bstab_plot.png'
    eps_name=obj1.figure+'/bstab_plot.eps'
    plt.savefig(png_name)
    plt.savefig(eps_name)
#