# -*- coding: utf-8 -*-
"""
Created on Tue Feb 05 10:35:51 2013

@author: abell5
"""

import urllib2
from bs4 import BeautifulSoup
from numpy import array, savetxt, loadtxt, vstack, int
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

meta = metadata_imp('../Seismic/Cats/Etna_INGVCT_C1_meta.txt')

#Load old catalogue
cat_arch = loadtxt('../Seismic/Cats/Etna_INGVCT_C1_99-onwards.txt', dtype = 'str', delimiter = '\t')

#Take ID of last event
id_last = int(cat_arch[-1,0])

cat = []
n_miss = 0

id_now = id_last +1

#Access records for successive events until 3 "empty events" have occurred
while n_miss <3:
    soup = BeautifulSoup(urllib2.urlopen('http://www.ct.ingv.it/ufs/analisti/mappage.php?chiave=%20%20%20'+str(id_now)).read())
    table = soup.find_all('table')[1]
    row = table.find_all('tr')[1]
    
    fields = [td.string.strip() for td in row]
    fields.insert(0,str(id_now))
    
    fields = filter(None, fields)# fastest
    
    if len(fields) == 9:
        test = [x.encode('ascii', 'ignore') for x in fields]
        cat.append(test)
    else:
        n_miss = n_miss + 1
    
    id_now = id_now + 1    
        

Cat1 = array(cat)

if len(Cat1) == 0:
    print 'No new events'
    
else:
    #Use number ids for magnitude types
    Cat1[Cat1[:,7]=='MD',7] = '1'
    Cat1[Cat1[:,7]=='ML',7] = '2'
    
    #Update catalogue by appending new records
    Cat_updated = vstack((cat_arch, Cat1))
    
    #Save updated catalogue
    savetxt('../Seismic/Cats/Etna_INGVCT_C1_99-onwards.txt', Cat_updated, fmt = '%s', delimiter = '\t')

today = dt.date.today()

meta['time_finish'] = today.strftime('%d-%m-%y')

with open('M:\Research\Data\Etna\Seismic\Cats\Etna_INGVCT_C1_meta.txt', 'w') as f:
    for tuple in meta:
        f.write('%s\t' %tuple)
    f.write('\n')
    for tuple in meta:
        f.write('%s\t' %meta[tuple])
#
