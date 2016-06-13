#Function to plot interevent time statistics of earthquakes

import matplotlib.pyplot as plt
from varpy.management import conversion
from numpy import arange, histogram, diff, logspace, zeros, mean, floor, ceil, logical_and
from scipy.stats import gamma, poisson, expon, scoreatpercentile


def rate_histogram(obj1, model=None, interval=None, t_lims=None, lon_lims=None, lat_lims=None, z_lims=None, Mc=None):
    """
    Plot a histogram of earthquake rates
    
    Args:
        obj1: a varpy object containing event catalogue data
        model: option to fit and bootstrap CoIs for model. Existing options: Poisson
        interval: bin width (default is daily)
        t_lims: [t_min, t_max] defining time axis limits
        lon_lims: [lon_min, lon_max] defining x-axis limits        
        lat_lims: [lat_min, lat_max] defining y-axis limits
        z_lims: [z_min, z_max] defining depth range
        Mc: magnitude cut-off
    
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
    
    if Mc is not None:
        data = data[data[:,header.index('magnitude')]>=Mc,:] 
    
    dt_data = data[:,header.index('datetime')]
    
    if t_lims is None:
        t_min = floor(dt_data.min())
        t_max = ceil(dt_data.max())
    
    if interval is not None:
        bin_width = interval
    else:
        bin_width = 1.
    
    der_bins = arange(t_min, t_max+bin_width, bin_width)
    
    ders, der_bes = histogram(dt_data, der_bins)
    
    rate_bins = arange(-0.5, ders.max()+1.5)
    mid_rate_bins = rate_bins[:-1] + diff(rate_bins)/2.
    rate_freqs, rate_bes = histogram(ders, rate_bins)
    
    fig1 = plt.figure(1, figsize=(8,6))
    ax1 = fig1.add_subplot(111, axisbg='lightgrey')
    
    ax1.bar(mid_rate_bins, rate_freqs, color='grey', edgecolor='darkgrey', align='center')
    
    if model is not None:
        der_mean = mean(ders)
    
        #Bootstrap 95% COIs
        rate_bstps = 1000

        rates_bstps = zeros((len(rate_bins)-1,rate_bstps))
    
        for j in range(rate_bstps):
            if model is 'Poisson':
                model_sim=poisson.rvs(der_mean,size=len(ders))
            
            rates_bstps[:,j], model_bes = histogram(model_sim, rate_bins)

        poisson_coi_95 = scoreatpercentile(rates_bstps.transpose(), 95, axis=0)
        poisson_coi_5 = scoreatpercentile(rates_bstps.transpose(), 5, axis=0)    
    

        ax1.plot(mid_rate_bins, poisson.pmf(mid_rate_bins, der_mean)*diff(rate_bins)*len(ders), '-or')
        ax1.plot(mid_rate_bins, poisson_coi_95, 'r:')
        ax1.plot(mid_rate_bins, poisson_coi_5, 'r:')
    
    ax1.set_xlabel('Rate', fontsize=8)
    ax1.set_ylabel('Frequency', fontsize=8)

    ax1.xaxis.set_ticks_position('bottom')

    png_name=obj1.figure_path+'/rate_histogram.png'
    eps_name=obj1.figure_path+'/rate_histogram.eps'
    plt.savefig(png_name)
    plt.savefig(eps_name)
#


def iet_plot(obj1, Norm=None, model=None, t_lims=None, lon_lims=None, lat_lims=None, z_lims=None, Mc=None):
    """
    Plot a histogram of interevent times and a pdf of normalized IETs
    
    Args:
        obj1: a varpy object containing event catalogue data
        Norm: if True, normalize the IET histogram
        model: option to fit and bootstrap CoIs for model. Existing options: Poisson, Gamma
        t_lims: [t_min, t_max] defining time axis limits
        lon_lims: [lon_min, lon_max] defining x-axis limits        
        lat_lims: [lat_min, lat_max] defining y-axis limits
        z_lims: [z_min, z_max] defining depth range
        Mc: magnitude cut-off

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
    
    if Mc is not None:
        data = data[data[:,header.index('magnitude')]>=Mc,:] 
    
    dt_data = data[:,header.index('datetime')]
    
    iets = diff(dt_data, n=1)
    iet_mean = mean(iets)
    
    iet_bins = logspace(-5.0,2.0,num=50)
    mid_iet_bins = iet_bins[:-1] + diff(iet_bins)/2

    iet_counts, iet_bes = histogram(iets, iet_bins)
    
    ##########
    fig1 = plt.figure(1, figsize=(12,6))
    ax1 = fig1.add_subplot(121,axisbg='lightgrey')
    
    ax1.semilogx(mid_iet_bins, iet_counts, '-s', color='blue')

    ax2 = fig1.add_subplot(122,axisbg='lightgrey')
    ax2.loglog(mid_iet_bins/iet_mean, (iet_mean*iet_counts)/(diff(iet_bins)*len(iets)), '-s', color='blue')
    
    if Norm is True:
        norm = iet_mean
    else:
        norm = 1.
    
    if model is not None:
        #Bootstrap 95% COIs
        iet_bstps = 1000
        rates_bstps = zeros((len(iet_bins)-1,iet_bstps))
        
        if model is 'Gamma':
            #fit gamma model
            fit_alpha,fit_loc,fit_beta=gamma.fit(iets, loc=0.0)
            for j in range(iet_bstps):
                model_sim = gamma.rvs(fit_alpha,loc=fit_loc,scale=fit_beta,size=len(iets))
                rates_bstps[:,j], model_bes = histogram(model_sim, iet_bins)
                
            coi_95 = scoreatpercentile(rates_bstps.transpose(), 95, axis=0)
            coi_5 = scoreatpercentile(rates_bstps.transpose(), 5, axis=0)
            
            ax1.semilogx(mid_iet_bins/norm, gamma.pdf(mid_iet_bins, fit_alpha, fit_loc, fit_beta)*diff(iet_bins)*len(iets), 'r')
            ax1.semilogx(mid_iet_bins/norm, coi_95, 'r:')
            ax1.semilogx(mid_iet_bins/norm, coi_5, 'r:')
            
            ax2.loglog(mid_iet_bins/iet_mean, (iet_mean*gamma.pdf(mid_iet_bins, fit_alpha, fit_loc, fit_beta)), 'r')
            ax2.loglog(mid_iet_bins/iet_mean, (iet_mean*coi_95)/(diff(iet_bins)*len(iets)), 'r:')
            ax2.loglog(mid_iet_bins/iet_mean, (iet_mean*coi_5)/(diff(iet_bins)*len(iets)), 'r:')
            
        elif model is 'Poisson':
            #fit exponential model            
            for j in range(iet_bstps):
                model_sim = expon.rvs(scale=iet_mean,size=len(iets))
                rates_bstps[:,j], model_bes = histogram(model_sim, iet_bins)
            
            coi_95 = scoreatpercentile(rates_bstps.transpose(), 95, axis=0)
            coi_5 = scoreatpercentile(rates_bstps.transpose(), 5, axis=0)
            
            ax1.semilogx(mid_iet_bins/norm, expon.pdf(mid_iet_bins, loc=0, scale=iet_mean)*diff(iet_bins)*len(iets), 'r')
            ax1.semilogx(mid_iet_bins/norm, coi_95, 'r:')
            ax1.semilogx(mid_iet_bins/norm, coi_5, 'r:')
            
            ax2.loglog(mid_iet_bins/iet_mean, (iet_mean*expon.pdf(mid_iet_bins, loc=0, scale=iet_mean)), 'r')
            ax2.loglog(mid_iet_bins/iet_mean, (iet_mean*coi_95)/(diff(iet_bins)*len(iets)), 'r:')
            ax2.loglog(mid_iet_bins/iet_mean, (iet_mean*coi_5)/(diff(iet_bins)*len(iets)), 'r:')
    
    if Norm is True:
        ax1.set_xlabel(r'$\tau \backslash \bar\tau$ (days)')
    else:
        ax1.set_xlabel(r'$\tau$ (days)')
    
    ax1.set_ylabel('Frequency')
    ax1.xaxis.set_ticks_position('bottom')    
    
    ax2.set_xlim(0.00008,200)
    ax2.set_ylim(0.00001,1000)
    ax2.set_xlabel(r'$\tau \backslash \bar\tau$ (days)')
    ax2.set_ylabel('pdf')
    
    ax2.xaxis.set_ticks_position('bottom')

    png_name=obj1.figure_path+'/iet_plots.png'
    eps_name=obj1.figure_path+'/iet_plots.eps'
    plt.savefig(png_name)
    plt.savefig(eps_name)
#