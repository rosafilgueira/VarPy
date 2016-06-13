import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys
import os
import pickle
import shutil
from matplotlib import pylab

def date2int(date_str):
    date = dt.datetime.strptime(date_str, '%d-%m-%Y')
    return date.toordinal()

def Read_ECVD_Data(metadata):
   
    data=np.array(np.loadtxt(metadata[6], usecols=(0,1,2,3,4,5,6,7),delimiter='\t',converters={1:date2int,2:mdates.datestr2num}))

    return data

def Read_Metadata(directory,data_name):
    
    metadata=[]
    
    
    file=open(directory+'/Metadata/'+'Metadata_'+data_name, 'r')
    for line in file.readlines():
        metadata = line.split('\t')
    file.close()

    metadata[0]=data_name
    metadata[6]=directory + '/'+ metadata[6] +'/'+ data_name
    metadata[7]=directory+ '/'+ metadata[7] 
    metadata[10]=directory+ '/'+ metadata[10]

    fileobj1=open(directory+'/Metadata/'+'Metadata_'+data_name, 'w')
    for item in metadata:
        fileobj1.write('%s\t' % str(item))
    fileobj1.close()
    return metadata

#Meatada list contains right now -->0:Exp_Id, 1:Experiment_type, 2:Datatypes, 3:Time_increment, 4:Speed , 5:Path_data , 6:Path_Results, 7:Timestamp_start, 8:Timestamp_creep 9:Time_Experiment, 10:Path_Figures, 11: Completness_Magnitude(Portlet Parameter),
#12:Source_location:Hierro or Etna. For real and synthetic data, this value is t1


def Remove_Environment(directory):
    if os.path.exists(directory +'/Data'):
        shutil.rmtree(directory +'/Data')
    if os.path.exists(directory +'/Output'):
        shutil.rmtree(directory +'/Output')
    if os.path.exists(directory +'/Figure'):
        shutil.rmtree(directory +'/Figure')
    if os.path.exists(directory +'/Metadata'):
        shutil.rmtree(directory +'/Metadata')
        print "after removing Metadata"


def Setup_Environment(directory, data_file, metadata_file):
    if not os.path.exists(directory +'/Data'):
        os.makedirs(directory +'/Data')
    if not os.path.exists(directory +'/Output'):
        os.makedirs(directory +'/Output')
    if not os.path.exists(directory +'/Figure'):
        os.makedirs(directory +'/Figure')
    if not os.path.exists(directory +'/Metadata'):
        os.makedirs(directory +'/Metadata')

            
    data_F= data_file.split('/')
    data_name = data_F[-1]


    shutil.copy(data_file,directory+'/Data/'+data_name)
    shutil.copy(metadata_file,directory+'/Metadata/'+'Metadata_'+data_name)
    return data_name

def Moving_Window(start_date,finish_date,data,t_window,t_move, metadata):
    print "printing metadata 7"
    print metadata[7]
    reply='y'
    answer='n'
    while(reply!='n' and answer!='y'):
        if(t_move>=t_window):
            print "The analysis windows do not overlap."
            reply=raw_input("Would you like to chose parameters again (y/n)?")
            continue
        else:
            print "Your parameters are %s and %s days" % (t_window,t_move)
            answer=raw_input("Accept? (y/n)")
            continue
    start_date=date2int(start_date)
    finish_date=date2int(finish_date)
    datesls=list(data[:,1])
    x=datesls.index(start_date)
    beg_date=start_date
    end_date=start_date
    points=[0]
    med_dates=[0]
    while(end_date<=finish_date):
        i=0
        med_date=(datesls[((datesls.index(beg_date))+(datesls.index(end_date)))/2])-start_date
        med_dates.append(med_date)
        y=datesls.index(beg_date)
        beg_date=datesls[(y+(points[-1])*t_move)] #This is not an accurate way to do it sadly but tis a way
        quakes_per_day=[0]
        while(i<=t_window):
            y=datesls[x]
            w=datesls[x-1]
            if(y==w):
                x=x+1
                continue
            else:
                i=i+1
                j=datesls.count(y)
                quakes_per_day.append(j)
                x=x+1
                continue
        end_date=datesls[x]
        points.append(sum(quakes_per_day)/t_window)
        continue

    fileobj1=open(metadata[7]+'/Median_dates(fromt0).txt','w')
    pickle.dump(med_dates,fileobj1)
    fileobj1.close()

    fileobj2=open(metadata[7]+'/Average_quakes_per_day.txt','w')
    pickle.dump(points,fileobj2)
    fileobj2.close()

#    fileobj3=open(directory+'/Output/Time_Interval.txt','w')
#   pickle.dump(start_date,fileobj3)
#     fileobj3.close()

# fileobj4=open(directory+'/Output/Time_Interval.txt','a')
#  pickle.dump(finish_date,fileobj4)
#  fileobj4.close()

    return med_dates
    return points

def Plot_Window(metadata):
    
    fig1 = plt.figure(1)
    fig1 = plt.figure(1, figsize=(8, 3))
    fileobj1=open(metadata[7]+'/Median_dates(fromt0).txt','r')
    med_dates=pickle.load(fileobj1)
    fileobj1.close()

    fileobj2=open(metadata[7]+'/Average_quakes_per_day.txt','r')
    points=pickle.load(fileobj2)
    fileobj2.close()


    plt.plot(med_dates,points,color='blue',linewidth=1.0,linestyle='-',label='Mean quakes per day')
    plt.xlim(min(med_dates),max(med_dates))
    plt.ylim(0,20)
    plt.legend(loc='upper right')
    plt.xlabel('Date')
    plt.ylabel('The average number of earthquakes over a window')# (%s days)' % t_window)

    fig_name=metadata[10]+'/Window.png'
    plt.savefig(fig_name)

def Rectangular_Location_Plotter(data, metadata, myexperiment):
    fig1=plt.figure(1)
    start_date=myexperiment[1]
    end_date=myexperiment[2]
    #fig1=plt.figure(1,figsize-(8,3))
    start_date=date2int(start_date)
    end_date=date2int(end_date) 
    dates=list(data[:,1])
    start=dates.index(start_date)
    end=dates.index(end_date)
    
    LocX=(data[start:end,4])
    LocY=(data[start:end,3])
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
    fig_name=metadata[10]+'/Location_plot.png'
    plt.savefig(fig_name)

def Circular_Location_Plotter(data,metadata,myexperiment):
    ###################
    #Centre defined how?
    #For now I will do an average of the points but the location of the volcano may be a good centre definition
    fig1=plt.figure(1)
    start_date=myexperiment[1]
    end_date=myexperiment[2]
    #fig1=plt.figure(1,figsize-(8,3))
    start_date=date2int(start_date)
    end_date=date2int(end_date)
    dates=list(data[:,1])
    start=dates.index(start_date)
    end=dates.index(end_date)
    LocX=(data[start:end,4])
    LocY=(data[start:end,3])
    #Find n, the number of points
    n=LocX.size
    X_av=sum(LocX)/n
    Y_av=sum(LocY)/n
    X=LocX-X_av
    Y=LocY-Y_av
    plt.plot(X,Y,'ro')
    ax=gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data',0))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data',0))
    
    fig_name=metadata[10]+'/Cicular_Location_plot.png'
    plt.savefig(fig_name)
