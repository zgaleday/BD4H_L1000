from sklearn.decomposition import PCA
from sklearn.decomposition import FastICA


def reduce_dimensionality(x, alg='pca'):
    if alg is 'ica':
        d = FastICA()
    else:
        d = PCA()
    projected = d.fit_transform(x)
    return projected, d
