#Selecting a window of data according to one variable
#How best to do it: several if statements that each call smaller functions?
#Just lots of functions one of which the user can chose?
#Also how to select data if we want this to be generic
#Variables: time window, location circle, location window, depth window, magnitude minimum

from varpy.management import conversion

from numpy import float, logical_and, array
import copy

def latlon(obj1, min_lat, max_lat, min_lon, max_lon, *attributes):
    """
    Performs a latitude-longitude filter on earthquake catalogue data
    
    Args:
        Obj1: A Varpy Volcanic data class containing earthquake catalogue data
        min_lat: minimum latitude of earthquakes to be retained by filter
        max_lat: maximum latitude of earthquakes to be retained by filter
        min_lon: minimum longitude of earthquakes to be retained by filter
        max_lon: maximum longitude of earthquakes to be retained by filter
        attributes: list of attributes (ecvd,scvd ....) which the filter is going to be applied.
    
    Returns:
        Obj2: Varpy volcanic data class with filtered earthquake catalogue
    
    Raises:
    """
    obj2=copy.deepcopy(obj1)
    
    if not attributes:

        if obj2.type == 'volcanic':
                attributes=['ecvd']
        else:

            print "This object is a Laboratory type, and this method can not be applied"
            return



    for atr in attributes: 
    #    if atr != 'scvd' :
        try:
            lat_column=getattr(obj2,atr).header.index('latitude')
            lon_column=getattr(obj2,atr).header.index('longitude')
            
                    #1. By Latitude
                
            getattr(obj2,atr).dataset=  getattr(obj2,atr).dataset[logical_and(getattr(obj2,atr).dataset[:,lat_column]>=min_lat, getattr(obj2,atr).dataset[:,lat_column]<max_lat),:]
                    #2. By Longitude
            getattr(obj2,atr).dataset = getattr(obj2,atr).dataset[logical_and(getattr(obj2,atr).dataset[:,lon_column]>=min_lon, getattr(obj2,atr).dataset[:,lon_column]<max_lon),:]
    
        except:
                print "This object does not have ecvd datatype"
                pass
            #else:
                
            #        for key in obj2.scvd.keys():
            #            try:
            #                lat_column = obj2.scvd[key].header.index('latitude')
            #                lon_column = obj2.scvd[key].header.index('longitude')
    
            #                obj2.scvd[key].dataset=  obj2.scvd[key].dataset[logical_and(obj2.scvd[key].dataset[:,lat_column]>=min_lat, obj2.scvd[key].dataset[:,lat_column]<max_lat),:]
                            #2. By Longitude
            #                obj2.scvd[key].dataset = obj2.scvd[key].dataset[logical_and(obj2.scvd[key].dataset[:,lon_column]>=min_lon, obj2.scvd[key].dataset[:,lon_column]<max_lon),:]
    
            #            except:
            #                pass  
        return obj2

def datetime(obj1, start, finish, *attributes):
    """
    Performs a datetime filter on Varpy var_data class
    
    Args:
        Obj1: A Varpy Volcanic data class containing earthquake catalogue data
        start: start datetime of retained data (number or datetime string)
        finish: finish datetime of retained data (number or datetime string)
        attributes: list of attributes (ecvd,scvd ....) which the filter is going to be applied.
    
    Returns:
        Obj2: Filtered Varpy Var_data class
    
    Raises:
    """
    obj2=copy.deepcopy(obj1)

    if not attributes:

        if obj2.type == 'volcanic':
                attributes=['ecvd','evcd','scvd']
        else:

            attributes=['ecld, scld']

    
    try:
        start=conversion.date2int(start)
        finish=conversion.date2int(finish)
    except:
        start = float(start)
        finish = float(finish)
        pass
    

    for atr in attributes:     

        if atr != 'scvd' :
            try:
                var_column = getattr(obj2,atr).header.index('datetime')
                getattr(obj2,atr).dataset = getattr(obj2,atr).dataset[logical_and(getattr(obj2,atr).dataset[:,var_column]>=start, getattr(obj2,atr).dataset[:,var_column]<finish),:]
              
            except:
                pass

        else:

           
            for key in obj2.scvd.keys():

                try: 
                    var_column = obj2.scvd[key].header.index('datetime')
                    obj2.scvd[key].dataset=obj2.scvd[key].dataset[logical_and(obj2.scvd[key].dataset[:,var_column]>=start, obj2.scvd[key].dataset[:,var_column]<finish),:]
                except:
                    pass

    return obj2

def creep_phase(obj1, *attributes):
    """
    Filters creep experiment laboratory data to reatain only data during the creep phase
    
    Args:
        Obj1: A Varpy Laboratory data class from creep experiment
        attributes: list of attributes (ecvd,scvd ....) which the filter is going to be applied.
    
    Returns:
        Obj2: Filtered Varpy Laboratory data class
       
    
    Raises:
    """
    obj2=copy.deepcopy(obj1)

    if not attributes:

        if obj2.type == 'volcanic':
                attributes=['ecvd','evcd','scvd']
        else:

            attributes=['ecld, scld']


    #Rosa_problem. I don't find exp_type in ULCv1
    #if obj2.datatype == 'laboratory' & obj2.scld.metadata['exp_type'] == 'Creep':
    if obj2.type == 'laboratory' :
    
        try:
            start = float(obj2.scld.metadata['t1'])
            finish = float(obj2.scld.metadata['tf'])
        except:
            start = float(obj2.scld.metadata['t1'])
            finish = obj2.scld.dataset[:,obj2.scld.header=='datetime'].max()
            pass

        try:
            var_column = obj2.ecld.header.index('datetime')
            obj2.ecld.dataset = obj2.ecld.dataset[logical_and(obj2.ecld.dataset[:,var_column]>=start, obj2.ecld.dataset[:,var_column]<finish),:]
        except:
            pass

        try:
            var_column = obj2.scld.header.index('datetime')
            obj2.scld.dataset = obj2.scld.dataset[logical_and(obj2.scld.dataset[:,var_column]>=start, obj2.scld.dataset[:,var_column]<finish),:]
        except:
            pass
        
    else:
        print 'Obj1 does not contain laboratory creep experiment data'

    return obj2


def single_attribute(obj1, variable, minimum, maximum, *attributes):
    """
    Performs a single variable filter on Varpy var_data class
    
    Args:
        Obj1: A Varpy Volcanic data class containing earthquake catalogue data
        variable: the variable by which to filter the data
        minimum: minimum value of variable to be retained by filter
        maximum: maximum value of variable to be retained by filter
        attributes: list of attributes (ecvd,scvd ....) which the filter is going to be applied.
    
    Returns:
        Obj2: Filtered Varpy Var_data class
    
    Raises:
    """

    obj2=copy.deepcopy(obj1)

    if not attributes:

        if obj2.type == 'volcanic':
                attributes=['ecvd','evcd','scvd']
        else:

            attributes=['ecld, scld']

    for atr in attributes:

        if atr != 'scvd':
            if (variable in getattr(obj2,atr).header):
               
                var_column = getattr(obj2,atr).header.index(variable)
                getattr(obj2,atr).dataset = getattr(obj2,atr).dataset[logical_and(getattr(obj2,atr).dataset[:,var_column]>=minimum, getattr(obj2,atr).dataset[:,var_column]<maximum),:]
            else:
               
                pass

        else:

            for key in obj2.scvd.keys():

                  
                if (variable in obj2.scvd[key].header):
                    
                    var_column = obj2.scvd[key].header.index(variable)
                    obj2.scvd[key].dataset=obj2.scvd[name].dataset[logical_and(obj2.scvd[key].dataset[:,var_column]>=minimum, obj2.scvd[key].dataset[:,var_column]<maximum),:]

                else:
                    pass    

        

    return obj2
    

def location_filter(obj1, variable, value, *attributes):
    """
    Performs a filter on a location identifier in location_data
    
    Args:
        Obj1: A Varpy Volcanic data class containing earthquake catalogue data and location_data
        variable: the location variable by which to filter the data
        value: the value of variable to be retained by filter
        attributes: list of attributes (ecvd,scvd ....) which the filter is going to be applied.
    
    Returns:
        Obj2: Filtered Varpy Var_data class
    
    Raises:
    """
    obj2=copy.deepcopy(obj1)

    if not attributes:

        if obj2.type == 'volcanic':
                attributes=['ecvd','evcd','scvd']
        else:

            attributes=['ecld, scld']

    if obj2.type == 'volcanic':
        for atr in attributes :
            if atr != 'scvd':
                try:
                    # ERROR!! does not exit .location_data
                    locations = array(getattr(obj2,atr).location_data)
                    getattr(obj2,atr).dataset = getattr(obj2,atr).dataset[locations[:,0]==value,:]
                    getattr(obj2,atr).location_data = getattr(obj2,atr).location_data[locations[:,0]==value]
                except:
                    pass
            else:
                for key in obj2.scvd.keys():
                    try:
                        location= array(obj2.scvd[key].location_data)
                        obj2.scvd[key].dataset = obj2.scvd[key].dataset[locations[:,0]==value,:]
                        obj2.scvd[key].location_data = obj2.scvd[key].location_data[locations[:,0]==value]
                    except:
                        pass 
                         
    return obj2