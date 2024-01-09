

The FGND package provides the first fully generalized normal distribution, generalized for skewness and kurtosis.

System Requirements:
Python installation with the Python packages
- Numpy
- Scipy
- Sympy
- Pandas

- sys
- os
- time.

These ones -- in case -- can be easierst installed as follows: 
1. Installling Python Packkages PIP. 
2. Typing "pip3 install numpy scipy sympy pandas sys os time" (Windows/ OS-X: "pip install numpy scipy sympy pandas sys os time") in a terminal window.

Or you can install the Anaconda Numerical Python Distribution, that already includes them all. (Which however, is a commercial (non-open-source) project.)


#############################################################################################################################


The FGND package is distributed as a classical "Python source code distribution". To install the package proceed as follows:

1. Download py-fgnd.zip (from subfolder dist) and unzip it. (Which you may have already done, when reading this README.txt) 

2. Just to make sure check, if the subdirectory "fgnd" is populated with files listed in "MANIFEST". 

3. Open a terminal window (Windows: power shell) and change to the directory you have unzipped to. It has to contain the file setup.py.

4. Then execute (in case with adminstrator/ root privileges):
    Linux terminal: "sudo python3 setup.py install"
    Windows admin-powershell: "python setup.py install".
    OS-X: "python setup.py install".

That's all. 




The package should have been installed under the operating system's standard path for 3rd party Python packages into the directoy "fgnd". Check the succesfull install by typing "python3 import fgnd" (Windows/ OS-X: "python import fgnd"). If successfull, "FGND Setup Check SUCCESSFULL" and some other check routines will be printed.


Now, you can reproduce the generation and re-Identification test by typing into a terminal window: 
1. python3 (Windows/ OS-X: python)
2. import fgnd.genreidtest 



Or you can include the author's FGND into your own Python program using 

"import fgnd.modul as fgnd" 

at the beginning of your program. 




