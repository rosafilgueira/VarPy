from varpy.statistics import mags
from varpy.data_preparation import data_conversion
from collections import namedtuple
import copy

def mag_completeness(obj1):
    """
    Calculates estimates of the earthquake catalogue completeness magnitude.
    
    Calculates completeness magnitudes using:
    * The maximum-curvature method (Maxc)
    * The Goodness-of-Fit test (GFT)
    * The method of b-value stability (mbs)
    
    Args:
        Obj1: A Varpy Var_data class containing event catalogue data
    
    Returns:
        Obj2: A Varpy Var_data class with output defining completeness magnitude
    
    Raises:
    """

    obj2 = copy.deepcopy(obj1)
    if obj2.type == 'volcanic':
        mag_column=obj2.ecvd.header.index('magnitude')
        mag_data = obj2.ecvd.dataset[:,mag_column]
    else: 
        if obj1.ecld.metadata['size_format'] == 'magnitude':
            mag_column=obj2.ecld.header.index('magnitude')
            mag_data = obj2.ecld.dataset[:,mag_column]
        else:
            mag_data = data_conversion.energy_to_magnitude(obj1)
    
    GFT = mags.mc_GFT(mag_data, 0.1, 0.1)
    MBS = mags.mc_mbs(mag_data, 0.1, 0.1)
    
    mc_maxc = mags.mc_maxc(mag_data, 0.1, 0.1)
    mc_GFT = GFT.Mc_GFT
    mc_mbs = MBS.Mc_mbs
    
    Mc = namedtuple('Mc', ['mc_maxc','Mc_GFT','mc_mbs'])
    
    if obj2.type == 'volcanic':
        obj2.ecvd.outputs['completeness_mag']= Mc(mc_maxc,mc_GFT,mc_mbs)  
    else:
        obj2.ecld.outputs['completeness_mag']= Mc(mc_maxc,mc_GFT,mc_mbs)
    
    return obj2

def freq_mag_dist(obj1, method):
    """
    Calculates the maximum-likelihood Gutenberg-Richter b-value and error for an earthquake catalogue.
    
    Applies a completeness threshold of different types:
    * The maximum-curvature method (Maxc)
    * The Goodness-of-Fit test (GFT)
    * The method of b-value stability (mbs)
    
    Args:
        Obj1: A Varpy Var_data class containing event catalogue data
        method (str): The method for determining the completeness magnitude
    
    Returns:
        Obj2: A Varpy Var_data class with output defining the frequency magnitude distribution
    
    Raises:
    """

    obj2 = copy.deepcopy(obj1)
    
    if obj2.type == 'volcanic':
        mag_column=obj2.ecvd.header.index('magnitude')
        mag_data = obj2.ecvd.dataset[:,mag_column]
    else: 
        if obj2.ecld.metadata['size_format'] == 'magnitude':
            mag_column=obj2.ecld.header.index('magnitude')
            mag_data = obj2.ecld.dataset[:,mag_column]
        else:
            mag_data = data_conversion.energy_to_magnitude(obj1)
    
    if method == 'maxc':
        maxc = mags.mc_maxc(mag_data, 0.1, 0.1)
        mc = maxc
    elif method == 'GFT':
        GFT = mags.mc_GFT(mag_data, 0.1, 0.1)
        mc = GFT.Mc_GFT
    elif method == 'mbs':
        MBS = mags.mc_mbs(mag_data ,0.1, 0.1)
        mc = MBS.Mc_mbs
    
    gr_paras = mags.GR_mle(mag_data, mc, 0.1, 0.1)
    
    
    gr_dist = namedtuple('gr_dist', ['b_mle','b_unc','a_mle', 'method'])
    
    if obj2.type == 'volcanic':
        obj2.ecvd.outputs['gr_dist'] = gr_dist(gr_paras[0],gr_paras[1],gr_paras[2], method)  
    else:
        obj2.ecld.outputs['gr_dist'] = gr_dist(gr_paras[0],gr_paras[1],gr_paras[2], method)
    
    return obj2

    
    