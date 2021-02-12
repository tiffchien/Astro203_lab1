import numpy as np 
from astropy.io import fits
from matplotlib import pyplot as plt 
from matplotlib import colors
import scipy.stats

# inputs:
    # folder: path to where the .fits files are, e.g. '2016jul14/'
    # start, end: range of indices of images, e.g. 95,96
        # assumes that the filenames look like e.g. n0095.fits
# outputs:
    # list of full paths to images, e.g. ['2016jul14/n0095.fits', '2016jul14/n0096.fits']
def get_file_names(folder, start, end):
    lst = []
    for num in range(start, end+1):
        num_digits = len(str(num))
        lst.append(folder + '/n' + '0'*(4-num_digits) + str(num) + '.fits')
    return lst

# Opens (and closes) a list of .fits file and returns the data (numpy arrays) in the PrimaryHDUs
# inputs:
    # list of full paths to .fits file, e.g. output of get_file_names()
# outputs:
    # numpy array of all data (shape: n_images x image_size x image_size)
def get_data(filenames):
    data = []
    for filename in filenames:
        with fits.open(filename) as hdul:
            data.append(hdul[0].data)
    return np.array(data)

# Computes average of given frames
def average(folder, start, end):
    filenames = get_file_names(folder, start, end)
    all_frames = get_data(filenames)
    return np.mean(all_frames, axis=0)