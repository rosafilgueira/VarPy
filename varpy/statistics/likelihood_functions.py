# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 15:43:45 2011

@author: abell5
"""

#Returns negative log likelihood functions for point process models

import numpy as np

#########################################
#1. neg_ll for exponential rate increase:
#rate = k.exp(lambda.t)
def exp_negll(paras, t0,t1,times):
    #paras are [k, lamda]
    #t0, t1 are start and end of data
    #times are observed earthquake times

    np.seterr(all='ignore') #Errors caught and set to large value
    neg_ll = []
    
    f1 = len(times)*np.log(paras[0]) + paras[1]*np.sum(times)
    
    f2 = -paras[0]/paras[1]*(np.exp(paras[1]*t1)-np.exp(paras[1]*t0))
     
    neg_ll = -(f1 + f2)
    
    if np.isnan(neg_ll) or np.isinf(neg_ll):
        neg_ll = 10**15
    
    return neg_ll

#####################################
#2a. neg_ll for IOL, Ogata's method
#All paras unknown
def iol_negll_og(paras, t0, t1, times):
    #paras are [k, tf, p]
    #t0, t1 are start and end of data
    #times are observed earthquake times

    np.seterr(all='ignore') #Errors caught and set to large value
    neg_ll = []

    f1 = np.sum(np.log(paras[0]*((paras[1]-times)**-paras[2])))
    
    if paras[2] == 1:
        sasump = -np.log(paras[1]-t1) + np.log(paras[1]-t0)
    else:
        sasump = -1.0/(1.-paras[2]) * ((paras[1]-t1)**(1.-paras[2]) - (paras[1]-t0)**(1.-paras[2]))
    
    neg_ll = -(f1 - paras[0]*sasump)
    
    if np.isnan(neg_ll) or np.isinf(neg_ll):
        neg_ll = 10**15
    
    return neg_ll

#2b. neg_ll for IOL, Ogata's method
#tf known a priori
def iol_negll_og_tf(paras, tf, t0, t1, times):
    #paras are [k, p]
    #t0, t1 are start and end of data
    #times are observed earthquake times
    
    np.seterr(all='ignore') #Errors caught and set to large value
    neg_ll = []
    
    f1 = np.sum(np.log(paras[0]*((tf-times)**-paras[1])))
    
    if paras[1] == 1:
        sasump = -np.log(tf-t1) + np.log(tf-t0)
    else:
        sasump = -1.0/(1.-paras[1]) * ((tf-t1)**(1.-paras[1]) - (tf-t0)**(1.-paras[1]))
    
    neg_ll = -(f1 - paras[0]*sasump)
    
    if np.isnan(neg_ll) or np.isinf(neg_ll):
        neg_ll = 10**15
    
    return neg_ll

#2b. neg_ll for IOL, Ogata's method
#p known a priori
def hyp_negll(paras, t0, t1, times):
    #paras are [k, tf]
    #t0, t1 are start and end of data
    #times are observed earthquake times
    
    np.seterr(all='ignore') #Errors caught and set to large value
    neg_ll = []
    f1 = np.sum(np.log(paras[0]*((paras[1]-times)**-1.)))
    
    sasump = -np.log(paras[1]-t1) + np.log(paras[1]-t0)
    
    neg_ll = -(f1 - paras[0]*sasump)
    
    if np.isnan(neg_ll) or np.isinf(neg_ll):
        neg_ll = 10**15
    
    return neg_ll

###################################
#3a. neg_ll for IOL, reparameterized method
#All paras unknown
def iol_negll_rp(paras, t0, t1, times):
    #paras are [tf, p]
    #t0, t1 are start and end of data
    #times are observed earthquake times
    
    np.seterr(all='ignore') #Errors caught and set to large value
    neg_ll = []
    f1 = len(times)*np.log(D(t0, t1, paras[0], paras[1]))
    f2 = paras[1]*np.sum(np.log((1-times/paras[0])))
    
    neg_ll = -f1 + f2
    
    if np.isnan(neg_ll) or np.isinf(neg_ll):
        neg_ll = 10**15
    
    return neg_ll

#3b. neg_ll for IOL, reparameterized method
#tf known a priori
def iol_negll_rp_tf(paras, tf, t0, t1, times):
    #paras are [p]
    #t0, t1 are start and end of data
    #times are observed earthquake times
    
    np.seterr(all='ignore') #Errors caught and set to large value
    neg_ll = []
    f1 = len(times)*np.log(D(t0, t1, tf, paras[0]))
    f2 =  paras[0]*np.sum(np.log((1-times/tf)))
    
    neg_ll = -f1 + f2
    
    if np.isnan(neg_ll) or np.isinf(neg_ll):
        neg_ll = 10**15
    
    return neg_ll
    
#4. D function for reparameterized IOL
def D(t_start, t_stop, tf, p):
    val = []
    np.seterr(all='ignore') #Errors caught and set to large value
    if p == 1.0:
        val = -(1.0/tf)/((np.log(1-t_stop/tf)) - (np.log(1-t_start/tf)))
    else:
        val = -((1.0-p)/tf)/(((1-t_stop/tf)**(1-p)) - ((1-t_start/tf)**(1-p)))
    
    return val
    
    
###################################
#5. Constant rate model
#rate = lambda
def cr_negll(lam, t0, t1, times):
    np.seterr(all='ignore') #Errors caught and set to large value
    neg_ll = []
    neg_ll = -(len(times)*np.log(lam) - lam*(t1-t0))

    return neg_ll

###################################
#2b. neg_ll for IOL, Ogata's method
#all parameters unknown
def creep_negll(paras, t0, t1, times):
    #paras are [k1, c, p1, k2, tf, p2]
    #t0, t1 are start and end of data
    #times are observed earthquake times
    
    np.seterr(all='ignore') #Errors caught and set to large value
    neg_ll = []
    f1 = np.sum(np.log(paras[0]*((times + paras[1])**-paras[2]) + paras[3]*((paras[4]-times)**-paras[5])))
    
    if paras[1] == 1:
        sasump = paras[0]*(np.log(t1+paras[1]) + np.log(t0+paras[1])) + paras[3]*(-np.log(paras[4]-t1) + np.log(paras[4]-t0))
    else:
        sasump = (paras[0]/(1-paras[2]) * ((t1+paras[1])**(1-paras[2]) - (t0+paras[1])**(1-paras[2]))) + (-paras[3]/(1-paras[5]) * ((paras[4]-t1)**(1-paras[5]) - (paras[4]-t0)**(1-paras[5])))
    
    neg_ll = -(f1 - sasump)
    
    if np.isnan(neg_ll) or np.isinf(neg_ll):
        neg_ll = 10**15
    
    return neg_ll

#tf known a priori
def creep_negll_tf(paras, tf, t0, t1, times):
    #paras are [k1, c, p1, k2, p2]
    #t0, t1 are start and end of data
    #times are observed earthquake times
    
    np.seterr(all='ignore') #Errors caught and set to large value
    neg_ll = []
    f1 = np.sum(np.log(paras[0]*((times + paras[1])**-paras[2]) + paras[3]*((tf-times)**-paras[4])))
    
    if paras[1] == 1:
        sasump = paras[0]*(np.log(t1+paras[1]) + np.log(t0+paras[1])) + paras[3]*(-np.log(tf-t1) + np.log(tf-t0))
    else:
        sasump = (paras[0]/(1-paras[2]) * ((t1+paras[1])**(1-paras[2]) - (t0+paras[1])**(1-paras[2]))) + (-paras[3]/(1-paras[4]) * ((tf-t1)**(1-paras[4]) - (tf-t0)**(1-paras[4])))
    
    neg_ll = -(f1 - sasump)
    
    if np.isnan(neg_ll) or np.isinf(neg_ll):
        neg_ll = 10**15
    
    return neg_ll
    
#parameters of transient phase known a priori
def creep_negll_accel(paras, k1, c, p1, t0, t1, times):
    #paras are [k2, tf, p2]
    #t0, t1 are start and end of data
    #times are observed earthquake times
    
    np.seterr(all='ignore') #Errors caught and set to large value
    neg_ll = []
    f1 = np.sum(np.log(k1*((times+c)**-p1) + paras[0]*((paras[1]-times)**-paras[2])))
    
    if paras[2] == 1: #need to rewrite for two different ps
        sasump = k1*(np.log(t1+c) + np.log(t0+c)) + paras[0]*(-np.log(paras[1]-t1) + np.log(paras[1]-t0))
    else:
        sasump = (k1/(1-p1)*((t1+c)**(1-p1)-(t0+c)**(1-p1))) + (-paras[0]/(1-paras[2])*((paras[1]-t1)**(1-paras[2])-(paras[1]-t0)**(1-paras[2])))
    
    neg_ll = -(f1 - sasump)
    
    if np.isnan(neg_ll) or np.isinf(neg_ll):
        neg_ll = 10**15
    
    return neg_ll

######################################
#2neg_ll for MOL, Ogata's method
#All paras unknown
def mol_negll_og(paras, t0, t1, times):
    #paras are [k, c, p]
    #t0, t1 are start and end of data
    #times are observed earthquake times
    
    np.seterr(all='ignore') #Errors caught and set to large value
    neg_ll = []
    f1 = np.sum(np.log(paras[0]*((times+paras[1])**-paras[2])))
    
    if paras[2] == 1:
        sasump = np.log(t1+paras[1]) - np.log(t0+paras[1])
    else:
        sasump = 1.0/(1-paras[2]) * ((t1+paras[1])**(1-paras[2]) - (t0+paras[1])**(1-paras[2]))
    
    neg_ll = -(f1 - paras[0]*sasump)
    
    if np.isnan(neg_ll) or np.isinf(neg_ll):
        neg_ll = 10**15
    
    return neg_ll