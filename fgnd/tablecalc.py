#! /usr/bin/env python3


""" 
Description:
The "tabelcalc.py" python script computes a new moments table "table.csv", which is used by the findparams() identification procedure. Thus, computing a new larger moments table can enhance the identification parameter space of findparams().

The new "table.csv" will be written at the current work directory. In case make a backup of "table.csv", first, before running tablecalc.py. 
"""


def version_changes():
	"""
	Version changes from V0.17 to V0.20:
	- Code clean up, writing comments
	"""
	pass


### Setup:

import numpy as np
# import numpy.random
# from numpy.linalg import inv

import scipy.integrate as sp_it
# from scipy.special import gamma

from sympy.functions.special.gamma_functions import gamma

import pandas as pd

# import matplotlib as mpl

import time


### Functions:

def fgnd(x):
	"""
	Author's Fully Generalized Normal Distribution appropriate for one-dimensional numerical integration
	"""
	norm1= (2 *z *gamma(1/(k*a))) /(k*a *0.5**(1/(k*a)))
	norm2= (2 *z *gamma(1/(k/a))) /(k/a *0.5**(1/(k/a)))
	norm= (norm1 + norm2) /2
	# print("norm:", norm)
	if x-c <0:
		return np.exp(-0.5 *(abs(x-c)/z)**(k*a) ) /norm
	else:
		return np.exp(-0.5 *(abs(x-c)/z)**(k/a) ) /norm

def mean_fct(x):
	return fgnd(x)* x 

def variance_fct(x):
	return fgnd(x)* (x-mean)**2 

def skewness_fct(x):
	return fgnd(x)* ((x-mean)/std)**3 

def kurtosis_fct(x):
	return fgnd(x)* ((x-mean)/std)**4 


### Creating FGND parameter matrix to get tabled: 

c= np.array([0], dtype=np.float128)

z= np.array([1], dtype=np.float128)

k= pd.Series(np.arange(1.5, 3.01, 0.01, dtype=np.float128))
 
a= pd.Series(np.arange(1.0, 1.51, 0.01, dtype=np.float128))
# adding 1/a values for left skewed:
a= pd.Series(a).append(pd.Series((1/a)[1:]))


c= pd.DataFrame({"key": np.repeat(0, c.shape[0]), "c": pd.Series(c)}) 
z= pd.DataFrame({"key": np.repeat(0, z.shape[0]), "z": pd.Series(z)})
k= pd.DataFrame(({"key": np.repeat(0, k.shape[0]), "k": pd.Series(k)}))
a= pd.DataFrame(({"key": np.repeat(0, a.shape[0]), "a": pd.Series(a)}))
params= pd.merge(c, z)
params= pd.merge(params, k)
params= pd.merge(params, a)
params= np.array(params, dtype=np.float128)
# Deleting key:
params= params[:,1:]


print("")
print("Machine precision of params table containing c,z,k,a,:")
print(params.dtype)
print("")
print("parameter preview:")
print(params)
print("")


### Calculating moments table:

table= np.zeros((params.shape[0], 8), dtype= np.float128)

# for i in range (0, 1, 1):
for i in range (0, params.shape[0], 1):
	print("iteration:", i, "/", params.shape[0], "  time:", time.asctime(time.localtime()) )  
	
	c= params[i, 0]
	z= params[i, 1]
	k= params[i, 2]
	a= params[i, 3]
	
	mean= sp_it.quad(mean_fct, -np.inf, np.inf)[0]
	variance= sp_it.quad(variance_fct, -np.inf, np.inf)[0]
	std= np.sqrt(variance)
	skew= sp_it.quad(skewness_fct, -np.inf, np.inf)[0]
	kurt= sp_it.quad(kurtosis_fct, -np.inf, np.inf)[0]
			
	table[i, 0:4]= params[i, 0:4]
	table[i, 4:8]= np.array([mean, std, skew, kurt])
	

tabledf= pd.DataFrame(table, columns= ["c","z","k","a","mean","std","skew","kurt"])

if tabledf.to_csv("table.csv", index= False, header= True):
	print("")				
	print("writing table.csv has failed")
else:
	print("")				
	print("the moments table (preview):")				
	print(tabledf)
	print("")
	print("has been written succesfully")


