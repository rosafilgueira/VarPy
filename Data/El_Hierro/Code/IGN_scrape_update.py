# -*- coding: utf-8 -*-
"""
Created on Tue Feb 05 10:35:51 2013

@author: abell5
"""

import urllib2
from bs4 import BeautifulSoup
from numpy import array, vstack, savetxt, loadtxt, int
import matplotlib.dates as mdates
import datetime as dt

cat_arch = loadtxt('Data\IGN_2000-date.txt', dtype = 'str', delimiter = '\t')

def date2int(date_str):
    date = dt.datetime.strptime(date_str, '%d/%m/%Y')
    return date.toordinal()
    
#Take date of last event
date_last = date2int(cat_arch[0,1])

n_days = int(mdates.date2num(dt.date.today()) - date_last)

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

#Append update, excluding duplicates
def f2(seq1,seq2): 
   # order preserving
   for i in range(len(seq1)):
       if seq1[len(seq1)-i-1,0] not in seq2[:,0]:
           seq2 = vstack((seq1[len(seq1)-i-1,:],seq2))
   return seq2

Cat_updated = cat_arch

Cat_updated = f2(Cat1, Cat_updated)


#Save updated catalogue
savetxt('Data\IGN_2000-date.txt', Cat1, fmt = '%s', delimiter = '\t')

