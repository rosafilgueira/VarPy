import sys

from varpy.management import core , data_feed
from varpy.visualisation import rate_plots, mag_plots, model_plots, scatter_plots
from varpy.data_preparation import window
from varpy.modelling.models import varpy_models
from varpy.analysis import magnitudes

ecvd_data_file = './Library/Hierro_IGN_2011-13_v2.txt'
ecvd_metadata_file = './Library/Hierro_ecvd_metadata_v2.txt'
evd_data_file = './Library/Hierro_eruption.txt'
evd_metadata_file = './Library/eruption_metadata.txt'

ID = 'Hierro2'
# Attention:New!
d1 = core.Volcanic(ID)

# The rest is the same ...
d1.add_datatype('ecvd',ecvd_data_file, ecvd_metadata_file)
d1.add_datatype('evd',evd_data_file, evd_metadata_file)

d1.ecvd.info_attribute()
d1.evd.info_attribute()

d1 = window.single_attribute(d1, 'depth', -20, 100.0, 'ecvd','evd')
d1 = window.single_attribute(d1, 'magnitude', 0.0, 10.0, 'ecvd','evd')

mag_plots.mag_mc_plot(d1)
magnitudes.mag_completeness(d1)

d2=window.single_attribute(d1, 'magnitude', 2.5, 10.0, 'ecvd','evd')

start = '05-04-2013'
finish = '26-10-2013'

rate_plots.rate_plot(d2, t_lims=[start,finish], Mc=2.5, t_inc=0.2)

d3=window.datetime(d1, start, finish,'ecvd','evd')


scatter_plots.scatter_plot(d3, 'longitude', colour='magnitude', z_lims=[-1,30], t_lims=[start, finish])

lon_min = -18.06
lon_max = -17.95
lat_min = 27.65
lat_max = 27.82

d4=window.latlon(d3, lat_min, lat_max, lon_min, lon_max,'ecvd', 'evd')

scatter_plots.scatter_plot(d4, 'depth', colour='magnitude', z_lims=[-1,30], t_lims=[start, finish])

magnitudes.mag_completeness(d4)

magnitudes.freq_mag_dist(d4,'mbs')

magnitudes.freq_mag_dist(d4,'GFT')

magnitudes.freq_mag_dist(d4,'maxc')

mag_plots.mag_mc_plot(d4)

# Important: This line gives me problems.
#mag_plots.mf_plot(d4)


d5=window.single_attribute(d4, 'magnitude', 1.1, 10.0,'ecvd','evd')
d6=window.single_attribute(d4, 'magnitude', 1.5, 10.0, 'ecvd','evd')



# Attention: Everything is New!!

d5.apply_model('ecvd','retro','iol_mle',start,finish)
model_plots.iol_total_plot(d5, 'ecvd', 'iol_mle',start, finish)

d5.apply_model('ecvd','retro','hyp_mle',start,finish)
#model_plots.hyp_total_plot(d5, 'ecvd', 'hyp_mle',start, finish)

d5.apply_model('ecvd','retro','exp_mle',start,finish)
#model_plots.exp_total_plot(d5, 'ecvd', 'exp_mle',start, finish)


d5.apply_model('ecvd','retro','cr_mle',start,finish)
d5.ecvd.display_models()



