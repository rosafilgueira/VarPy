from varpy.data_preparation import window
from varpy.analysis import magnitudes
from varpy.management import core, conversion
import copy
from numpy import arange, size
from datetime import date, timedelta

def single_analysis(obj1, data_type, model_name, **kwargs):

    obj2=copy.deepcopy(obj1)  
    t_min=kwargs['t_min']
    t_max=kwargs['t_max']
    try:
        t_min = conversion.date2int(t_min)
        t_max = conversion.date2int(t_max)
    except:
        t_min =float(t_min)
        t_max=float(t_max)
            
    if 'spatial' in kwargs:            
        obj2=getattr(window,kwargs['spatial'])(obj2, kwargs['spatial_x_min'], kwargs['spatial_x_max'] , kwargs['spatial_y_min'],kwargs['spatial_y_max'])
    else:
        obj2=obj1
    if 'single_attribute' in kwargs:
        obj2=window.single_attribute(obj2, kwargs['single_attribute'],kwargs['z_min'],kwargs['z_max'], data_type)
    
    obj2=window.datetime(obj2, t_min, t_max, data_type)
   
    #4. Determine completeness magnitude, apply magnitude filter, based on "mag_comp" option
    if 'mag_comp' in kwargs:
    #May need extra options here, e.g. a default value for when catalogue size is small
        if kwargs['mag_comp'] is 'maxc':
            mc = magnitudes.mag_completeness(obj2).ecvd.outputs['completeness_mag'].mc_maxc
        elif kwargs['mag_comp'] is 'GFT':
            mc = magnitudes.mag_completeness(obj2).ecvd.outputs['completeness_mag'].Mc_GFT
        elif kwargs['mag_comp'] is 'mbs':
            mc = magnitudes.mag_completeness(obj2).ecvd.outputs['completeness_mag'].mc_mbs
        else:
            mc = mag_comp
    
        obj2 = window.single_attribute(obj2, 'magnitude', mc, 10.0, data_type)     

    #5. Apply model to object
    if 'tf' in kwargs:
        obj2.apply_model(data_type, 'retrospective_analysis', model_name, t_min, t_max, **kwargs)
    else:
        obj2.apply_model(data_type, 'single_forecast', model_name, t_min, t_max, **kwargs)
    
    return obj2

def multiple_analysis(obj1, data_type, model_name, **kwargs):

    obj2=copy.deepcopy(obj1) 
    
    t_step=kwargs['t_step']
    
    if 't_min' not in kwargs:
        #time limits have not been specified, therefore we are in prospective mode
        t_min = conversion.date2int(date.today().strftime("%d-%m-%Y"))
        t_max_a =date.today() + timedelta(days=100)
        t_max = conversion.date2int(t_max_a.strftime("%d-%m-%Y"))
        model_type='prospective_forecast'
    else:
        t_min=kwargs['t_min']
        t_max=kwargs['t_max']
        model_type='retrosepective_forecast'
        try:
            t_min = conversion.date2int(t_min)
            t_max = conversion.date2int(t_max)
        except:
            t_min =float(t_min)
            t_max=float(t_max)
        
    
    times = arange(t_min, t_max, t_step)

    if 'data_file' in kwargs:
        
        data_file=kwargs['data_file']
       

    for t_forc in times:
    
        if model_type == 'prospective_forecast':
            obj2.update_datatype(data_type,data_file)
            
        if 'spatial' in kwargs:

            obj2=getattr(window,kwargs['spatial'])(obj2, kwargs['spatial_x_min'], kwargs['spatial_x_max'] , kwargs['spatial_y_min'],kwargs['spatial_y_max'])
        else:
            obj2=obj1
            
        if 'single_attribute' in kwargs:
            obj2=window.single_attribute(obj2, kwargs['single_attribute'],kwargs['z_min'],kwargs['z_max'], data_type)
        else:
            obj2=obj1
        
        obj2=window.datetime(obj2,t_min,t_forc, data_type)
        n_events = len(getattr(obj2,data_type).dataset)

        if n_events >= 10:
                
            #4. Determine completeness magnitude, apply magnitude filter, based on "mag_comp" option
            if 'mag_comp' in kwargs:
                if n_events<=50:
                    mc = 0.
                
                else:
                    if kwargs['mag_comp'] is 'maxc':
                        mc = magnitudes.mag_completeness(obj2).ecvd.outputs['completeness_mag'].mc_maxc
                    elif kwargs['mag_comp'] is 'GFT':
                        mc = magnitudes.mag_completeness(obj2).ecvd.outputs['completeness_mag'].Mc_GFT
                    elif kwargs['mag_comp'] is 'mbs':
                        mc = magnitudes.mag_completeness(obj2).ecvd.outputs['completeness_mag'].mc_mbs
                    else:
                        mc = mag_comp
            
                obj2 = window.single_attribute(obj2, 'magnitude', mc, 10.0, data_type)
    
            #5. Apply model to object
            if 'tf' in kwargs:
                obj2.apply_model(data_type, model_type, model_name, t_min, t_forc, **kwargs)
            else:
                obj2.apply_model(data_type, model_type, model_name, t_min, t_forc, **kwargs)
                
            #6. Modify the model output to record the value of mc
                  
            model_output=getattr(obj2,data_type).last_model_output(model_name)
            model_output.t_forc=t_forc
            model_output.mc=mc
            
            getattr(obj2,data_type).update_last_model_output(model_name,model_output)
            
        else:
            pass
        
    return obj2
