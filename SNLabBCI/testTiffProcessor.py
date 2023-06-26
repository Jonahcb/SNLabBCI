import TiffProcessor as tp
import numpy as np
import Grapher as g


def test_photon_count():
    # create array of test data
    array = np.array([
        [[[2, 4, 3], [4, 1, 6], [6, 2, 10]], [[9, 4, 13], [7, 13, 2], [11, 5, 17]]],
        [[[10, 12, 8], [3, 1, 19], [14, 11, 2]], [[12, 9, 15], [4, 5, 1], [6, 4, 8]]]
    ])

    # make it have 2 trials, 2 channels, 1 frame, 3 lines, and 3 values per line
    x = array.reshape(2, 2, 1, 3, 3)

    # plot non-normalized data
    g.plot_single_trial(x.reshape(2, 2, 9), [1, 2], values={"-GRAPH_TITLE-": 'test'})

    # normalize data using TiffProcessor's normalization code
    x_min, x_max = x.min(axis=1, keepdims=True), x.max(axis=1, keepdims=True)
    normalized_data = (x - x_min) / (x_max - x_min)

    # plot normalized data
    g.plot_single_trial(normalized_data.reshape(2, 2, 9), [1, 2], values={"-GRAPH_TITLE-": 'test'})


    # plot threshold data
    g.plot_single_trial(tp.photon_count(data=normalized_data), [1, 2],
                        values={"-GRAPH_TITLE-": 'test'})


test_photon_count()
