# -*- coding: utf-8 -*-
"""
Created on Mon Feb 07 13:44:11 2011

@author: abell5
"""
import numpy as np
from collections import namedtuple

def mag_prep(mags, m_min, mbin):
    """
    Preparation of a series of earthquake magnitudes.
    
    Trims catalogue to exclude anomolous values (e.g. -999) and rounds to a specified precision
    
    Args:
        mags: a list or 1D array of event magnitudes
        m_min: the value below which to discard values
        mbin: the precision with which to return magnitudes
    
    Returns:
        mags: the prepared 1D array of magnitudes
    """
    mags = mags[mags>=m_min] #remove e.g. anomalous values at 0.0
    mags = np.round((mags+0.00001)/mbin)*mbin #round to required no. dp
    #Added small value is to avoid rounding down at e.g. 1.45
    return mags


def fmd(mags, m_min, mbin):
    """
    Determine the FMD for a series of magnitudes.
    
    Calculates the discrete and cumulative earthquake frequency magnitude distribution.
    
    Args:
        mags: a list or 1D array of event magnitudes
        m_min: the value below which to discard values
        mbin: the precision with which to return magnitudes
    
    Returns:
        fmd: a named tuple consisting of:
            nmags: the number of events
            m_bins: the bin edges for determining earthqauke frequency
            dis_mf: the discrete frequency of earthquakes with m=mi
            cum_mf: the cumulative frequency of earthquakes with m>=mi
    """
    
    mags = mag_prep(mags, m_min, mbin)
    nmags = len(mags)
    minmag = np.min(mags)
    maxmag = np.max(mags)
    m_bins = np.arange(minmag, maxmag, mbin)
    nbins = len(m_bins)
    dis_mf = np.zeros(nbins)
    cum_mf = np.zeros(nbins)
    for i in range(nbins):
        cum_mf[i] = len(mags[mags>m_bins[i]-mbin/2])
    
    dis_mf = np.absolute(np.diff(np.concatenate((cum_mf, [0]), axis=0)))
    
    Fmd = namedtuple('Fmd', ['nmags','m_bins','dis_mf','cum_mf'])
    fmd = Fmd(nmags,m_bins,dis_mf,cum_mf)
    return fmd


def GR_mle(mags, mco, m_min, mbin):
    """
    Calculate the MLE of the GR relation.
    
    Uses Aki's formula to determine the b-value, b-value uncertainty and a-value of the Gutenbrg-Richter relation. 
    Includes the correction for bin width
    
    Args:
        mags: a list or 1D array of event magnitudes
        mco: the magntiude cut-off above and including which to determine the GR parameters
        m_min: the value below which to discard values
        mbin: the precision with which to return magnitudes
        
    Returns:
        gr_paras: a named tuple consisting of:
            b_mle: the MLE of the GR b-value
            b_unc: the uncertainty on the b-value MLE
            a_mle: the MLE of the GR a-value
    """
    
    mags = mag_prep(mags, m_min, mbin)
    mags = mags[mags>=mco]
    nbev = len(mags)
    b_mle = np.log10(np.exp(1))/(np.mean(mags)-(mco-mbin/2))
    b_unc = (2.3*b_mle**2)*np.sqrt(np.sum((mags-np.mean(mags))**2)/(nbev*(nbev-1)))
    a_mle = np.log10(nbev) + b_mle*mco 
    #What is expression for a_unc?
    #note - b-value error estimate using this expression (from Shi & Bolt) is not correct...
    
    GR_paras = namedtuple('GR_paras', ['b_mle','b_unc','a_mle'])
    gr_paras = GR_paras(b_mle,b_unc,a_mle)
    return gr_paras
    
 
def GR_dist(m_bins, a_value, b_value):
    """
    Determine the expected FMD for a given GR distribution.
    
    Calculates the discrete and cumulative earthquake frequency magnitude distribution expected for GR parameters.
    
    Args:
         m_bins: the bin edges for determining earthqauke frequency (output of fmd)
         a_value: the GR a-value
         b_value: the GR b-value
    
    Returns:
        GR_dist: a named tuple consisting of:
            GR_dis: the discrete frequency of earthquakes with m=mi
            GR_cum: the cumulative frequency of earthquakes with m>=mi
    """
    
    GR_cum = 10**(a_value-b_value*m_bins)
    GR_dis = np.absolute(np.diff(np.concatenate((GR_cum, [0]), axis=0)))
    
    GR_dist = namedtuple('GR_dist', ['GR_cum','GR_dis'])
    gr_dist = GR_dist(GR_cum,GR_dis)    
    return gr_dist


def gr_mags(n, b_value, m_min):
    """
    Generate a series of magnitudes according to GR distribution
    
    Args:
        n: the number of magnitudes
        b_value: the GR b-value
        m_min: the minimum magnitude threshold or cut-off
        
    Returns:
        ms: a 1D array of magnitudes
    """
    
    rng = np.random.RandomState()
    rng.seed
    ms = m_min -0.05 + rng.exponential(1.0/(b_value/np.log10(np.e)), n)
    return ms


def incomp_mags(n, slope, mc):
    """
    Generate a series of magnitudes according to an "inverse" GR distribution to simulate incompleteness
    
    Args:
        n: the number of magnitudes
        slope: the "inverse" GR b-value
        mc: the maximum magnitude threshold or cut-off
        
    Returns:
        ms: a 1D array of magnitudes
    """
    rng = np.random.RandomState()
    rng.seed
    ms = mc-0.05 - rng.exponential(1.0/(slope/np.log10(np.e)), n)
    return ms


def mc_maxc(mags, m_min, mbin):
    """
    Calculates the catalogue completeness magnitude by the Maximum-curvature method
    
    Args:
        mags: a list or 1D array of event magnitudes
        m_min: the value below which to discard values
        mbin: the precision at which to analyze magnitudes
    
    Returns:
        mc: the maximum-curvature completeness magnitude
    """
    mags = mag_prep(mags, m_min, mbin)
    FMD = fmd(mags, m_min, mbin)
    mc = FMD.m_bins[FMD.dis_mf==np.max(FMD.dis_mf)]
    mc = mc[0]
    return mc


def mc_GFT(mags, m_min, mbin):
    """
    Calculates the catalogue completeness magnitude by the Goodness of fit test (after Wiemer and Wyss, 2000)
    
    Args:
        mags: a list or 1D array of event magnitudes
        m_min: the value below which to discard values
        mbin: the precision at which to analyze magnitudes
    
    Returns:
        gft: a named tuple consisting of:
            Mc_GFT: the Goodness of fit test completeness magnitude
            best: the method used to determine Mc
            Mco: a 1D array of cut-off magnitudes
            R: a 1D array of R values at those cut-off magnitudes
    """
    mags = mag_prep(mags, m_min, mbin)
    mag_max = mags.max()
    
    FMD = fmd(mags, m_min, mbin)
    
    maxc_mc = mc_maxc(mags, m_min, mbin)
    Mco = maxc_mc+np.arange(-0.4,2.0,mbin)
    Mco = Mco[Mco<(mag_max-2.*mbin)]
    
    n_R = len(Mco)
    R = np.ones(n_R)*100.
    
    for i in range(n_R):
        mags_sel = mags[mags>Mco[i]-mbin/2]
        GR_paras = GR_mle(mags_sel, Mco[i], m_min, mbin)
        cum_model = GR_dist(FMD.m_bins, GR_paras.a_mle, GR_paras.b_mle)
        R[i] = np.sum(np.abs(FMD.cum_mf[FMD.m_bins>=Mco[i]]-cum_model.GR_cum[FMD.m_bins>=Mco[i]]))/np.sum(FMD.cum_mf[FMD.m_bins>=Mco[i]])*100
    
    logic_GFT = R<=5
    if np.any(logic_GFT):
        Mco_sel = Mco[logic_GFT]
        Mc_GFT = Mco_sel[0]
        best = '95%'
        
    else:
        logic_GFT = R<=10
        if np.any(logic_GFT):
            Mco_sel = Mco[logic_GFT]
            Mc_GFT = Mco_sel[0]
            best = '90%'
        else:
            Mc_GFT = maxc_mc
            best = 'Maxc'

    GFT = namedtuple('GFT', ['Mc_GFT','best', 'Mco', 'R'])
    gft = GFT(Mc_GFT,best,Mco,R)        
    
    return gft


def mc_mbs(mags, m_min, mbin):
    """
    Calculates the catalogue completeness magnitude by the method of b-value stability
    
    Args:
        mags: a list or 1D array of event magnitudes
        m_min: the value below which to discard values
        mbin: the precision at which to analyze magnitudes
    
    Returns:
        mbs: a named tuple consisting of:
            Mc_mbs: the b-val stability completeness magnitude
            Mco: a 1D array of cut-off magnitudes
            bi: the b-value at each of those cut-off magnitudes
            unc: the b-value uncertainty at each of those cut-off magnitudes
            bave: the b-value averaged over the succeeding 5 Mcos
    """
    mags = mag_prep(mags, m_min, mbin)
    maxc_mc = mc_maxc(mags, m_min, mbin)
    mag_max = mags.max()
    
    Mco = maxc_mc+np.arange(-0.7,2.0,mbin)
    Mco = Mco[Mco<(mag_max-2.*mbin)]
    n_bs = len(Mco)
    bi = np.zeros(n_bs)
    unc = np.zeros(n_bs)
    
    for i in range(n_bs):
        mags_sel = mags[mags>Mco[i]-mbin/2]
        GR_paras = GR_mle(mags_sel, Mco[i], m_min, mbin)
        bi[i] = GR_paras.b_mle
        unc[i] = GR_paras.b_unc
    
    bave = np.zeros(n_bs-5)
    for i in range(n_bs-5):
        bave[i] = np.mean(bi[i:i+5])
    
    dbi = np.abs(bave-bi[0:n_bs-5])
    logic_dbi = dbi<=unc[0:n_bs-5]
    Mco_sel = Mco[logic_dbi]
    if len(Mco_sel)>0:
        Mc_mbs = Mco_sel[0]
    else:
        Mc_mbs = maxc_mc
    
    MBS = namedtuple('MBS', ['Mc_mbs', 'Mco', 'bi', 'unc', 'bave'])
    mbs = MBS(Mc_mbs,Mco,bi,unc,bave)
    
    return mbs