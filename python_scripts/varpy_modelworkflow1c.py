import sys



from varpy.management import core, conversion
from varpy.data_preparation import window
from varpy.analysis import magnitudes
from numpy import linspace
from datetime import date

#For different experiment types...:
#c) retrospective forecast test: t_min = value, t_max = value, t_step = value, tf = None

#specify experiment name, data locations
ID = 'Etna'
ecvd_data_file = '../Library/Etna_INGVCT_C1_99-170214.txt'
ecvd_metadata_file = '../Library/Etna_INGVCT_C1_meta.txt'
#Method variables
#1. Spatial variables
lat_min = 37.5
lat_max = 37.9
lon_min = 14.7
lon_max = 15.3

#2. Depth variables
z_min = -10.0
z_max = 30.0

#3. Time variabl3s
t_min = '01-06-2011' #Could be today, may want to add capability for a "None" option
t_max = '01-01-2013' #Could be in future, may want to add capability for a "None" option
t_step = 1.0 #time between model applications, in days (for ecvd, maybe minutes for ecld?). #If None means single application

#4
mag_comp = 'GFT' #method for magnitude filtering. 'None' is no filtering

#5
model = 'iol_mle' #name of model to apply. Could do many???

#Setup Varpy object
d1 = core.Volcanic(ID)

#Add data to Varpy object
d1.add_datatype('ecvd',ecvd_data_file, ecvd_metadata_file)

#Set-up times to run model
try:
    t_min=conversion.date2int(t_min)
    t_max=conversion.date2int(t_max)
except:
    t_min = float(t_min)
    t_max = float(t_max)
    pass

times = linspace(t_min, t_max, t_step)

#Run forecasts in a loop...
for t_forc in times:
    print "iter"
    print t_forc	 	
    #Maybe update object d1 here????
    #1. Apply spatial filter
    #May need a "None" option here
    d2 = window.latlon(d1, lat_min, lat_max, lon_min, lon_max)
    #2. Apply depth filter
    #May need a "None" option here
    d3 = window.single_attribute(d2, 'depth', z_min, z_max, 'ecvd')

    #3. Select time window
    d4=window.datetime(d3, t_min, t_forc, 'ecvd')

    #4. Determine completeness magnitude, apply magnitude filter, based on "mag_comp" option
    if mag_comp is not None:
        #May need extra options here, e.g. a default value for when catalogue size is small
        if mag_comp is 'maxc':
            mc = magnitudes.mag_completeness(d3).ecvd.outputs['completeness_mag'].mc_maxc
        elif mag_comp is 'GFT':
            mc = magnitudes.mag_completeness(d3).ecvd.outputs['completeness_mag'].Mc_GFT
        elif mag_comp is 'mbs':
            mc = magnitudes.mag_completeness(d3).ecvd.outputs['completeness_mag'].mc_mbs
        else:
            mc = mag_comp
        print "mc is "
	print mc 
        d4 = window.single_attribute(d3, 'magnitude', mc, 10.0, 'ecvd')
    else:
        #Use unfiltered catalogue
        d4 = d3
            
    #5. Apply model to object
    d4.apply_model('ecvd', 'retrospective_forecast', model, t_min, t_forc)
   
    #don't think we need to specify 'retro' etc. here - same functino applies
    

    #6. Analyze/visualize model outputs - to be written
    #Plot graph etc.
######
print "after the loop, all the models"    
d4.ecvd.display_models()
