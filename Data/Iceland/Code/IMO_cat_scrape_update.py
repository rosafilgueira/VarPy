# -*- coding: utf-8 -*-
"""
Created on Tue Feb 05 10:35:51 2013

@author: abell5
"""

import urllib2
from numpy import arange, array, savetxt, float, add, concatenate, loadtxt, vstack, unique, hstack
import matplotlib.dates as mdates
import datetime as dt

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

meta = metadata_imp('../Seismic/Cats/Iceland_IMO_C1_meta.txt')

cat_arch = loadtxt('../Seismic/Cats/Iceland_IMO_C1_95-onwards.txt', delimiter = '\t')

year_last = mdates.num2date(cat_arch[-1,0]).isocalendar()[0]
week_last = mdates.num2date(cat_arch[-1,0]).isocalendar()[1]

year_today = dt.date.today().isocalendar()[0]
week_today = dt.date.today().isocalendar()[1]

year = arange(year_last,year_today+1,1)

if week_last<=week_today:
    week = arange(week_last,week_today+1,1)
else:
    week = hstack([arange(1,week_today+1,1),arange(week_last,53,1)])

cat_update = []

for i in range(len(year)):
    for j in range(len(week)):
        url = "http://hraun.vedur.is/ja/viku/{0}/vika_{1:02d}/listi".format(year[i],week[j])
        
        try:
            f = urllib2.urlopen(url)            
            next(f)
            
            for line in f:
                fields = line.split()
                cat_update.append(fields)                
        except:
            pass

cat1 = array(cat_update)
y=cat1[:,3:].astype(float)
x=cat1[:,1:3]

dates = []
times = []
for line in x:
    datevalues = mdates.date2num(dt.datetime.strptime(line[0], "%Y%m%d"))
    timevalues = mdates.date2num(dt.datetime.strptime(line[1], "%H%M%S.%f"))-(mdates.date2num(dt.date(1900,01,01)))
    dates.append(datevalues)
    times.append(timevalues)

datetimes = add(dates,times)
datetimes = datetimes.reshape(len(dates),1)
Cat1 = concatenate((datetimes,y), axis=1)
Cat1 = Cat1[Cat1[:,0].argsort()]

if len(Cat1) == 0:
    print 'No new events'
    
else:
    #Update catalogue by appending new records
    Cat_updated = vstack((cat_arch, Cat1))
    
    u, indices = unique(Cat_updated[:,0], return_index=True)
    Cat_updated = Cat_updated[indices,:]
    
    
    #Save updated catalogue
    savetxt('../Seismic/Cats/Iceland_IMO_C1_95-onwards.txt', Cat_updated, fmt = ['%6.10f','%2.5f','%2.5f','%2.3f','%1.2f','%1.2f'], delimiter = '\t')

today = dt.date.today()

meta['time_finish'] = today.strftime('%d-%m-%y')

with open('M:\Research\Data\Etna\Seismic\Cats\Etna_INGVCT_C1_meta.txt', 'w') as f:
    for tuple in meta:
        f.write('%s\t' %tuple)
    f.write('\n')
    for tuple in meta:
        f.write('%s\t' %meta[tuple])
#
