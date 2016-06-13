#Function to plot rates of earthquakes leading up to the point of eruptions
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from varpy.management import conversion
from numpy import logical_and, floor, ceil

def scatter_plot(obj1, variable1, variable2=None, colour=None, x_lims=None, y_lims=None, t_lims=None, lon_lims=None, lat_lims=None, z_lims=None, Mc=None):
    """
    Plot the evolution of ecvd variables. If a single variable is specified, this is plotted as a function of datetime. 
    If a second variable is specified, this is plotted on the y-axis, with variable1 on the x-axis
    
    Args:
        obj1: a varpy object containing 
        variable1: first ecvd variable
        variable2: second ecvd variable (optional)
        colour: variable to define colour scale
        x_lims: [x_min, x_max] defining x-axis limits
        y_lims: [y_min, y_max] defining y-axis limits
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
    
    if variable2 is None:
        v1_data = data[:,header.index('datetime')]
        v2_data = data[:,header.index(variable1)]
        
        if t_lims is None:
            t_min = floor(v1_data.min())
            t_max = ceil(v1_data.max())
        
        if y_lims is None:
            y_min = v2_data.min()
            y_max = v2_data.max()
    else:
        v1_data = data[:,header.index(variable1)]
        v2_data = data[:,header.index(variable2)]
        
        if x_lims is None:
            x_min = v1_data.min()
            x_max = v1_data.max()

        if y_lims is None:
            y_min = v2_data.min()
            y_max = v2_data.max()
    
    
    fig1 = plt.figure(1, figsize=(8,6))
    ax1 = fig1.add_subplot(111, axisbg='lightgrey')
    
    c_val = 'blue' #default
    if colour is not None:
        cvar_column = header.index(colour)
        c_val = data[:,cvar_column]
    
    if variable2 is None:     
        if v1_data[0]>693500:
            ax1.scatter(mdates.num2date(v1_data), v2_data, marker='o', s=9, c=c_val, edgecolor='none')
            ax1.set_xlabel('Date', fontsize=10)
        else:
            ax1.scatter(v1_data, v2_data, marker='o', s=9, c=c_val, edgecolor='none')
            ax1.set_xlabel('Day', fontsize=10)
            
        ax1.set_ylabel(variable1, fontsize=10)
        
        ax1.set_xlim(t_min,t_max)
        ax1.set_ylim(y_min,y_max)
        
        if variable1 == 'depth':
            ax1.invert_yaxis()
        
    else:    
        ax1.scatter(v1_data, v2_data, marker='o', s=9, c=c_val, edgecolor='none')
        ax1.set_xlabel(variable1, fontsize=10)
        ax1.set_ylabel(variable2, fontsize=10)
        
        ax1.set_xlim(x_min,x_max)
        ax1.set_ylim(y_min,y_max)
    
        if variable2 == 'depth':
            ax1.invert_yaxis()
    
    png_name=obj1.figure+'/'+variable1+'_scatter.png'
    eps_name=obj1.figure+'/'+variable1+'_scatter.eps'
    plt.savefig(png_name)
    plt.savefig(eps_name)
#