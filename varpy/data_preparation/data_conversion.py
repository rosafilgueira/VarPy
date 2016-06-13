from varpy.statistics import mags
import copy

def energy_to_magnitude(obj):
    """
    Converts AE energy value to magnitude
    
    Uses simple logarithmic conversion
    
    Args:
        Obj1: A Varpy Var_data class containing event catalogue data with energy values
    
    Returns:
        Magnitudes converted from energy values
    
    Raises:
    """
    #if obj1.ecld.metadata['size_format'] == 'energy1':

