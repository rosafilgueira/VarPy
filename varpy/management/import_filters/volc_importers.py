# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 16:18:14 2013

@author: abell5
"""
import numpy as np
import matplotlib.dates as mdates
import datetime as dt

from varpy.management import conversion 

#ECVD data- Rosa-1
def Etna_ecvd(data_file):
    Cat1 = np.array(np.loadtxt(data_file, usecols=(0,1,2,3,4,5,6),delimiter='\t',converters={1:conversion.date2int,2:mdates.datestr2num}))
    Cat1[:,2] = Cat1[:,1]+ Cat1[:,2] - mdates.date2num(dt.date.today())
    Cat1 = Cat1[:,(2,3,4,5,6)]
    Cat1 = Cat1[np.argsort(Cat1[:,0]),:]
    return Cat1

def Hierro_ecvd(data_file):
    #Import catalogue in IGN fixed width text file format
    columns = [slice(5,12), slice(17,27), slice(34,42), slice(50,57), slice(64,75), slice(85,87), slice(114,117)]
    output = []

    myfile = open(data_file)
    for line in myfile:
        fields = [line[column].strip() for column in columns]
        output.append(fields)
    Cat1 = np.array(output)
    Cat1[Cat1==''] = 999
    y=Cat1[1:,3:].astype(np.float)
    x=Cat1[1:,1:3]


    dates =[]
    times = []
    for line in x:
        datevalues = mdates.date2num(dt.datetime.strptime(line[0], "%d/%m/%Y"))
        timevalues = mdates.date2num(dt.datetime.strptime(line[1], "%H:%M:%S"))-(mdates.date2num(dt.date(1900,01,01)))
        dates.append(datevalues)
        times.append(timevalues)

    datetimes = np.add(dates,times)
    datetimes = datetimes.reshape(len(dates),1)
    Cat1 = np.concatenate((datetimes,y), axis=1)
    Cat1 = Cat1[Cat1[:,0].argsort()]
    return Cat1

def Hierro_web_ecvd(data_file):
    #Import catalogue in tab delimited txt file, copied into exel from IGN website
    Cat1 = np.array(np.loadtxt(data_file, usecols=(0,1,2,3,4,5,7),delimiter='\t',converters={1:conversion.date2int2,2:mdates.datestr2num}, skiprows=2))
    Cat1[:,2] = Cat1[:,1]+ Cat1[:,2] - mdates.date2num(dt.date.today())
    Cat1 = Cat1[:,(2,3,4,5,6)]
    Cat1 = Cat1[np.argsort(Cat1[:,0]),:]
    return Cat1

def IMO_ecvd(data_file):
    """
    Import IMO icelandic earthquake catalogue to ecvd dataset
    
    Uses data text file in format scraped from IMO weekly data by IMO_cat_scrape_update
    
    Args:
        data_file: the name and path to the text file containing ECVD data
    
    Returns:
        Cat1: the ecvd dataset
    """
    Cat1 = np.array(np.loadtxt(data_file, usecols=(0,1,2,3,4),delimiter='\t'))
    Cat1 = Cat1[np.argsort(Cat1[:,0]),:]
    return Cat1

def HVO_ecvd(data_file):
    """
    Import operation for HVO ecvd
    
    Reads HVO fixed column text file, extracts key ecvd data
    
    Args:
        data_file: the file containing the ecvd data

    Returns:
        Cat1: the processed catalogue of ecvd data
    """
    #columns are [Year, Mon, Day, Hour, Min, Sec*100, Lat-deg, Lat-min*100, Lon-deg, Lon-min*100, Depth *100, Mag*100]
    columns = [slice(0,4), slice(4,6), slice(6,8), slice(8,10), slice(10,12), slice(12,16), slice(16,18), slice(19,23), slice(23,26), slice(27,31), slice(32,36), slice(36,39)]
    region_columns = [slice(73,76)]
    
    output = []
    regions = []
    
    myfile = open(data_file)
    for line in myfile:
        fields = [line[column].strip() for column in columns]
        output.append(fields)
        
        location = [line[column].strip() for column in region_columns]
        regions.append(location)
    
    output = np.array(output)
    output[output==''] = -999
    x=output[:,0:6].astype(np.int)
    y=output[:,6:].astype(np.float)
    
    Cat1 = np.zeros((len(output), 5))
    
    for i in range(len(output)):
        Cat1[i,0] = dt.date.toordinal(dt.date(x[i,0],x[i,1],x[i,2])) + (x[i,3]/24.+x[i,4]/(24.*60.)+x[i,5]/(24.*60.*60.*100.))
        Cat1[i,1] = y[i,0] + y[i,1]/(60*100.)
        Cat1[i,2] = -(y[i,2] + y[i,3]/(60*100.))
        Cat1[i,3] = y[i,4]/100
        Cat1[i,4] = y[i,5]/100
    
    Cat1 = Cat1[Cat1[:,0].argsort()]
    return Cat1, regions


#######################
#SCVD data
def scvd_Etna_tilt(data_file):
    Cat1 = np.array(np.loadtxt(data_file, usecols=(0,1),delimiter='\t',converters={0:conversion.date2int2}))
    return Cat1

#######################
#Metadata
def metadata_imp(metadata_file):
    key=[]
    value=[]
    metadata={}
    file=open(metadata_file, 'r')
    firstline = file.readline()
    key = firstline.rstrip('\n').split('\t')
    secondline = file.readline()
    value = secondline.rstrip('\n').split('\t')     
    i = 0
    
    for item in key:
        metadata[item] = value[i]
        i =  i + 1
    
    return metadata

#######################
#Eruption data
def Etna_evd(data_file):
    catalogue=np.array(np.loadtxt(data_file, usecols=(0,1,5,6),delimiter='\t',converters={0:conversion.date2int3, 1:conversion.date2int3, 5:conversion.fill_empties, 6:conversion.fill_empties}))
    dataset=np.nan_to_num(catalogue)
    key=['start_datetime','end_datetime','event_type','eruption_location','vent_elevation','area','volume','notes']
    eruption_data={}
    file=open(data_file, 'r')
    line = file.readline()
    
    while line:
        value = line.rstrip('\n').split('\t')     
        i = 0 
        for item in key :  
            eruption_data[item] = value[i]
            i =  i + 1 
        line = file.readline()
    
    return dataset, eruption_data