import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pickle
import sys
import os
from matplotlib import pylab
from varpy.management import conversion


def plot_window(obj1):
    
    fig1 = plt.figure(3)
    fig1 = plt.figure(3, figsize=(8, 3))

    plt.plot(obj1.result['med_date'],obj1.result['points'],color='blue',linewidth=1.0,linestyle='-',label='Mean quakes per day')
    plt.xlim(min(obj1.result['med_date']),max(obj1.result['med_date']))
    plt.ylim(0,20)
    plt.legend(loc='upper right')
    plt.xlabel('Datetime')
    plt.ylabel('The average number of earthquakes over a window')# (%s days)' % t_window)

    fig_name=obj1.figure+'/Window.png'
    plt.savefig(fig_name)
