# -*- coding: utf-8 -*-
"""
Created on Tue Feb 05 10:35:51 2013

@author: abell5
"""

import urllib2
from bs4 import BeautifulSoup
from numpy import array, savetxt, int
import matplotlib.dates as mdates
import datetime as dt

n_days = int(mdates.date2num(dt.date.today()) - mdates.date2num(dt.date(2000,1,1)))

cat = []

#Access records for last n days
soup = BeautifulSoup(urllib2.urlopen('http://www.02.ign.es/ign/layoutIn/sismoListadoTerremotos.do?cantidad_dias='+str(n_days)).read())
table = soup.find_all('table')[0]
rows = table.find_all('tr')
n_rows = rows.__len__() - 1

for i in range(n_rows-1):
    row = rows[i+1]
    fields = row.find_all('td')
    
    out = []
    out.append(fields[0].string.strip())
    out.append(fields[1].string.strip())
    out.append(fields[2].string.strip())
    out.append(fields[3].string.strip())
    out.append(fields[4].string.strip())
    
    if fields[5].string.strip() == '':
        out.append('-99')
    else:
        out.append(fields[5].string.strip())
        
    if fields[7].string.strip() == '':
        out.append('-99')
    else:
        out.append(fields[7].string.strip())

    out.append(fields[8].string.strip())
    out.append(fields[9].string.strip())
    
    test = [x.encode('ascii', 'ignore') for x in out]

    cat.append(test)

Cat1 = array(cat)

#Save updated catalogue
savetxt('Data\IGN_2000-date.txt', Cat1, fmt = '%s', delimiter = '\t')

