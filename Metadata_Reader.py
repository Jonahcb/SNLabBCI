import os
import numpy as np
from PIL import Image
import scipy.io
import math


def read_metadata():
    # constant list with orientations
    orientations = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]

    # set numpy array to print non-truncated version
    np.set_printoptions(threshold=np.inf)

    # read in metadata file
    f = scipy.io.loadmat(
        '/Users/jonahbernard/Desktop/SN Lab/2022-10-24 spot1_4AEQ_ctz_test_Thy1GCaMP6s_ctz/2022-10-24 spot1_4AEQ_ctz_test_Thy1GCaMP6s_ctz stim vs.mat')

    # save useful data to numpy array
    data = np.array(f['vs'][0][0][2])

    # save order of orientations
    data = data[:, ::16]

    # generate list with number of trials for each orientation
    num_orientations = []

    for angleConstant in orientations:
        count = 0
        for angleTrial in data:
            if angleTrial[1] == angleConstant:
                count = count + 1
        num_orientations.append(count)

    sum_orientations = np.array(num_orientations).cumsum()
    # reorder array to group by angle
    sorted_list = np.array(sorted(data, key=lambda x: x[1]))

    # return 2D numpy array with each element having a list with two elements: file # and
    # orientation
    sorted_list = sorted_list[:, 0] - 1

    # cast index list values to ints
    result = np.array(sorted_list).astype(int, casting='unsafe')

    return result, num_orientations


read_metadata()
