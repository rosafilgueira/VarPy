import sys



from varpy.management import core, conversion
from varpy.data_preparation import window
from varpy.analysis import magnitudes
from numpy import linspace
from varpy.modelling.model_application import experiments
from datetime import date

#For different experiment types...:
#a) retrospective analysis: t_min = value, t_max = value, t_step = None, tf = value

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
tf = '01-01-2013' #Known failure time. If stated, retrospective analysis is used, if None, forecast method is used.

#4
mag_comp = 'GFT' #method for magnitude filtering. 'None' is no filtering

#5
model = 'iol_mle' #name of model to apply. 

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

kwargs={'spatial':'latlon','spatial_x_min':lat_min,'spatial_x_max':lat_max,'spatial_y_min':lon_min,'spatial_y_max':lon_max,'single_attribute':'depth','z_max':z_max, 'z_min':z_min,'mag_comp':mag_comp,'t_min':t_min,'t_max':t_max}

d2=experiments.single_analysis(d1,'ecvd',model,**kwargs)

d2.ecvd.display_models()
