import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import sys
import os
import copy
from matplotlib import pylab
from varpy.management import conversion


def circular_location_plotter(obj1,start_datetime,finish_datetime):
    obj2=copy.deepcopy(obj1)

    
    
    start_datetime=conversion.date2int3(start_datetime)
    finish_datetime=conversion.date2int3(finish_datetime)
    datetime_colum=obj2.ecvd.header.index('datetime')

    
    datetimesls=list(obj2.ecvd.dataset[:,datetime_colum])
    size=len(datetimesls)
    start_datetime2=-1
    finish_datetime2=-1

    i=0
    flag=0
    while (i<size) and (flag==0):
        if (datetimesls[i]>=start_datetime):
            flag=1
            start_datetime2=datetimesls[i]
        else:
            i=i+1
    i=size-1
    flag=0
    while (i>0) and (flag==0):
        if (datetimesls[i]<=finish_datetime):
            flag=1
            finish_datetime2=datetimesls[i]
        else:
            i=i-1
    
    if (start_datetime2 == finish_datetime2):
        print "Exit: Start_datetime is the same than finish_datetime"
        return obj2
    elif (start_datetime2 == -1) or (finish_datetime2 == -1):
         print "Exit: One of the interval it is not found in the list"
         return obj2
    else:
        start_datetime=start_datetime2
        finish_datetime=finish_datetime2 
    #fig1=plt.figure(1,figsize-(8,3))
    #start_datetime=conversion.datetime2int(start_datetime)
    #end_datetime=conversion.datetime2int(end_datetime)
    datetime_colum=obj2.ecvd.header.index('datetime')
    lat_colum=obj2.ecvd.header.index('latitude')
    long_colum=obj2.ecvd.header.index('longitude')
    datetimes=list(obj2.ecvd.dataset[:,datetime_colum])
    start=datetimes.index(start_datetime)
    finish=datetimes.index(finish_datetime)
    LocX=(obj2.ecvd.dataset[start:finish,long_colum])
    LocY=(obj2.ecvd.dataset[start:finish,lat_colum])
    #Find n, the number of points
    n=LocX.size
    X_av=sum(LocX)/n
    Y_av=sum(LocY)/n
    X=LocX-X_av
    Y=LocY-Y_av
    fig1=plt.figure(1)
    plt.plot(X,Y,'ro')
    ax=pylab.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data',0))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data',0))

    fig_name=obj2.figure_path+'/Cicular_Location_plot.png'
    plt.savefig(fig_name)

def rectangular_location_plotter(obj1, start_datetime, finish_datetime):
    obj2=copy.deepcopy(obj1)

    start_datetime=conversion.date2int3(start_datetime)
    finish_datetime=conversion.date2int3(finish_datetime)
    
    datetime_colum=obj2.ecvd.header.index('datetime')
    lat_colum=obj2.ecvd.header.index('latitude')
    long_colum=obj2.ecvd.header.index('longitude')
    datetimes=list(obj2.ecvd.dataset[:,datetime_colum])
    #start=datetimes.index(start_datetime)
    #finish=datetimes.index(finish_datetime)

    fig1=plt.figure(2)
    datetimesls=list(obj2.ecvd.dataset[:,datetime_colum])
    size=len(datetimesls)
    start_datetime2=-1
    finish_datetime2=-1

    i=0
    flag=0
    while (i<size) and (flag==0):
        if (datetimesls[i]>=start_datetime):
            flag=1
            start_datetime2=datetimesls[i]
        else:
            i=i+1
    i=size-1
    flag=0
    while (i>0) and (flag==0):
        if (datetimesls[i]<=finish_datetime):
            flag=1
            finish_datetime2=datetimesls[i]
        else:
            i=i-1
    
    if (start_datetime2 == finish_datetime2):
        print "Exit: Start_datetime is the same than finish_datetime"
        return obj2
    elif (start_datetime2 == -1) or (finish_datetime2 == -1):
         print "Exit: One of the interval it is not found in the list"
         return obj2
    else:
        start_datetime=start_datetime2
        finish_datetime=finish_datetime2 
    
    start=datetimes.index(start_datetime)
    finish=datetimes.index(finish_datetime)
    LocX=(obj1.ecvd.dataset[start:finish,long_colum])
    LocY=(obj1.ecvd.dataset[start:finish,lat_colum])
    #Find minimums to define origin
    #Low_X=np.amin(LocX)
    #Low_Y=np.amin(LocY)
    #Find points in terms of origin
    #X=LocX-Low_X
    #Y=LocY-Low_Y
    #Plot it all
    plt.xlim(np.amin(LocX),np.amax(LocX))
    plt.ylim(np.amin(LocY),np.amax(LocY))
    plt.plot(LocX,LocY,'ro')
    fig_name=obj1.figure_path+'/Rectangular_Location_plot.png'
    plt.savefig(fig_name)

