import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from numpy import arange, around, logical_or, logical_and
from varpy.management import conversion

def plot_map(obj1, boundary=None, colour=None, t_lims=None, lon_lims=None, lat_lims=None, z_lims=None, Mc=None):
    """
    Plot a map of ecvd locations
    
    Args:
        obj1: a varpy object containing ecvd data
        colour: variable to define colour scale (e.g. 'depth')
        boundary: a list of lon_min, lon_max, lat_min, lat_max
        t_lims: [t_min, t_max] defining time axis limits
        lon_lims: [lon_min, lon_max] defining x-axis limits        
        lat_lims: [lat_min, lat_max] defining y-axis limits
        z_lims: [z_min, z_max] defining depth range
        Mc: magnitude cut-off
        
    Returns:
        fig1: a png image of the resulting plot
    """
    
    data = obj1.ecvd.dataset
    header = obj1.ecvd.header
    
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
    
    if colour == None:
        c_val = 'blue'
    else:
        cvar_column = header.index(colour)
        c_val =  data[:,cvar_column]
    
    lats = data[:,header.index('latitude')]
    lons = data[:,header.index('longitude')]
    
    if boundary == None:
        lon_min = lons.min()
        lon_max = lons.max()
        lat_min = lats.min()
        lat_max = lats.max()
    else:
        lon_min = boundary[0]
        lon_max = boundary[1]
        lat_min = boundary[2]
        lat_max = boundary[3]
    
    m = Basemap(llcrnrlon=lon_min, llcrnrlat=lat_min, urcrnrlon=lon_max, urcrnrlat=lat_max,
            resolution='h',projection='tmerc',lon_0=lon_max +(lon_max-lon_min)/2.,lat_0=lat_max +(lat_max-lat_min)/2.)

    m.drawcoastlines()
    x,y = m(lons,lats)
    
    m.scatter(x,y, s=10, c=c_val, marker='o', edgecolor='none')
    
    delta = 0.001
    parallels = arange(around(lat_min,1),around(lat_max,1),delta)
    meridians = arange(around(lon_min,1),around(lon_max,1),delta)
    
    while logical_or(len(parallels)>10,len(meridians)>10,):
        delta = delta*10
        parallels = arange(around(lat_min,1),around(lat_max,1),delta)
        meridians = arange(around(lon_min,1),around(lon_max,1),delta)
    
    m.drawparallels(parallels,labels=[1,0,0,1])
    m.drawmeridians(meridians,labels=[1,0,0,1])
    
    m.drawmapboundary(fill_color='lightgrey')
    #m.fillcontinents(color='grey',lake_color='aqua')    
    #m.readshapefile('../Data/100m_contours', 'Contours')
    
    png_name=obj1.figure+'/map.png'
    eps_name=obj1.figure+'/map.eps'
    plt.savefig(png_name)
    plt.savefig(eps_name)
#