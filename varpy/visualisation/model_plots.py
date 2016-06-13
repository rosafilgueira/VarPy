#Function to plot rates of earthquakes leading up to the point of eruptions
import matplotlib.pyplot as plt
from numpy import arange, int, linspace, interp, diff
import copy
from varpy.statistics import rate_funcs
from varpy.management import conversion

# Rosa comment: I have change the functions in order to be able to be used with ecvd and ecld data. 

def iol_total_plot(obj1, data_type , model_name, start, finish):
    try:
        tmin=conversion.date2int(start)
        tmax=conversion.date2int(finish)
    except:
        tmin=start
        tmax=finish
        pass
    
    days = arange(int(tmax-tmin))

    model= getattr(obj1, data_type).models[model_name]

    


    dataset=[]
    for m in model.outputs: 
        dataset.extend(m.dataset)



    fig1 = plt.figure(1, figsize=(8,6))
    ax1 = fig1.add_subplot(111)
    ax2 = ax1.twinx()
    ax2.plot(days+tmin, rate_funcs.iol_total(days, 0.0, dataset[0], dataset[1], dataset[2]), 'r-')
    ax1.set_xlim(tmin, tmax)

    png_name=obj1.figure+'/iol_plot.png'
    eps_name=obj1.figure+'/iol_plot.eps'
    plt.savefig(png_name)
    plt.savefig(eps_name)

    
def hyp_total_plot(obj1, data_type , model_name, start, finish):
    try:
        tmin=conversion.date2int(start)
        tmax=conversion.date2int(finish)
    except:
        tmin=start
        tmax=finish
        pass
    
    days = arange(int(tmax-tmin))

    model= getattr(obj1, data_type).models[model_name]

    dataset=[]
    for m in model.outputs: 
        dataset.extend(m.dataset)

    fig1 = plt.figure(1, figsize=(8,6))
    ax1 = fig1.add_subplot(111)
    ax2 = ax1.twinx()
    ax2.plot(days+tmin, rate_funcs.hyp_total(days, 0.0, dataset[0], dataset[1]), 'b-')
    ax1.set_xlim(tmin, tmax)
    
    png_name=obj1.figure+'/hyp_plot.png'
    eps_name=obj1.figure+'/hyp_plot.eps'
    plt.savefig(png_name)
    plt.savefig(eps_name)

def exp_total_plot(obj1, data_type , model_name, start, finish):
    try:
        tmin=conversion.date2int(start)
        tmax=conversion.date2int(finish)
    except:
        tmin=start
        tmax=finish
        pass
    
    days = arange(int(tmax-tmin))

    model= getattr(obj1, data_type).models[model_name]
    dataset=[]
    for m in model.outputs: 
        dataset.extend(m.dataset)
    #key_list=model.outputs.keys()
    #dataset=[]

    #for key in key_list:
    #    dataset.extend(model.outputs[key].dataset)

    fig1 = plt.figure(1, figsize=(8,6))
    ax1 = fig1.add_subplot(111)
    ax2 = ax1.twinx()
    ax2.plot(days+tmin, rate_funcs.exp_total(days, 0.0, dataset[0], dataset[1]), 'g-')
    ax1.set_xlim(tmin, tmax)
    
    png_name=obj1.figure+'/exp_plot.png'
    eps_name=obj1.figure+'/exp_plot.eps'
    plt.savefig(png_name)
    plt.savefig(eps_name)

# Rosa comment: I am not sure about this method. It is only for scld data ??? what about scvd data ? 
# Can you tell me if, volcanic data are going to use this function ?    
def creep_model_plot(obj1, data_type , model_name, start, finish):

    
    fig1 = plt.figure(1, figsize=(8,5))
    ax1 = fig1.add_subplot(111)
    
    var_column = getattr(obj1,data_type).header.index(variable)
    var_data = getattr(obj1,data_type).dataset[:,var_column]
    var_data = var_data -var_data[0]
    
    dt_column=getattr(obj1,data_type).header.index('datetime')
    dt_data = getattr(obj1,data_type).dataset[:,dt_column]
    dt_data = dt_data - dt_data[0]
    
    times = linspace(dt_data[0],dt_data[-1], num = 501)
    vals = interp(times, dt_data, var_data)
    
    midtimes = times[:-1] + diff(times)/2.
    rates = diff(vals)/diff(times)

    model= getattr(obj1, data_type).models[model_name]

    dataset=[]
    for m in model.outputs: 
        dataset.extend(m.dataset)
    
    
    ax1.plot(midtimes, rates, 'o')
    ax1.plot(midtimes, rate_funcs.creep_rate(midtimes, dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]), 'r-')
    ax1.set_ylabel(variable + ' rate (/s)', fontsize=8)
    
    ax2 = ax1.twinx()
    ax2.plot(dt_data, var_data)
    ax2.plot(times, rate_funcs.creep_total(times, 0.0, dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]), 'r-')
    ax2.set_xlabel('Time (seconds)', fontsize=8)
        
    ax2.set_ylabel(variable, fontsize=8)
    
    ax1.xaxis.set_ticks_position('bottom')
    ax1.set_ylabel('Creep time (Secs)', fontsize=8)

    ax1.set_ylim(rates.min(), rates.max())
    ax2.set_ylim(vals.min(), vals.max())
    
    png_name=obj1.figure+'/creep_plot.png'
    eps_name=obj1.figure+'/creep_plot.eps'
    plt.savefig(png_name)
    plt.savefig(eps_name)