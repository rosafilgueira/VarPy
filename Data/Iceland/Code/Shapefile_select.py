# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 10:38:17 2011

@author: abell5
"""

#Outputs boolean type file detailing whether point lies within shapefile polygon
import sys
import numpy as np
import shapefile


namefile = sys.argv[1] #e.g. 'VWC_Katla_1995onwards.txt'
namepoly = sys.argv[2] #e.g. 'is_glaci_polygon.shp'

##########################
#Read seismicity data
Cat1 = np.array(np.loadtxt('namefile'))
lat_lons = Cat1[:,1:2]

#Read in polygon
poly = shapefile.Reader("namepoly")
poly_shp = poly.shapes()[0]

#########################
def point_in_poly(x,y,poly):

    n = len(poly)
    inside = False

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
    
#########################
#Select only events that lie within Italy polygon
poly_select = []

for line in lat_lons:
    inside = point_in_poly(line[1],line[0],poly_shp.points)
    poly_select.append(inside)

poly_select = np.array(poly_select)
namefile_select = sys.argv[3]
np.savetxt(namefile_select, poly_select, delimiter='\t')
