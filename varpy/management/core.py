import os
import shutil

from varpy.simulation.earthquake_data import eq_sim, etas_sim
from varpy.simulation.lab_data import ae_sim
from varpy.simulation.volcanic_data import Eruption_sim, Volcanic_defm_sim, Volcanic_eq_sim
from varpy.management.import_filters import volc_importers, lab_importers
from varpy.modelling.models import MLE_retro_models, MLE_rate_models, MLE_forecast_models, LSQ_retro_models
from varpy.management import data_feed, user_data_feed, conversion
from datetime import datetime
from varpy.modelling.models import varpy_models, user_models

###################### Rosa 1
class Var_Data():
    #Define core functions for volcanic and Rock physics data
    def __init__(self):      
            raise NotImplementedError('This class is non-instantable')
    def __var_data(self,ID):
        """
        Private_Method. Initialize some attributes of the object.
        
        Args:
            self: A Varpy Var_Data object
         
        Raises:
        """
        self.id=ID
        self.figure= './'+ self.id + '/Figure'
        self.output= './'+ self.id + '/Output'
        self.result={}
        self.type=''

        self.__remove_environment()
        self.__setup_environment()    
    
    def __remove_environment(self):
        """
        Private_Method. Remove the environment of the project.
        
        Args:
            self: A Varpy Var_Data object
         
        Raises:
         """
        if os.path.exists( './'+self.id +'/Data'):
            shutil.rmtree( './'+self.id +'/Data')
        if os.path.exists( self.output):
            shutil.rmtree( self.output)
        if os.path.exists( self.figure):
            shutil.rmtree( self.figure)
        if os.path.exists( './'+self.id +'/Metadata'):
            shutil.rmtree( './'+self.id +'/Metadata')
    
    def __setup_environment(self):
        """
        Private_Method. Set up the environment of the project.
        
        Args:
            self: A Varpy Var_Data object
         
        Raises:
        """
        if not os.path.exists( './'+self.id +'/Data'):
            os.makedirs( './'+self.id +'/Data')
        if not os.path.exists(self.output):
            os.makedirs(self.output)
        if not os.path.exists(self.figure):
            os.makedirs( self.figure)
        if not os.path.exists('./'+self.id +'/Metadata'):
            	os.makedirs('./'+self.id +'/Metadata')

    def display_result(self):
        """
        Display the result attribute of the object.
        
        Args:
            self: A Varpy Var_Data object
         
        Raise
        """
        print self.result

    def sim_datatype(self,data_type,simulator_name, *paras): 
        """
        Simulate the data_type data. 
        
        Args:
            self: A Varpy Var_data object
            data_type: the datatype name that you want to simulate, e.g 'scvd', or 'ecvd' ...
            simulator_name: It is the name of the simulator
            *paras: It is a list of the input parameters for the simulator
        
        
        Raises:
        """ 

        setattr(self,data_type,Generic_Data(data_type))
        
        try:
            getattr(data_feed,simulator_name)(self,*paras)
        except:
            getattr(user_data_feed,simulator_name)(self,*paras) 

    def __add_datatype(self,data_type, data_file, metadata_file, name_station=None):
        """
        Private method. Add an datatype to the object. The datatype could be: ecvd, scvd, evc, scld, ecld
        
        Args:
            self: A Varpy Var_data object
            data_type: the datatype name that you want to add to the object (ecld, scld, ecvd, evd, scvd)
            data_file: the file name which stores the data
            metadata_file: the file name which describes the data stored in data_file
            name_station: the name of the station. Only relevant for "scvd" data_type
        
        
        Raises:
        """
        
        
        setattr(self,data_type,Generic_Data(data_type))

        shutil.copy(data_file,'./'+self.id+'/Data/'+ data_type+'_data.txt')
        shutil.copy(metadata_file,'./'+self.id+'/Metadata/'+data_type+'_metadata.txt')

        getattr(data_feed,data_type)(self, data_file, metadata_file)


    def __apply_model(self, data_type, model_type, model_name, start, finish, tf=None, name_station=None, *paras):
        """
        Private Method. Application of model to the "data_type"  of the object. 
        
        Args:
            self: A Varpy Var_data object
            data_type: the datatype name to which to apply the model (ecvd, scvd, ecld, scld)
            model_type: the model type: retrosepective model fit, prospective model fit or real time (series of prospective model fits)
            model_name: The name of the model to apply. 
            start: the datetime of the start of the modelled period
            finish: the datetime of the finish of the modelled period
            tf: the failure or eruption time
        
        
        Raises:
        """
        
        try:
            tmin=conversion.date2int(start)
            tmax=conversion.date2int(finish)
        except:
            tmin=start
            tmax=finish
            pass
        
        
        #New_Rosa: First of all, we get the current time.     
        current_time=str(datetime.now())    
        #New_Rosa: Then, we check if we have already this model in our dictionary of models.
        #In case not, a new key-value is appended to the self.data_type.models dictionary, where the key is the model_name. 

        getattr(self,data_type).add_model_list(model_name,model_type)

        try:
            #New_Rosa: Later, a new Model_Output object is created for storing later the outputs of the model. 
            m1_output=Model_Output()
       
            #New_Rosa: Once the Model_Output is created, the model (which name is stored in model_name) is applied, and the outputs are stored in the Model_Output object. 
            getattr(varpy_models,model_name)(self, data_type, m1_output, tmin, tmax, tf, paras)
            
            getattr(self,data_type).models[model_name].update_model(m1_output)
            
            
            
        except:  
            #New_Rosa: If not, I assume that the function is inside of user_models.py module, and the function is called directly with those arguments
            #m1_output=getattr(user_models,model_name)(self, data_type, m1_output, tmin, tmax, tf, paras)
            #getattr(self,data_type).models[model_name].update_model(m1_output)
            pass
    
           
    
               

# New_Rosa: I have create this class to represent a model
class Model():
    def __init__(self, modeltype):
        #--- input parameters        
        self.type=modeltype # It is to store the type of model: retrosepective model fit, prospective model fit or real time (series of prospective model fits)
        self.outputs=[]

        
    def update_model(self, model_output):
        """
        Update the outputs dicitionary of the object.
        
        Args:
            self: A Varpy Model object
            model_output: It is the result to apply a model to the object in a specific time.
            It is going to be the value of the dicitionary. 
        
        
        Raises:
        """
        
        self.outputs.append(model_output)


       


class Model_Output():
    def __init__(self):

        self.metadata=[]
        self.dataset=[]
        self.starting_parameters={}
        self.ll=None
        self.ft=None

    def display_model_outputs(self):
        """
        Display the outputs (dataset, ll, ft, starting_parameters) of a model.
        
        Args:
            self: A Varpy Model_Output object
         
        Raises:
        """
        print "dataset:"
        print self.dataset
        print "metadata:"
        print self.metadata
        print "ll:"
        print self.ll
        print "ft:"
        print self.ft
        print "starting parameters"
        for key, value in self.starting_parameters.iteritems() :
            print key, value     

         
   



#New_Rosa: I have modified Generic_Data in order to be able to store the models. 
###################### 
class Generic_Data():
    #Define core functinos for generic data
    def __init__(self,type):
        self.dataset=[]
        self.metadata={}
        self.header=[]
        self.extra_data=[]
        self.outputs={}
        self.models={} # New_Rosa: it is a dictionary of 'object Models'. Initialy, it is empty. Only when a user calls to a model ( for example, apply_model('ecvd','retro','iol_mle', ...)), a new object model is appended to this list. The key is the name of the model. The value is Model object. 
        self.type=type # New_Rosa: it is for storing the type of data. It could be: ecvd, scvd, evd, ecld or scld. Only can be one of those values. 
        self.selection_parameters=[] # New:_Rosa Criteria which the object has been filtered/ cut / like Depth, longitude, .... could be more than 1. Right now, I am not using this for nothing ....
        self.eruption_data=[] # New_Rosa: I do this because seems that it is needed in 'evd function' in data_feed.py model
        #self.location=[]. New_Rosa: Should we have this parameter ??
    
    def display_models(self):
        """
        
        Displays the model dictionary of the object-attribute. 
        Args:
            self: A Varpy Generic_data object
        Raises:
        """
        for model in self.models.keys():
                print "model name: " + model
                m1=self.models[model]
                print "model type: " + m1.type 
                print "model outputs:"
                for m in m1.outputs:
                    m.display_model_outputs();
                print "- - - - -"
       
                 
    
   
    def add_model_list(self, model_name, modeltype):   
        """
        Add a new key-value to the self.models dicitonary, in case that the "model_name" is not already in the dicitonary.
        Remember, the key of the self.models dicitonary is the name of the model ("model_name"), and the value is an "Model" object  
        
        Args:
            self: A Varpy Generic_data object
            model_type: the model type: retrosepective model fit, prospective model fit or real time (series of prospective model fits)
            model_name: The name of the model to apply. 
         
        Raises:                  
        """
        if model_name not in self.models.keys():

            self.models[model_name]=Model(modeltype)

        else:
            pass

    def info_attribute(self):
        """
        Display the metadata of a generic_data object
       
        Args:
            self: A Varpy Generic_data object
           
         
        Raises:                  
        """
        print "datatype:" + self.type
        #print self.dataset
        print self.metadata
        print "------"
        #print self.header
        #print self.extra_data

    def info_models(self):
        """
        Display the name of models applied of a generic_data object
       
        Args:
            self: A Varpy Generic_data object
           
         
        Raises:                  
        """

        for name in self.models.keys():
            print name



######################        
# Rosa comment: New class for represent any type of Volcanic data ( Real or Synthetic)
class Volcanic(Var_Data):
    def __init__(self,ID):
        self._Var_Data__var_data(ID)
        
        self.type='volcanic'
        self.scvd={}
        self.ecvd= None
        self.evd= None

    
    def display_datatypes(self):
        """
        Display the datatypes of a Volcanic object
       
        Args:
            self: A Varpy Volcanic object
           
         
        Raises:                  
        """  
        self.ecvd.info_attribute()
        self.evd.info_attribute()
        for key in self.scvd:
            print key
            self.scvd[key].info_attribute()

    def add_datatype(self,data_type, data_file, metadata_file, name_station=None):
        """
        Add an datatype to the object. 
        If the datatype is ecvd, or evc, the __add_datatype method from Var_Data class is called.
        If the datatype is scvd, then a new Generic_Data is created, and added to the self.scvd
        dicitonary. Then, the __add_datatype method from Var_Data class is called. Finally, the self.scvd dicitonary is
        updated. 
        
        Args:
            self: A Varpy Volcanic object
            data_type: the datatype name that you want to add to the object (ecvd, evd or scvd)
            data_file: the file name which stores the data
            metadata_file: the file name which describes the data stored in data_file
            name_station: the name of the station. Only relevant for "scvd" data_type
        
        
        Raises:
        """
        
        if data_type == 'ecvd' or data_type == 'evd': 
             self._Var_Data__add_datatype(data_type, data_file, metadata_file, name_station) 
            
        elif data_type =='scvd':

            obj2=Generic_Data('scvd')
            shutil.copy(metadata_file,'./'+self.id+'/Data/scvd'+name_station+'_data.txt')
            shutil.copy(metadata_file,'./'+self.id+'/Metadata/scvd'+name_station+'_metadata.txt')
          
            getattr(data_feed,data_type)(obj2, data_file, metadata_file, name_station)
           
            self.scvd[name_station]=obj2
        
        else:
            print "We do not support " + data_type

    
    def apply_model(self, data_type, model_type, model_name, start, finish, tf=None, name_station=None, *paras):
        """
        Application of model to one datatype of the object. 
        The __apply_model method from Var_Data class is called
        
        Args:
            self: A Varpy Volcanic object
            data_type: the datatype name to which to apply the model (ecvd, scvd or evd)
            model_type: the model type: retrosepective model fit, prospective model fit or real time (series of prospective model fits)
            model_name: The name of the model to apply. 
            start: the datetime of the start of the modelled period
            finish: the datetime of the finish of the modelled period
            tf: the failure or eruption time
        
        
        Raises:
        """ 


        if data_type == 'ecvd' or data_type == 'evd':  

            if getattr(self, data_type) == None : 
                print "the " + data_type +" datatype does not have any data"  
                
            else:
                   
                 self._Var_Data__apply_model(data_type, model_type, model_name, start, finish, tf, name_station, *paras)

        elif data_type == 'scvd':
            if len(self.scvd) == 0 :
                print "the " + data_type +" datatype does not have any data"  

            else :
                # Question: Should we apply a model, to the scvd data of a specif station ?
                # self.scvd[name_station] ??? 
                self.scvd[name_station]._Var_Data__apply_model(data_type, model_type, model_name, start, finish, tf, name_station, *paras) 
        else:

            print "Error in the attribute " + "datatype"


class Laboratory(Var_Data):
    #Rosa comment: New class for representing any type of Laboratory data (Real or Synthetic)
    def __init__(self,ID):
        self._Var_Data__var_data(ID)
        self.type='laboratory'
        self.scld = None
        self.ecld= None
     
        
    def display_datatypes(self):
        self.ecld.info_attribute()
        self.scld.info_attribute()
        
    
    def add_datatype(self,data_type, data_file, metadata_file, name_station=None):
        """
        Add an datatype to the object. 
        The __add_datatype method from Var_Data class is called.
        
        Args:
            self: A Varpy Laboratory object
            data_type: the datatype name that you want to add to the object (ecld or scld)
            data_file: the file name which stores the data
            metadata_file: the file name which describes the data stored in data_file
            name_station: None
        
        
        Raises:
        """
        
        
        if data_type == 'ecld' or data_type == 'scld': 
           
            self._Var_Data__add_datatype(data_type, data_file, metadata_file) 
        else:
            print "We do not support " + data_type

    def apply_model(self, data_type, model_type, model_name, start, finish, tf=None, name_station=None, *paras):
        """
        Application of model to the "data_type" of the object. 
        The __apply_model method from Var_Data class is called. 
        
        Args:
            self: A Varpy Laboratory object
            data_type: the datatype name to which to apply the model (ecld or scld)
            model_type: the model type: retrosepective model fit, prospective model fit or real time (series of prospective model fits)
            model_name: The name of the model to apply. 
            start: the datetime of the start of the modelled period
            finish: the datetime of the finish of the modelled period
            tf: the failure or eruption time
        
        
        Raises:
        """  


        if data_type == 'ecld' or data_type == 'scld': 

            if getattr(self, data_type) == None : 
                print "the " + data_type +" datatype does not have any data"  
                
            else:

                self._Var_Data__apply_model(data_type, model_type, model_name, start, finish, tf, name_station, *paras) 

        else:

            print "Error in the datatype " + "data_type"       
             
     


  
