# -*- coding: utf-8 -*-
"""
Created on Tue Feb 05 14:32:18 2013

@author: abell5
"""

import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
import matplotlib.gridspec as gridspec

##########################
def date2int(date_str):
    date = dt.datetime.strptime(date_str, '%d/%m/%Y')
    return date.toordinal()

#Load data
Cat1 = np.array(np.loadtxt('Data\IGN_2000-date.txt', usecols=(0,1,2,3,4,5,6), delimiter = '\t', converters = {1: date2int, 2: mdates.datestr2num}))

#Organize data-time
Cat1[:,2] = Cat1[:,1]+Cat1[:,2]-mdates.date2num(dt.date.today())
Cat1 = Cat1[:,(2,3,4,5,6)]
Cat1 = Cat1[np.argsort(Cat1[:,0]),:]

##########################
#Lat-lon filters for El Hierro
lat_min = 27.55
lat_max = 27.95
lon_min = -18.40
lon_max = -17.85

z_max = 40.0
m_cutoff = 0.05

t_erupt = mdates.date2num(dt.date(2011,10,11))

t_start = mdates.date2num(dt.date(2011,7,19))
t_end = mdates.date2num(dt.date.today())

#Filter catalogue
#1. By Latitude
Cat1 = Cat1[np.logical_and(Cat1[:,1]>=lat_min, Cat1[:,1]<lat_max),:]
#2. By Longitude
Cat1 = Cat1[np.logical_and(Cat1[:,2]>=lon_min, Cat1[:,2]<lon_max),:]
#3. By depth
Cat1 = Cat1[Cat1[:,3]<=z_max]

#4. By time
Cat1 = Cat1[np.logical_and(Cat1[:,0]>=t_start, Cat1[:,0]<t_end),:]

mc_cat = 1.5

#5. BY magnitude
Cat_mc = Cat1[Cat1[:,4]>=mc_cat]

N = len(Cat_mc[:,0])
###############################################

#Count daily rates of earthquakes
days = np.floor(Cat_mc[:,0])
day_bins = np.arange(days.min(), days.max()+1)
DER, DER_bes = np.histogram(days, day_bins)

i=t_end-t_start

mpl.rc('font', **{'sans-serif':'Verdana','family':'sans-serif','size':6})
mpl.rcParams['xtick.direction'] = 'out'
mpl.rcParams['ytick.direction'] = 'out'
mpl.rcParams['axes.linewidth'] = 0.75
mpl.rcParams['lines.markeredgewidth'] = 0.05


#######################
#daily and total rate plot
fig1 = plt.figure(figsize=(11.7, 6.0))
gs = gridspec.GridSpec(3, 2)
ax1 = fig1.add_subplot(gs[:, 0])

###########
#locations
m = Basemap(llcrnrlon=lon_min, llcrnrlat=lat_min, urcrnrlon=lon_max, urcrnrlat=lat_max,
            resolution='h',projection='tmerc',lon_0=lon_max +(lon_max-lon_min)/2.,lat_0=lat_max +(lat_max-lat_min)/2.)

m.drawcoastlines()
x,y = m(Cat_mc[:,2],Cat_mc[:,1])

m.scatter(x,y,s=10, c=range(len(Cat_mc[:,0])), norm=plt.normalize(vmin=0, vmax=N), marker='o', edgecolor='none')
m.drawmapboundary(fill_color='lightgrey')
m.drawparallels(np.arange(27.6,28.0,0.1),labels=[1,0,0,1])
m.drawmeridians(np.arange(-18.4,-17.8,0.1),labels=[1,0,0,1])

mdates.DateFormatter('dd/mm/yyyy')

plt.text(0.67, 0.95, mdates.num2date(t_start+i).strftime('%d/%m/%Y'), fontsize = 9, transform=ax1.transAxes)

###########
ax2 = fig1.add_subplot(gs[0,1],axisbg='lightgrey')
ax2.bar(mdates.num2date(day_bins[:-1]), DER, color='darkslategrey', edgecolor='darkslategrey')
ax2.set_ylabel('Daily earthquakes (M>1.5)', fontsize=8)
ax2.set_xlim(mdates.num2date(t_start), mdates.num2date(t_end))
ax2.set_ylim(0, 250)

ax3 = ax2.twinx()
ax3.plot(mdates.num2date(Cat_mc[:,0]), np.arange(len(Cat_mc[:,0]))+1, 'b')
ax3.set_ylabel('Total earthquakes (M>1.5)', fontsize=8)
ax2.xaxis.set_ticks_position('bottom')
ax3.set_ylim(0, 11000)
ax3.set_xlim(mdates.num2date(t_start), mdates.num2date(t_end))
ax3.axvline(mdates.num2date(t_erupt), color='r', ls = '--')
ax3.axvline(mdates.num2date(t_start+i+1), color='k', ls = '--')

###########
#    time_scaled = (data[:,0]-data[:,0].min())/data[:,0].ptp(axis=0)
#    colors = plt.cm.coolwarm(time_scaled)

ax4 = fig1.add_subplot(gs[1,1],axisbg='lightgrey')
ax4.scatter(mdates.num2date(Cat1[:,0]), Cat1[:,4], marker='o', s=7, c='grey', edgecolor='none')
ax4.scatter(mdates.num2date(Cat_mc[:,0]), Cat_mc[:,4], marker='o', s=7, c=range(len(Cat_mc[:,0])), norm=plt.normalize(vmin=0, vmax=N), edgecolor='none')    
ax4.set_ylim(0,5)
ax4.set_ylabel('Magnitude', fontsize=8)
ax4.xaxis.set_ticks_position('bottom')
ax4.set_xlim(mdates.num2date(t_start), mdates.num2date(t_end))
ax4.axhline(1.5, color='darkgrey', ls = '--')
ax4.axvline(mdates.num2date(t_erupt), color='r', ls = '--')
ax4.axvline(mdates.num2date(t_start+i+1), color='k', ls = '--')

###########
ax5 = fig1.add_subplot(gs[2,1],axisbg='lightgrey')
ax5.scatter(mdates.num2date(Cat1[:,0]),Cat1[:,3], marker='o', s=7, c='grey', edgecolor='none')
ax5.scatter(mdates.num2date(Cat_mc[:,0]),Cat_mc[:,3], marker='o', s=7, c=range(len(Cat_mc[:,0])), norm=plt.normalize(vmin=0, vmax=N), edgecolor='none')
ax5.set_ylim(30,0)
ax5.set_ylabel('Depth', fontsize=8)
ax5.set_xlabel('Time (days)', fontsize=8)
ax5.xaxis.set_ticks_position('bottom')
ax5.set_xlim(mdates.num2date(t_start), mdates.num2date(t_end))
ax5.axvline(mdates.num2date(t_erupt), color='r', ls = '--')
ax5.axvline(mdates.num2date(t_start+i+1), color='k', ls = '--')


plt.subplots_adjust(wspace = 0.15)

plt.show()