# -*- coding: utf-8 -*-
"""
Created on Tue Feb 05 10:35:51 2013

@author: abell5
"""

import urllib2
from bs4 import BeautifulSoup
from numpy import array, savetxt


id_max = 11902
#id_max = 10

cat = []

for i in range(id_max):
    soup = BeautifulSoup(urllib2.urlopen('http://www.ct.ingv.it/ufs/analisti/mappage.php?chiave=%20%20%20'+str(i+1)).read())
    table = soup.find_all('table')[1]
    row = table.find_all('tr')[1]
    
    fields = [td.string.strip() for td in row]
    fields.insert(0,str(i+1))
    
    fields = filter(None, fields)# fastest
    
    if len(fields) == 9:
        test = [x.encode('ascii', 'ignore') for x in fields]
        cat.append(test)

Cat1 = array(cat)

Cat1[Cat1[:,7]=='MD',7] = '1'
Cat1[Cat1[:,7]=='ML',7] = '2'

savetxt('..\Data\INGV_CT_1999-2013.txt', Cat1, fmt = '%s', delimiter = '\t')
#

