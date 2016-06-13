    
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 15:43:45 2011

@author: abell5
"""

import numpy as np

#########################################
#1. rate function for exponential model:
def exp_rate(t, params):
    k=params[0]
    lam=params[1]
    
    rate = []
    rate = k*np.exp(lam*t)
    return rate

#2. Total functin for exponential model:
def exp_total(t, t0, params):
    k=params[0]
    lam=params[1]
    
    total = []
    total = (k/lam)*(np.exp(lam*t)-np.exp(lam*t0))
    return total
    
#########################################
#1. rate function for modified omori law:
def mol_rate(t, params):
    k=params[0]
    c=params[1]
    p=params[2]
    
    #note t is time from t0
    rate = []
    rate = k*(t+c)**-p
    return rate
    
#4. Total function for modified Omori law:
def mol_total(t, t0, params):
    k=params[0]
    c=params[1]
    p=params[2]
    
    total = []
    if p == 1.0:
        total = k*(np.log(c+t) - np.log(c+t0))
    else:
        total = k/(1.-p)*(((c+t)**(1.-p))-((c+p)**(1.-p)))
    return total

#########################################
#3. Rate function for inverse Omori law:
def iol_rate(t, params):
    k=params[0]
    tf=params[1]
    p=params[2]
    
    rate = []
    rate = k*(tf-t)**-p
    return rate

#4. Total function for inverse Omori law:
def iol_total(t, t0, params):
    k=params[0]
    tf=params[1]
    p=params[2]
    
    total = []
    if p == 1.0:
        total = k*(-np.log(tf-t) + np.log(tf-t0))
    else:
        total = -k/(1.-p)*(((tf-t)**(1.-p))-((tf-t0)**(1.-p)))
    return total

#########################################
#3. Rate function for inverse Omori law:
def hyp_rate(t, params):
    k=params[0]
    tf=params[1]
    
    rate = []
    rate = k*(tf-t)**-1.0
    return rate

#4. Total function for inverse Omori law:
def hyp_total(t, t0, params):
    k=params[0]
    tf=params[1]
    
    total = []
    total = k*(-np.log(tf-t) + np.log(tf-t0))
    return total
    
#########################################
#5. k-value for reparameterized IOL
#Determined using number of events occuring in given time window
def k_rp(times, t0, t1, params):
    tf=params[0]
    p=params[1]
    
    k=[]
    if p==1.0:
        k=-len(times)/(np.log(tf-t1)-np.log(tf-t0))
    else:
        k=-len(times)*(1.-p)/((tf-t1)**(1.-p)-(tf-t0)**(1.-p))
    return k

#########################################
#6. Rate function for Creep model
def creep_rate(t, params):
    k1=params[0]
    c=params[1]
    p1=params[2]
    k2=params[3]
    tf=params[4]
    p2=params[5]
    
    rate = []
    rate = k1*(t+c)**-p1 + k2*(tf-t)**-p2
    return rate

#7. Total function for Creep model, t1 = 0.0
def creep_total(t, t0, params):
    k1=params[0]
    c=params[1]
    p1=params[2]
    k2=params[3]
    tf=params[4]
    p2=params[5]
    
    total = []
    total = k1/(1.-p1)*(((t+c)**(1.-p1))-((t0+c)**(1.-p1))) - k2/(1.-p2)*(((tf-t)**(1.-p2))-((tf-t0)**(1.-p2)))
    return total

#########################################
#define exponential aftershock productivity law
def prod(alpha, m, mc):
    value = np.exp(alpha*(m-mc))
    return value
    