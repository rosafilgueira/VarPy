import pickle

def write_median_dates(obj1):
	fileobj1=open(obj1.output+'/Median_dates(fromt0).txt','w')
	pickle.dump(obj1.result['med_date'],fileobj1)
	fileobj1.close()

def write_average_quakes(obj1):
	fileobj1=open(obj1.output+'/Average_quakes_per_day.txt','w')
	pickle.dump(obj1.result['points'],fileobj1)
	fileobj1.close()

def write_daily_quakes(obj1):
	fileobj1=open(obj1.output+'/Earthquakes_per_day.txt','w')
	pickle.dump(obj1.result['daily_quakes'],fileobj1)
	fileobj1.close()

def write_dates(obj1):
	fileobj1=open(obj1.output+'/Dates.txt','w')
	pickle.dump(obj1.result['datetimes'],fileobj1)
	fileobj1.close()