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