

##### for building distribution package in genreidtest.py reset "import modul" to "import fgnd.modul as modul"
##### python3 setup.py sdist --formats=zip
##### sudo python3 setup.py install



#####################################################################################


from distutils.core import setup

setup(
	name="py-fgnd",
	version= "0.26",
	author= "H. Schlingmann",
	author_email= "email{at]quantsareus[dot}net",
	# maintainer= "Dr. Open Role",
	# maintainer_email= "dr.open.role@quantsareus.net",
	url= "www.github.com/quantsareus/introducing_a_fully_generalized_normal_distribution",
	download_url= "www.github.com/quantsareus/introducing_a_fully_generalized_normal_distribution/dist/py-fgnd.zip",
	license= "GPLv3 for non-commercial use.",
	# packages= subdirectories to be installed containing a __init__.py ; should not have the same name as distribution:
	packages= ["fgnd"],
	package_data= {"fgnd": ["table.csv"]},
	# further data files to be included in the distribution archive but not to get installed by setup.py install: 
	data_files= [(".", ["MANIFEST"])],
	# python modules in the project's root directory to be installed without directory and to get imported into the global namespace:
	# py_modules= [""],
	# scripts in the project's root directory not to be included in the distribution archive (e.g. building scripts):
	# scripts= [""],
	description= "The author is introducing the world's first fully generalized normal distribution, generalized for skewness and kurtosis. This is the accompanying python package for the thesis introducing_a_fully_generalized_normal_distribution_published.pdf, a.o. also available at the github repository.",
	long_description="Before this package it was an absolute nuisance in data-science, that data-scientists had to find the appropriate theoretical distribution and the appropriate statistical test case by case, more or less individual and for each piece of data and for each parameter to test. Meaning the data-scientist effectively had to choose from hundreds of statistical test setups, when validating the computed parameters of prediction and effect-size models. This nuisance is intended to get ended right here by delivering a foundation of a new theoretically fully flexible distribution. However, there still exist some less restrictive practical application limits. Mainly in the parameter space possible for random number generation by the function qrng(), caused by precision and size limits from practical machining. However, the effective generation parameter space can be massively extended in deviation applying z-transform. Another, less relevant limit exists in the out-of-the-box range of the findparams() function. The re-identification range in parameters of findparams() is limited by the out-of-the-box size of the moments table 'table.csv'. The moments table can be enlarged by computing a new one with the tablecalc.py script. All out-of-the-box parameter limits are printed, when the fgnd package gets imported by 'import fgnd'."
	)

