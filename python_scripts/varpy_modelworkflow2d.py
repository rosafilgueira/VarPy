import sys



from varpy.management import core, conversion
from varpy.data_preparation import window
from varpy.analysis import magnitudes
from numpy import linspace
from varpy.modelling.model_application import experiments
from datetime import date

#For different experiment types...:
#d) propspective forecast test: t_min = None (today), t_max = None (or future), t_step = value, tf = None

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
t_step = 1.0 #time between model applications, in days (for ecvd, maybe minutes for ecld?). #If None means single application

#4
mag_comp = 'GFT' #method for magnitude filtering. 'None' is no filtering

#5
model = 'iol_mle' #name of model to apply. Could do many???

#Setup Varpy object
d1 = core.Volcanic(ID)

#Add data to Varpy object
d1.add_datatype('ecvd',ecvd_data_file, ecvd_metadata_file)

kwargs={'data_file':ecvd_data_file,'spatial':'latlon','spatial_x_min':lat_min,'spatial_x_max':lat_max,'spatial_y_min':lon_min,'spatial_y_max':lon_max,'single_attribute':'depth','z_max':z_max, 'z_min':z_min,'mag_comp':mag_comp,'t_step':t_step}

d2=experiments.multiple_analysis(d1,'ecvd',model,**kwargs)

d2.ecvd.display_models()
