import TiffProcessor as tp
from sklearn import decomposition
from sklearn import datasets
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# unused but required import for doing 3d projections with matplotlib < 3.2
import mpl_toolkits.mplot3d  # noqa: F401


def my_pca(data):

    X = data

    print("Principal Component Analysis")
    print(X.shape)
    pca = decomposition.PCA(n_components=3)
    pca.fit(X)
    X = pca.transform(X)

    print(pca.explained_variance_ratio_)

    print(X.shape)
    print(X)
