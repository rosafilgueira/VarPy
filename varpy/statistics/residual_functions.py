# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 15:43:45 2011

@author: abell5
"""

#Returns residuals for leastsq optmization
from varpy.statistics import rate_funcs

#########################################
def IOL_resids(ps,ts,ys):
    resids = ys - rate_funcs.iol_rate(ts, ps[0], ps[1], ps[2])
    return resids

def IOL_resids_p(ps,ts,ys,p):
    resids = ys - rate_funcs.iol_rate(ts, ps[0], ps[1], p)
    return resids

def iol_resids_tf(ps,ts,ys,tf):
    resids = ys - rate_funcs.iol_rate(ts, ps[0], tf, ps[1])
    return resids

def mol_resids(ps,ts,ys):
    resids = ys - rate_funcs.mol_rate(ts, ps[0], ps[1], ps[2])
    return resids

def Exp_resids(ps,ts,ys):
    resids = ys - rate_funcs.exp_rate(ts, ps[0], ps[1])
    return resids

def Creep_resids(ps, ts, ys):
    resids = ys - rate_funcs.creep_rate(ts, ps[0], ps[1], ps[2], ps[3], ps[4], ps[5])
    return resids

def creep_resids_tf(ps, ts, ys, tf):
    resids = ys - rate_funcs.creep_rate(ts, ps[0], ps[1], ps[2], ps[3], tf, ps[4])
    return resids

def Creep_resids_accel(ps, ts, ys, k1, c, p1):
    resids = ys - rate_funcs.creep_rate(ts, k1, c, p1, ps[0], ps[1], ps[2])
    return resids
