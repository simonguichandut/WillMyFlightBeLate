
import pandas as pd
import numpy as np
from datetime import date

from sklearn.preprocessing import PolynomialFeatures 
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression 
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge, Lasso

d=pd.read_csv('JFK.csv')

# map date to fraction of year (2pi)

fldates=[]
for el in list(d['FL_DATE']):
	day=int(el.split(' ')[0].split('/')[1])
	month=int(el.split(' ')[0].split('/')[0])
	fracyr=(date(2018,1,1)-date(2018,month,day)).total_seconds()*1.997858576000835e-07
	fldates.append(np.abs(fracyr))

e=pd.DataFrame(np.array([d['FL_DATE'],fldates,d['CRS_DEP_TIME'],d['DEP_DELAY']])).T
e.columns=['FL_DATE','DATE_YR','CRS_DEP_TIME','DEP_DELAY']

e=e.loc[e['DEP_DELAY']>0]

print(e)

alpha = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]
n=2
# to hold our coefficient estimates
lasso_coefs = np.empty((len(alpha),n))

for i in range(len(alpha)):
	# set up the lasso pipeline
	lasso_pipe = Pipeline([("scale",StandardScaler()),("poly",PolynomialFeatures(n, interaction_only=False, include_bias=False)), ("lasso",Lasso(alpha=alpha[i], max_iter=5000000))])
	# fit the lasso 
	lasso_pipe.fit(np.array(e['DATE_YR']).reshape(-1,1), e['DEP_DELAY'])
	# record the coefficients
	lasso_coefs[i,:] = lasso_pipe["lasso"].coef_

	print(lasso_coefs)
