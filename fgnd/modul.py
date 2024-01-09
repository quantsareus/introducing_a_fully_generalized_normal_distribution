

#####! /usr/bin/env python3


"""
Description:
The fgnd module provides the first fully generalized normal distribution (FGND), generalized for skewness and kurtosis. [To be precise also provides a normal distribution (nd) and an ADOPTED generalized normal version 1 distribution (gndv1a)]. The naked distributions are accompanied by foundation identification and random number generation methods. For a more detailed introduction of the new FGND refer to http://www.quantsareus.net/hs/publ/introducing_a_fully_generalized_normal_distribution.pdf
"""

def version_changes():
	"""
	Version changes from V0.17 to V0.20
	- Renamed skew() to skewness()
	- Code clean up, writing comments
	- findinstalledpath()
	- setupcheck()
	"""
	pass

	
### General Setup:

import numpy as np
# import numpy.random as np_rd
# from numpy.linalg import inv

# import scipy.integrate as sp_it
# from scipy.special import gamma

from sympy.functions.special.gamma_functions import gamma

import pandas as pd

# import matplotlib as mpl

import sys
import os


### Distributions:

def nd(u, c, z):
	"""
	Gauss' Normal Distribution
	"""
	norm= np.float128( z* (2* np.pi)**0.5 )
	d= 1 /norm *np.float128( np.exp(-0.5 *((u-c)/z)**2) )
	return d

def gndv1a(u, c, z, k):
	"""
	Nadarajah's Generalized Normal Distribution Version 1
	ADOPTED to direct downward compatibility to Gauss' Normal Distribution by the author 
	"""
	norm= np.float128( (2 *z *gamma(1/k)) /(k *0.5**(1/k)) )
	d= 1 /norm *np.float128( np.exp(-0.5 *(abs(u-c)/z)**k) )
	return d

 
def fgnd(u, c, z, k, a):
	"""
	Author's Fully Generalized Normal Distribution
 	"""	
	norm1= np.float128( (2 *z *gamma(1/(k*a))) /(k*a *0.5**(1/(k*a))) )
	norm2= np.float128( (2 *z *gamma(1/(k/a))) /(k/a *0.5**(1/(k/a))) )
	norm= np.float128( np.array((norm1 + norm2) /2) )
	d= np.float128( np.exp(-0.5 *(abs(u-c)/z)**(k*a) ) )
	d2= np.float128( np.exp(-0.5 *(abs(u-c)/z)**(k/a) ) )
	d[u-c > 0]= d2[u-c > 0]
	d= 1/ norm *d
	return d


### Methods:

def skewness(x):
	"""
	Statistical skewness without sample size correction
	"""
	n= x.shape[0]
	# return n /((n-1)*(n-2)) *np.sum( ((x- np.mean(x))/np.std(x))**3) 
	return 1/n* np.sum( ((x- np.mean(x))/np.std(x))**3) 

def kurtosis(x):
	"""
	Statistical kurtosis without sample size correction
	"""
	n= x.shape[0]
	# return n*(n+1) /((n-1)*(n-2)*(n-3)) *np.sum( ((x -np.mean(x))/np.std(x))**4) 
	return 1/n* np.sum( ((x -np.mean(x))/np.std(x))**4) 

def mkpop(u, ustep, n, distr, c, z, k, a, dtolmax):
	"""
	Method to create a population 
	from an independent variable u with stepsize (resolution) ustep
	that follows a distribution "distr" with parameters c, z, k, a,
	at maximum allowed density tolerance dtolmax (from 1)
	"""
	l= u.shape[0]
	if distr== "nd":
		d= np.float128( nd(u, c, z) )
	if distr== "gndv1a":
		d= np.float128( gndv1a(u, c, z, k) )
	if distr== "fgnd":
		d= np.float128( fgnd(u, c, z, k, a) )

	# PDF norming axiom test:
	dcontr= np.sum(d) *ustep
	dtol= abs(1- dcontr)
	if dtol < dtolmax:
		dcum= np.float128(np.cumsum(d) *ustep *n)
		dresid= np.float128(0.0)
		dint= np.int64(np.zeros(l))
		for i in range(1, l):
			if round(dcum[i] -dcum[i-1] +dresid) >= 0.5:
				dint[i]= round(dcum[i] -dcum[i-1] +dresid)
				dresid= (dcum[i] -dcum[i-1] +dresid) - round(dcum[i] -dcum[i-1] +dresid)
			else:
				dresid= dresid+ dcum[i] -dcum[i-1]
			# print(d[i], dcum[i], dint[i], dresid)
		pop= u.repeat(dint)
		return pop
		
	else:
		print("Error: mkpop cannot create the population on independent u within allowed dtolmax")
		print("pdf test for norming axiom negative")
		print("density sum:", dcontr)
		print("current density tolerance:", dtol, " > ", "allowed density tolerance:", dtolmax)
		print("")

def sample(pop, n):
	"""
	Method to create a sample 
	with size n
	from population pop
	"""
	samp= pop.take(np.random.permutation(len(pop))[:n])	
	return samp

def qrng(n, popsizefac, distr, c, z, k, a, dtolmax):
	"""
	Method to create a population "popsizefac" times large in the first step 
	from an independent variable u with stepsize (resolution) ustep
	that follows a distribution "distr" with parameters c, z, k, a,
	at maximum allowed density toleracance (from 1) dtolmax
	in the second step
	to create a sample 
	with size n
	"""
	popul= mkpop(u, ustep, n *popsizefac, distr, c, z, k, a, dtolmax)
	e= sample(popul, n)
	return e

def findparams(mean, std, skew, kurt):
	"""
	Method to find the construction parameters z, k, a of a FGND distribution from the moments std, skewnes and kurtosis
	"""
	installedpath= findinstalledpath()
	if installedpath!= "":
		tabledf= pd.read_csv(installedpath +"table.csv")
	else:
		if os.path.exists("fgnd/table.csv"):
			tabledf= pd.read_csv("fgnd/table.csv")
		else:
			if os.path.exists("table.csv"):
				tabledf= pd.read_csv("table.csv")
			else:
				print ("\nERROR: The moments table table.csv has not been found")
				print ("Most possibly is FGND neither installed (globally) nor is a local FGND executed from its local folder")
				print ("The current work directory is:", os.getcwd(), "\n")
			
	table= np.array(tabledf)
	tol= (abs(table[:, 6] -skew)) +(abs(table[:, 7] -kurt)) 
	params= table[tol==min(tol), :]
	# Calculating true z using z-reduction std(z=1)= std(z) / z 
	z= std/ params[:, 5]
	# Setting z, the first and second moment to the proper values correponding to z!=1 using z-transform
	params[:, 1]= z
	params[:, 4]= params[:, 4] *z
	params[:, 5]= params[:, 5] *z 
	return params[:]

def findinstalledpath():
	# List of runtime pathes for Python commands
	syspath= sys.path
	syspathlen= len(syspath)

	# Searching own installed path
	installedpath=""
	for i in range(0, syspathlen, 1):
		installedpath= syspath[i] +"/fgnd/"
		if os.path.exists(installedpath):
			break
		else:
			installedpath= ""
	return installedpath
	
def setupcheck():
	"""
	Check of proper fgnd setup 
	by constructing a normal distribution with std 1 
	and trying to re-identifying it on precision level 0.01
	"""
	params=np.array([0, 1, 2, 1])
	c= params[0]
	z= params[1]
	k= params[2]
	a= params[3]
	
	# Creating testdata from original c,z,k,a parameters:
	testdata= qrng(100000, 1, "fgnd", 0, z, k, a, 1e-4) 
		
	mean= np.mean(testdata)
	std= np.std(testdata)
	skew= skewness(testdata)
	kurt= kurtosis(testdata)
	
	# Finding parameter estimates c_, z_, k_, a_
	params_= findparams(mean, std, skew, kurt)
		
	c_= 0
	z_= params_[0, 1]
	k_= params_[0, 2]
	a_= params_[0, 3]
	
	diffsum= abs(c -c_) +abs(z -z_) +abs(k -k_) +abs(z -z_)
	if diffsum < 1e-2:
		print("FGND Setup Check SUCCESSFULL")
		print("")
		print("Parameter Space Limits")
		print("- in Re-Identifiaction by findparams() are: f(x) in s(c=0, z=z, 1.5<=k<=3.0, 0.66<=a<=1.50) @ precision 0.01")
		print("- in Random Number Generation by qrng() are: f(x) in s(c=0, 0.5<=z<=2, 1.5<=k<=3.0, 0.75<=a<=1.33) @ precision 0.01")
		print("out-of-the-box.\n\n\n")	
	else:
		print("FGND Setup Check FAILED")

def interpretercheck():
	print("Python Interpreter Check: Hello Worlds \n")

def tableprintf():
	"""
	Printing a preview of the moments table to file
	"""
	tabledf= pd.read_csv("table.csv")
	fobj= open("tablepreview.txt", "w")
	print(tabledf, file=fobj)
	fobj.close


#####################################################################################
### Active Technical Parameters for Random Number Generation 

# ustep= 0.1
# glm setting (n=10'000):
# ustep= 0.05
# ustep= 0.025
# ustep= 0.01
# genreidtest setting (n=100'000, 0.5<z<=2.0, 1.5<k<=3.0, 0.75<a<=1.33):
ustep= 0.005
# ustep= 0.0025
# ustep= 0.001

# u= np.arange(-10, 10, ustep)
# u= np.arange(-25, 25, ustep)
# genreidtest setting (n=100'000, 0.5<z<=2.0, 1.5<k<=3.0, 0.75<a<=1.33):
u= np.arange(-50, 50, ustep)
# u= np.arange(-100, 100, ustep)
# u= np.arange(-250, 250, ustep)
# u= np.arange(-500, 500, ustep)
# u= np.arange(-1000, 1000, ustep)


#####################################################################################
### Check Procedures on Startup 

interpretercheck()

print("Installation Check: The FGND package is installed to ", "'", findinstalledpath(),"'\n" )

setupcheck()


#####################################################################################
# INACTIVE further parameters FOR TESTING PURPOSES ONLY (Must be fully commented out for application!)

# number of testdata observations 
# n= 100
# n= 1000
# glm setting:
# n= 10000
# generation and re-identification test setting:
# n= 100000
# n= 1000000
# n= 10000000

# construction parameters:
# c= 0

# z=0.5
# z=0.75
# z= 1
# z= 1.5
# z= 2
# z= 3
# z= 4
# z= 5

# k= 1.5
# k= 2
# k=2.5
# k= 3

# a= 1
# a= 1.1
# a= 1.2
# a= 1.3
# a= 1/a


#####################################################################################
# INACTIVE Test Calls FOR TESTING PURPOSES ONLY (Must be fully commented out for application!)
 
# testdata= mkpop(u, ustep, n, "nd", 0, z, 0, 0, 1e-4)
# testdata= mkpop(u, ustep, n, "gndv1a", 0, z, k, 0, 1e-4)
# testdata= mkpop(u, ustep, n, "fgnd", 0, z, k, a, 1e-4)

# testdata= qrng(n, 2, "nd", 0, z, 0, 0, 1e-4)
# testdata= qrng(n, 2, "gndv1a", 0, z, k, 0, 1e-4)
# testdata= qrng(n, 2, "fgnd", 0, z, k, a, 1e-4)

# print("mean:", np.mean(testdata))
# print("estd:", np.std(testdata))
# print("skewness:", skew(testdata))
# print("kurtosis:", kurtosis(testdata))

# print(findparams(0.0, 1.0, 0.5, 3.3).shape)

# tableprintf()


