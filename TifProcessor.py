import os
import numpy as np
from PIL import Image
import Metadata_Reader as mr
import scipy.io
import matplotlib.pyplot as plt

# constants
pixelps = 3.4 / 65536.0

# frames per second
fps = 3.4

# seconds per frame
spf = 0.294

# milliseconds per line
mspl = 1.15


def filter_channel(tif):
    """
    Returns: 4D numpy array with an element for each channel

    Parameter tif: the data to separate into channels
    Precondition: tif must be 3D nested numpy array
    """
    # separate channels
    CH1 = tif[::4]
    CH2 = tif[1::4]
    CH3 = tif[2::4]
    CH4 = tif[3::4]

    return average_line(np.array([CH1, CH2, CH3, CH4]))


def average_line(data):
    """
    Returns: 3D numpy array averaged across each line

    Parameter data: the data to average across each line
    Precondition: data must be 4D nested numpy array
    """
    return np.mean(data, axis=-1)


def average_trials(files):
    """
    Returns: 4D numpy array averaged across each trial of same orientation

    Parameter data: the data to average across each orientation
    Precondition: files must be 4D nested numpy array
    """

    # list of lists grouped by angle: [file #, angle]
    meta_data, temp = mr.read_metadata()

    # determine where to split array by cumulating orientations
    temp = np.array(temp).cumsum()

    # get rid of last element to split
    sum_orientations = temp[:-1]

    # reorder array so it is grouped by angle
    arr_reordered = np.take(files, meta_data, axis=0)

    # split by orientation
    arr_reordered = np.split(arr_reordered, sum_orientations)

    temp = []
    for array in arr_reordered:
        temp.append(np.mean(array, axis=0))
    avgResult = np.array(temp)

    print(avgResult.shape)


    # return averaged numpy array
    return avgResult


def tif_processor_run(type):
    """
    Stores pixel values from a directory of tiff file into a numpy array.

    Parameter type: the type of processing to do to the tiff files
    Precondition: type must be an int

    Returns: 4D numpy array with pixel values separated into channels
    """
    # the folder directory with all the tiff files
    tiff_dir = '/Users/jonahbernard/Desktop/SN Lab/2022-10-24 spot1_4AEQ_ctz_test_Thy1GCaMP6s_ctz/stim'

    # tiff_dir = '/Users/jonahbernard/Desktop/SN Lab/Test'
    # initialize array to hold raw data from each frame
    processed_tiffs = []
    # loop through every tif file in folder
    for tiff in os.listdir(tiff_dir):
        # make sure it is a tif file
        if ('.tif' in tiff):
            # open tif file using PIL Image
            with Image.open(tiff_dir + '/' + tiff) as img:
                # initialize list to hold frames
                frames = []
                # loop through every frame
                for i in range(img.n_frames):
                    # go to right frame
                    img.seek(i)
                    # make frame data into array of floats
                    frame = np.array(img).astype(float)

                    # correct for zig-zag recording pattern by flipping every other line
                    frame[1::2, :] = frame[1::2, ::-1]

                    # append frame data array to frames list
                    frames.append(frame)
                # append frames array to processed tif files list
                processed_tiffs.append(np.array(frames))

    np.array(processed_tiffs)

    temp = []
    for tif in processed_tiffs:
        temp.append(filter_channel(tif))
    tiff_by_channel = np.array(temp)
    if type == 1:
        tiff_by_channel = average_trials(tiff_by_channel)
    return tiff_by_channel


def average():
    type = 1
    return tif_processor_run(type)


def single_trial(trials):
    """
    Returns: 4D numpy array with selected trials

    Parameter trials: the trial indices to plot
    Precondition: files must be 4D nested numpy array
    """
    type = 0
    all_trials = tif_processor_run(type)

    # select trials we need from list of indices
    selected_trials = np.take(all_trials, trials, axis=0)

    return (selected_trials)
