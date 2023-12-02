
import joblib
import datetime
import calendar
import numpy as np

min_airtime=19.
max_airtime=588.

def load_model():
	# with open('models/RF_2022_2023.pickle','rb') as f:
	# 	model = pickle.load(f)
	model = joblib.load('models/RF_2022_2023.joblib')
	return model

def predict(model, air_time, carrier_, origin_, dest_, datetime_, carrier_codes, airport_ids):
	
	# one-hot
	# correct for one-hot dropping first value
	carrier_onehot = np.zeros(7)
	if carrier_!=carrier_codes[0]:
		carrier_onehot[carrier_codes.index(carrier_)] = 1.0

	orig_onehot = np.zeros(19)
	if origin_!= airport_ids[0]:
		orig_onehot[airport_ids.index(origin_)] = 1.0
	
	dest_onehot = np.zeros(19)
	if dest_ != airport_ids[0]:
		dest_onehot[airport_ids.index(dest_)] = 1.0

	# frac yr, frac day
	is_leap = calendar.isleap(datetime_.year)
	if is_leap: dt_yr=366.
	else: dt_yr=365.
	frac_yr = (datetime_-datetime.datetime(datetime_.year,1,1))/datetime.timedelta(days=dt_yr)
	frac_day = (datetime_-datetime.datetime(datetime_.year,datetime_.month,datetime_.day,0))/datetime.timedelta(days=1)
	
	day_frac_sin, day_frac_cos = np.sin(2.*np.pi*frac_day/1.0),np.cos(2.*np.pi*frac_day/1.0)
	year_frac_sin, year_frac_cos = np.sin(2.*np.pi*frac_yr/1.0),np.cos(2.*np.pi*frac_yr/1.0)
	
	air_time = (air_time-min_airtime)/(max_airtime-min_airtime) #scaler.transform(np.asarray(air_time))
	
	X_array = np.concatenate([[air_time],carrier_onehot, orig_onehot, dest_onehot,
						   [year_frac_sin],[year_frac_cos],[day_frac_sin],[day_frac_cos]]).reshape(1,-1)
	prediction = model.predict(X_array)
	return prediction
