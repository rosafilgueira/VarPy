# -*- coding: utf-8 -*-
"""
Created on Tue Feb 05 10:35:51 2013

@author: abell5
"""

import urllib2
from numpy import arange, array, savetxt, float, add, concatenate
import matplotlib.dates as mdates
import datetime as dt


year = arange(1995,2014,1)
week = arange(1,53,1)

cat = []

for i in range(len(year)):
    for j in range(len(week)):
        url = "http://hraun.vedur.is/ja/viku/{0}/vika_{1:02d}/listi".format(year[i],week[j])
        
        try:
            f = urllib2.urlopen(url)            
            next(f)
            
            for line in f:
                fields = line.split()
                cat.append(fields)                
        except:
            pass

cat1 = array(cat)
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

#Save updated catalogue
savetxt('IMO_1995-2013.txt', Cat1, fmt = ['%6.10f','%2.5f','%2.5f','%2.3f','%1.2f','%1.2f'], delimiter = '\t')
#