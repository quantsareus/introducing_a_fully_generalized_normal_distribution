#! /usr/bin/env python3


"""
Description:
The generation and re-identification test is a python script, that verifies the validity of the new fully generalized normal distribution (FGND) for the FGND construction parameters within the test parameter matrix created further following.

The result files are written at the current work directory.
"""

def version_changes():
	"""
	Version changes from V0.17 to V0.20:
	- Code clean up, writing comments
	"""
	pass


### Setup:

# Proper import for installed FGND package:
import fgnd.modul as modul
# Proper import for running from local FGND folder:
# import modul

import numpy as np
# print("numpy Version:", np.__version__)
# import numpy.random
# from numpy.linalg import inv

# import scipy.integrate as sp_it
# from scipy.special import gamma
import scipy.stats as sp_stats
# print("scipy Version:", sp.__version__)

from sympy.functions.special.gamma_functions import gamma
# import sympy as sy
# print("sympy Version:", sy.__version__)

import pandas as pd
# print("pandas Version:", pd.__version__)

# import matplotlib as mpl

import time


### Creating test parameter matrix to perform tests from:

# number of testdata observations 
# n= 100
# n= 1000
# glm setting:
# n= 10000
# genreidtest setting:
n= 100000
# n= 1000000
# n= 10000000

c= np.array([0], dtype=np.float128)

z= np.arange(0.5, 2.1, 0.1, dtype=np.float128)

k= pd.Series(np.arange(1.50, 3.02, 0.02, dtype=np.float128))

# Out of bounds:
# a= pd.Series(np.arange(1.0, 1.38, 0.01, dtype=np.float128))
a= pd.Series(np.arange(1.0, 1.34, 0.01, dtype=np.float128))
# Adding 1/a values for left skewed:
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


print("Total number of parameter combinations:", params.shape[0])
print("")


# Generating 3 normal distribution parameter sets
paramsnd= np.array([[0, 0.5, 2, 1],[0, 1, 2, 1], [0, 2, 2, 1]], dtype=np.float128)

# Drawing random samples from params
paramsindexold= np.arange(0, params.shape[0], 1) 
# paramsindexnew= modul.sample(paramsindexold, 100)
paramsindexnew= modul.sample(paramsindexold, 1000)
paramssamp= params[paramsindexnew, :]

paramssamp= pd.DataFrame(paramsnd).append(pd.DataFrame(paramssamp))
paramssamp= np.array(paramssamp)


# print(params)
# print(paramsnd)
print("# Test Samples:", paramssamp.shape[0])
print("")
print("Machine precision of sample parameters c,z,k,a,:", paramssamp.dtype)
print("")


### Performing Generating and Re-Identification Tests:

results= np.zeros((paramssamp.shape[0], 10), dtype= np.float128)
# matched:
results[:, 8]= -1.0
# trial:
results[:, 9]= 1.0

# for i in range (0, 1, 1):
for i in range (0, paramssamp.shape[0], 1):
	print("iteration:", i, "/", paramssamp.shape[0], "  time:", time.asctime(time.localtime()) )  
	
	c= paramssamp[i, 0]
	z= paramssamp[i, 1]
	k= paramssamp[i, 2]
	a= paramssamp[i, 3]
	
	# Creating testdata from original c,z,k,a parameters:
	testdata= modul.qrng(n, 1, "fgnd", 0, z, k, a, 1e-4) 
		
	mean= np.mean(testdata)
	std= np.std(testdata)
	skew= modul.skewness(testdata)
	kurt= modul.kurtosis(testdata)
	
	# Finding parameter estimates c_, z_, k_, a_
	paramssamp_= modul.findparams(mean, std, skew, kurt)
		
	c_= 0
	z_= paramssamp_[0, 1]
	k_= paramssamp_[0, 2]
	a_= paramssamp_[0, 3]
	
	diffsum= abs(c -c_) +abs(z -z_) +abs(k -k_) +abs(z -z_)
	if diffsum < 1e-2:
		matched= 1.0
	else:
		matched= 0.0
				
	results[i, 0:4]= paramssamp[i, 0:4]
	results[i, 4:9]= np.array([c_, z_, k_, a_, matched])
	

### Writing Test Results:

testresultsdf= pd.DataFrame(results, columns= ["c","z","k","a","c_","z_","k_","a_", "matched", "trial"])

if testresultsdf.to_csv("./testresults.csv", index= False, header= True):
	print("")				
	print("writing testresults.csv has failed")
	print("")
else:
	print("")				
	print("testresults.csv has been written succesfully")				
	print("")
	fobj= open("testrespreview.txt", "w")
	print(testresultsdf, file=fobj)
	fobj.close
	

### Test Results Summary:

testresults= np.array(testresultsdf)
matchedsum= np.sum(np.int64(testresults[ :, 8]))
trialsum= np.sum(np.int64(testresults[ :, 9]))
matchedprop= matchedsum/ trialsum


print("")
print("")
print("#####################################################################################")
print("###                     Test Results Summary                                      ###")
print("#####################################################################################")
print("")
print("# Total Trials:" , trialsum )
print("# Among these # trials with z==1:", np.sum(testresults[np.round(testresults[ :, 1], 1) == 1.0, 9 ]), "; # trials with z!=1:", np.sum(testresults[np.round(testresults[ :, 1], 1) != 1.0, 9 ]) )
print("")
print("# Matched:", matchedsum)
print("")
print("Proportion Matched:", matchedprop)
print("")
print("")
print("#####################################################################################")
print("###                     Hypothesis Test Result                                    ###")
print("#####################################################################################")
print("")
print(sp_stats.binomtest(matchedsum, trialsum, (matchedprop -0.01), "greater") )
print("")
print("P-Value:", sp_stats.binom_test(matchedsum, trialsum, (matchedprop -0.01), "greater") )
print("")
# print("Tests failed:")
# print( testresults[np.round(testresults[ :, 8], 1)== 0.0, : ])


### File Versions of above:

fobj= open("testressum.txt", "w")
print("", file=fobj)
print("#####################################################################################", file=fobj)
print("###                     Test Results Summary                                      ###", file=fobj)
print("#####################################################################################", file=fobj)
print("", file=fobj)
print("# Total Trials:" , trialsum, file=fobj )
print("# Among these # trials with z==1:", np.sum(testresults[np.round(testresults[ :, 1], 1) == 1.0, 9 ]), "; # trials with z!=1:", np.sum(testresults[np.round(testresults[ :, 1], 1) != 1.0, 9 ]), file=fobj )
print("", file=fobj)
print("# Matched:", matchedsum, file=fobj)
print("", file=fobj)
print("Proportion Matched:", matchedprop, file=fobj)
print("", file=fobj)
fobj.close

fobj= open("hyptestres.txt", "w")
print("", file=fobj)
print("#####################################################################################", file=fobj)
print("###                     Hypothesis Test Result                                    ###", file=fobj)
print("#####################################################################################", file=fobj)
print("", file=fobj)
print(sp_stats.binomtest(matchedsum, trialsum, (matchedprop -0.01), "greater"), file=fobj )
print("", file=fobj)
print("P-Value:", sp_stats.binom_test(matchedsum, trialsum, (matchedprop -0.01), "greater"), file=fobj )
print("", file=fobj)
fobj.close

