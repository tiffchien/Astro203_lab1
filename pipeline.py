import numpy as np 
from astropy.io import fits
from matplotlib import pyplot as plt 
from matplotlib import colors
import scipy.stats

# Inputs:
    # folder: path to where the .fits files are, e.g. '2016jul14/'
    # start, end: range of indices of images, e.g. 95,96
        # assumes that the filenames look like e.g. n0095.fits
# Outputs:
    # list of full paths to images, e.g. ['2016jul14/n0095.fits', '2016jul14/n0096.fits']
def get_file_names(folder, start, end):
    lst = []
    for num in range(start, end+1):
        num_digits = len(str(num))
        lst.append(folder + '/n' + '0'*(4-num_digits) + str(num) + '.fits')
    return lst

# Opens (and closes) a list of .fits file and returns the data (numpy arrays) in the PrimaryHDUs
# Inputs:
    # list of full paths to .fits file, e.g. output of get_file_names()
# Outputs:
    # numpy array of all data (shape: n_images x image_size x image_size)
def get_data_from_path(filenames):
    data = []
    for filename in filenames:
        with fits.open(filename) as hdul:
            data.append(hdul[0].data)
    return np.array(data)

# Takes in image indices and returns the data from their fits files.
# Calls get_data_from_path()
def get_data(folder, start, end):
    filenames = get_file_names(folder, start, end)
    all_frames = get_data_from_path(filenames)
    return all_frames

# Visualizes image with log normalization and optional vmin and vmax.
# data: numpy array
def plot_img(data, vmin=None, vmax=None):
    plt.figure(figsize=(10,10))
    plt.imshow(data, norm=colors.LogNorm(), cmap='gray', vmin=vmin, vmax=vmax)

# Computes average of given frames
def average(folder, start, end):
    all_frames = get_data(folder, start, end)
    return np.mean(all_frames, axis=0)

# Computes median of given frames
def median(folder, start, end):
    all_frames = get_data(folder, start, end)
    return np.median(all_frames, axis=0)

# Master dark = average of multiple darks with the same total integration time.
def make_master_dark(folder, start, end):
    return average(folder, start, end)

# Master flat = average over multiple flats, then subtract dark.
# Dark and flats should match in total integration time.
    # Scale dark (linearly) before passing it in if this is not the case.
def make_master_flat(folder, start, end, master_dark):
    ave = average(folder, start, end)
    return ave - master_dark

# Master sky = average over multiple skys, then subtract dark, then normalize with flat.
    # (this master sky has dark removed.)
# Dark and skys should match total integration time. Flat doesn't have to.
def make_master_sky(folder, start, end, master_dark, master_flat):
    ave = average(folder, start, end)
    return (ave - master_dark ) / master_flat

# Full cleaned image = subtract dark, then normalize with flat, then subtract sky
# Dark, sky, and image should match total integration time.
def process_image(folder, img_index, master_dark, master_flat, master_sky):
    raw = get_data(folder, img_index, img_index)[0]
    return ((raw - master_dark) / master_flat) - master_sky

# Processes images and then writes them to new fits files (saved in folder out_folder).
# Copies the header of the original file to the new file.
def process_fits(in_folder, out_folder, start, end, master_dark, master_flat, master_sky):
    raw_imgs = get_data(in_folder, start, end)
    in_filenames = get_file_names(in_folder, start, end)
    out_filenames = get_file_names(out_folder, start, end)
    for i in range(raw_imgs.shape[0]):
        raw = raw_imgs[i]
        processed = process_image(in_folder, start+i, master_dark, master_flat, master_sky)

        in_header = None
        with fits.open(in_filenames[i]) as hdu_in:
            in_header = hdu_in[0].header

        fits.writeto(out_filenames[i], processed, header=in_header)



