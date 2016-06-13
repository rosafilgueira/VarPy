# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 15:03:00 2012

@author: Andrew Bell
"""
#To simulate and plot volcanic quake time-series data

import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates

import numpy as np

import Eruption_sim as erupt #Function to generate eruption times
import Volcanic_eq_sim as volc_eq #Functions to simulate AE data
import Volcanic_defm_sim as volc_defm


#Simulation length (years)
years = 10
sim_len = np.floor(years*365.25)

#################################
#Specify simulation parameters
br = 0.1 #Background rate, events/day

#Foreshock parameters
te = 200.0    #failure time (in days)
tc_fore = 0.1 #Constant to avoid singularity (in days)
p_fore = 0.85  #power-law exponent
k_fore = 10.0  #power-law amplitude

#Aftershock parameters
tc_aft = 1.0  #Constant to avoid singularity (in days)
p_aft = 1.5   #power-law exponent
k_aft = 40.0   #power-law amplitude

#Recharge parameters
t_recharge = 400.00 #Time required to re-enter accelerating phase

#M-F parameters
b_value = 1.5 #b-value of Gutenberg-Richter relation
m_min = 2.0  #Minimum catalog magnitude

#Tilt data parameters
k_infl = 0.4 #Inflation rate constant
k_defl = k_infl*te #Deflation constant
tilt_noise = 1.0 #Gaussian noise
sr = 1 #sample rate (days)

#####################################
#Determine eruption times and parameters
erupt_times, erupt_paras = erupt.eruptions(sim_len, te, tc_fore, p_fore, k_fore, tc_aft, p_aft, k_aft, t_recharge, k_infl, k_defl)

#############################
#Call volc_quakes function to simulate earthquake catalogue
quakes = volc_eq.volc_quakes(sim_len, br, erupt_paras, m_min, b_value)

#############################
#Call volc_defm function to simulate tilt data
tilt = volc_defm.volc_tilt(sim_len, tilt_noise, erupt_paras, sr)

#############################
#Calculate daily rate for plotting
ts = np.arange(np.ceil(sim_len)+1)
mid_ts = ts[:-1] + np.diff(ts)/2
daily_rates, dr_bes = np.histogram(quakes[:,0], ts)

#####################################
#Plot figures
fig1 = plt.figure(1)
ax1 = fig1.add_subplot(311)
ax1.bar(mdates.num2date(mid_ts+mdates.date2num(dt.date(2000,01,01))), daily_rates, align='center')
ax1.set_xlabel('Date')
ax1.set_ylabel('Daily Earthquake Rate')
ax1.set_ylim((0,50))
#ax1.set_xlim((0,sim_len))

ax2 = ax1.twinx()
ax2.plot(mdates.num2date(quakes[:,0]+mdates.date2num(dt.date(2000,01,01))), np.arange(1,len(quakes[:,0])+1), 'b')
ax2.set_ylabel('Total Earthquakes')
#ax2.set_ylim((0,1000))
#ax2.set_xlim((0,sim_len))

ax3 = fig1.add_subplot(312)
ax3.plot(mdates.num2date(quakes[:,0]+mdates.date2num(dt.date(2000,01,01))),quakes[:,1], '.')
ax3.set_ylim(ymin=m_min)
ax3.set_xlabel('Date')
ax3.set_ylabel('Magnitude')

ax4 = fig1.add_subplot(313)
ax4.plot(mdates.num2date(tilt[0,:]+mdates.date2num(dt.date(2000,01,01))),tilt[1,:])
#ax4.set_ylim(ymin=m_min)
ax4.set_xlabel('Date')
ax4.set_ylabel('Tilt')

plt.show()

