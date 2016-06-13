from datetime import datetime
import sys
import os
import numpy as np
from dateutil.parser import *



def date2int(date_str):
    date = datetime.strptime(date_str, '%d-%m-%Y')
    return date.toordinal()

def date2int2(date_str):
    date = datetime.strptime(date_str, '%d/%m/%Y')
    return date.toordinal()


def date2int3(date_str):
    if isinstance (date_str, (str, unicode)):
        date = parse(date_str).toordinal()
    else:
        date = datetime.fromordinal(date_str).toordinal()
 
    return date  

def int2date(date_int):
    date = datetime.fromordinal(date_int)
    date_str=date.strftime('%d-%m-%Y')
    return date_str

def fill_empties(data):
	try:
		output=float(data)
	except ValueError:
		output=np.nan
	return output


def time2int(time_str):
	time=datetime.strptime(time_str, '%H:%M:%S')
	return time.toordinal()

def datetime2int(date_str,time_str):
	stamp_str=date_str+time_str
	stamp=datetime.strptime(stamp_str,'%d-%m-%Y%H:%M:%S:%f')
	return stamp.toordinal()
	