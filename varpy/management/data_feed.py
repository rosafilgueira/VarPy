from varpy.management.import_filters import volc_importers, lab_importers
from varpy.simulation.lab_data import ae_sim
from varpy.simulation.volcanic_data import Eruption_sim, Volcanic_defm_sim, Volcanic_eq_sim

def ecvd( obj1, data_file, metadata_file=None):
    
	#Import metadata from the  meadata_file file, and store it into the object.
	if metadata_file != None: 
		obj1.ecvd.metadata= volc_importers.metadata_imp(metadata_file)

	#Import data from the data_file file, and store it into the object. 
	if obj1.ecvd.metadata['location'] == 'Etna':
		obj1.ecvd.dataset = volc_importers.Etna_ecvd(data_file)
	elif obj1.ecvd.metadata['location'] == 'Hierro':
		obj1.ecvd.dataset = volc_importers.Hierro_ecvd(data_file)
	elif obj1.ecvd.metadata['location'] == 'Hierro_web':
		obj1.ecvd.dataset = volc_importers.Hierro_web_ecvd(data_file)

	#Store the header it into the object.
	obj1.ecvd.header=['datetime','latitude','longitude','depth','magnitude']



def scvd(obj1, data_file, name_station, metadata_file=None):
	# Store the name_station into the object 
	obj1.station=name_station

	# Import metadata from the  meadata_file file, and store it into the object. 
	if metadata_file != None:
		obj1.metadata = volc_importers.metadata_imp( metadata_file)

	#Import data from the data_file file, and store it into the object. 
	if obj1.metadata['location'] == 'Etna':
		obj1.dataset = volc_importers.scvd_Etna_tilt(data_file)
	else:
		print "We need to write the import function for this location"	
	#Store the header it into the object.
	obj1.header=['datetime','tilt']  

def evd(obj1, data_file, metadata_file=None):

	# Import metadata from the  meadata_file file, and store it into the object.
	if metadata_file != None: 
		obj1.evd.metadata= volc_importers.metadata_imp(metadata_file)  

	#Import data from the data_file file, and store it into the object. 
	if obj1.evd.metadata['location'] == 'Etna':
	  obj1.evd.dataset, obj1.evd.eruption_data = volc_importers.Etna_evd(data_file)
	else:  
		print "We need to write the import function for this location"	

	#Store the header it into the object.
	obj1.evd.header=['start_datetime','end_datetime','area','volume'] 



def ecld(obj1, data_file, metadata_file=None):

	# Import metadata from the  meadata_file file, and store it into the object.
	if metadata_file != None: 
		obj1.ecld.metadata = lab_importers.metadata_imp(metadata_file)

	#Import data from the data_file file, and store it into the object. 
	if obj1.ecld.metadata['format'] == 'UCLv1':
	  obj1.ecld.dataset = lab_importers.ecld_UCL_v1(data_file)

	#Store the header it into the object.
	obj1.ecld.header=['datetime', obj1.metadata['size_format']]



def scld(obj1, data_file, metadata_file=None):

	# Import metadata from the  meadata_file file, and store it into the object.
	if metadata_file != None:
		obj1.scld.metadata = lab_importers.metadata_imp(metadata_file)

	#Import data from the data_file file, and store it into the object. 
	if obj1.scld.metadata['format'] == 'UCLv1':
	  obj1.scld.dataset = lab_importers.scld_UCL_v1(data_file)

	#Store the header it into the object.
	obj1.scld.header=['datetime','stress', 'axial_strain', 'porosity']




def iol_sim(obj1,t_start, t_stop, k, t_finish, p, mmin, b):

	#Store the header it into the object.
	obj1.ecvd.header=['datetime','magnitude']
	#Create data and store it into the object
	obj1.ecvd.dataset= eq_sim.IOL_sim(t_start, t_stop, k, tf, p, mmin, b)



def exp_sim(obj1,t_start, t_stop, k, lam, mmin, b):

	#Store the header it into the object.
	obj1.ecvd.header=['datetime','magnitude']
	#Create data and store it into the object
	obj1.ecvd.dataset = eq_sim.Exp_sim(t_start, t_stop, k, lam, mmin, b)



def cr_sim(obj1, t_start, t_stop, rate, mmin, b):

	#Store the header it into the object.
	obj1.ecvd.header=['datetime','magnitude']
	#Create data and store it into the object
	obj1.ecvd.dataset = eq_sim.CR_sim(t_start, t_stop, rate, mmin, b)

def mol_sim(obj1, t_start, t_stop, k, c, p, mmin, b):

	#Store the header it into the object.
	obj1.ecvd.header=['datetime','magnitude']
	#Create data and store it into the object
	obj1.ecvd.dataset = eq_sim.MOL_sim(t_start, t_stop, k, c, p, mmin, b)       

def etas_sim(obj1,t_start, t_stop, mu, alpha, p, c, k, mmin, b):

	#Store the header it into the object.
	obj1.ecvd.header=['datetime','magnitude']
	obj1.ecvd.dataset = etas_sim.etas(t_start, t_stop, mu, alpha, p, c, k, mmin, b)

def volc_quakes_sim(obj1, sim_len, br, m_min, b_value):

	#Store the header it into the object.
	erupt_paras = obj1.evd.extra_data
	obj1.ecvd.header=['datetime','magnitude']
	#Create data and store it into the object
	obj1.ecvd.dataset = Volcanic_eq_sim.volc_quakes(sim_len, br, erupt_paras, m_min, b_value) 

def volc_tilt_sim(obj1, sim_len, tilt_noise, sr):

	#Store the header it into the object.
	erupt_paras = obj1.evd.extra_data
	obj1.scvd.header=['datetime','tilt']
	#Create data and store it into the object
	obj1.scvd.dataset = Volcanic_defm_sim.volc_tilt(sim_len, tilt_noise, erupt_paras, sr)    

def eruption_sim(obj1, sim_len, te, tc_fore, p_fore, k_fore, tc_aft, p_aft, k_aft, t_recharge, k_infl, k_defl):

	#Store the header it into the object.
	obj1.evd.header=['eruption times','erupt_tes','tc_fores','normal dis1','normal dis2','tc_afts','normal dis3','normal dis 4','eruption recharge times','normal dis 5','normal dis6']
	#Create data and store it into the object
	obj1.evd.dataset, obj1.evd.extra_data = Eruption_sim.eruptions(sim_len, te, tc_fore, p_fore, k_fore, tc_aft, p_aft, k_aft, t_recharge, k_infl, k_defl)

def creep_sim_volc(obj1, t_start, t_stop, t0, t1, k1, c, p1, k2, t_finish, p2, mmin, b):

	#Store the header it into the object.
	obj1.ecvd.header=['datetime','magnitude']
	#Create data and store it into the object
	obj1.ecvd.dataset = ae_sim.Creep_sim(t_start, t_stop, t0, t1, k1, c, p1, k2, t_finish, p2, mmin, b)

def creep_incomp_sim_volc(obj1,t_start, t_stop, t0, t1, k1, c, p1, k2, t_finish, p2, mmin, b, b2):

	#Store the header it into the object.
	obj1.ecvd.header=['datetime','magnitude']
	#Create data and store it into the object
	obj1.ecvd.dataset = ae_sim.Creep_Incom_sim(t_start, t_stop, t0, t1, k1, c, p1, k2, t_finish, p2, mmin, b, b2)

def creep_sim_lab(obj1, t_start, t_stop, t0, t1, k1, c, p1, k2, t_finish, p2, mmin, b):

	#Store the header it into the object.
	obj1.ecld.header=['datetime','magnitude']
	#Create data and store it into the object
	obj1.ecld.dataset = ae_sim.Creep_sim(t_start, t_stop, t0, t1, k1, c, p1, k2, t_finish, p2, mmin, b)

def creep_incomp_sim_lab(obj1,t_start, t_stop, t0, t1, k1, c, p1, k2, t_finish, p2, mmin, b, b2):

	#Store the header it into the object.
	obj1.ecld.header=['datetime','magnitude']
	#Create data and store it into the object
	obj1.ecld.dataset = ae_sim.Creep_Incom_sim(t_start, t_stop, t0, t1, k1, c, p1, k2, t_finish, p2, mmin, b, b2)

  
   


  
        


     
