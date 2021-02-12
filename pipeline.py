import numpy as np 
from astropy.io import fits
from matplotlib import pyplot as plt 
from matplotlib import colors
import scipy.stats

# inputs:
	# folder: path to where the .fits files are, e.g. '2016jul14/'
	# nums: (start, end) range of indices of images, e.g. (95,96)
		# assumes that the filenames look like e.g. n0095.fits
# outputs:
	# list of full paths to images, e.g. ['2016jul14/n0095.fits', '2016jul14/n0096.fits']
def get_file_names(folder, nums):
    start, end = nums
    lst = []
    for num in range(start, end+1):
        num_digits = len(str(num))
        lst.append(folder + '/n' + '0'*(4-num_digits) + str(num) + '.fits')
    return lst

# Opens (and closes) a single .fits file and returns the data (numpy array) in the PrimaryHDU
# inputs:
	# full path to single .fits file
# outputs:
	# data (numpy array)
def get_data(filename):
    data = None
    with fits.open(filename) as hdul:
        data = hdul[0].data
    return data