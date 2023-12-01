
import pickle
from sklearn.ensemble import RandomForestClassifier
import datetime
import calendar
import numpy as np
from load_mod import load_mod

carrier_ids=np.load('/data/carrier_ids.npy',allow_pickle=True)
dest_ids=np.load('/data/dest_ids.npy',allow_pickle=True)
origin_ids=np.load('/data/origin_ids.npy',allow_pickle=True)

min_airtime=19.
max_airtime=588.

def predict(air_time,carrier_,origin_,dest_,datetime_,model):
	
	# one-hot
	# correct for one-hot dropping first value
	carrier=np.zeros(7)
	if carrier_!=carrier_ids[0]:
		carrier_ids_=[str(x) for x in carrier_ids[1:]]
		carrier[carrier_ids_.index(carrier_)]=1.0
	dest=np.zeros(19)
	if dest_!=dest_ids[0]:
		dest_ids_=[str(x) for x in dest_ids[1:]]
		dest[dest_ids_.index(dest_)]=1.0
	origin=np.zeros(19)
	if origin_!=origin_ids[0]:
		origin_ids_=[str(x) for x in origin_ids[1:]]
		origin[origin_ids_.index(origin_)]=1.0
	
	# frac yr, frac day
	is_leap=calendar.isleap(datetime_.year)
	if is_leap: dt_yr=366.
	else: dt_yr=365.
	frac_yr=(datetime_-datetime.datetime(datetime_.year,1,1))/datetime.timedelta(days=dt_yr)
	frac_day=(datetime_-datetime.datetime(datetime_.year,datetime_.month,1))/datetime.timedelta(days=1)
	
	day_frac_sin,day_frac_cos=np.sin(2.*np.pi*frac_day/1.0),np.cos(2.*np.pi*frac_day/1.0)
	year_frac_sin,year_frac_cos=np.sin(2.*np.pi*frac_yr/1.0),np.cos(2.*np.pi*frac_yr/1.0)
	
	air_time=(air_time-min_airtime)/(max_airtime-min_airtime) #scaler.transform(np.asarray(air_time))
	
	X_array=np.concatenate([[air_time],carrier,origin,dest,[year_frac_sin],[year_frac_cos],[day_frac_sin],[day_frac_cos]]).reshape(1,-1)
	prediction=model.predict(X_array)
	return prediction
