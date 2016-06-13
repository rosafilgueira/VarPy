# -*- coding: utf-8 -*-
"""
Created on Wed Nov 02 12:24:38 2011

@author: abell5
"""
import datetime as dt
import numpy as np
import matplotlib.dates as mdates

#Import catalogue to format:
########################
#0.Date.time in numpy date number
#1.lat
#2.lon
#3.depth
#4.mag
#########################
#Import catalogue in ANSS fixed width text file format
columns = [slice(0,10), slice(11,22), slice(24,31), slice(32,41), slice(43,48), slice(50,54)]
output = []

myfile = open('Data/Hawaii_ANSS.txt')
for line in myfile:
    fields = [line[column].strip() for column in columns]
    output.append(fields)
Cat1 = np.array(output)
Cat1[Cat1==''] = 999
y=Cat1[:,2:].astype(np.float)
x=Cat1[:,0:2]


dates =[]
times = []
for line in x:
    datevalues = mdates.date2num(dt.datetime.strptime(line[0], "%Y/%m/%d"))
    timevalues = mdates.date2num(dt.datetime.strptime(line[1], "%H:%M:%S.%f"))-(mdates.date2num(dt.date(1900,01,01)))
    dates.append(datevalues)
    times.append(timevalues)

datetimes = np.add(dates,times)
datetimes = datetimes.reshape(len(dates),1)
Cat1 = np.concatenate((datetimes,y), axis=1)
Cat1 = Cat1[Cat1[:,0].argsort()]
# Determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs. This function
# returns True or False.  The algorithm is called
# the "Ray Casting Method".
#http://geospatialpython.com/2011/01/point-in-polygon.html

def point_in_poly(x,y,z,poly,z_range):

    n = len(poly)
    inside = False
    
    if z >= z_range[0]:
        if z < z_range[1]:
            
             p1x,p1y = poly[0]
             for i in range(n+1):
                 p2x,p2y = poly[i % n]
                 if y > min(p1y,p2y):
                     if y <= max(p1y,p2y):
                         if x <= max(p1x,p2x):
                             if p1y != p2y:
                                 xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                             if p1x == p2x or x <= xints:
                                 inside = not inside
                 p1x,p1y = p2x,p2y
                                     
    return inside


## Test

caldera_poly = [(-155.3167,19.4667),(-155.2333,19.4667),(-155.2333,19.3667),(-155.3167,19.3667)]
caldera_z = [0.0, 5.0]

## Call the function with the points and the polygon
poly_select = []

for line in Cat1:
    inside = point_in_poly(line[2],line[1],line[3],caldera_poly, caldera_z)
    poly_select.append(inside)

poly_select = np.array(poly_select)
Cat_select = Cat1[poly_select,:]

np.savetxt('Data/Hawaii_ANSS_Caldera.txt', Cat_select, fmt='%10.10f', delimiter='\t')