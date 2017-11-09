import pandas as pd
from plotting import plot_hist


def compute_target_distribution(labels, plot=False, verbose=False):
    distribution = pd.DataFrame(labels).sum(axis=0)
    if verbose:
        print('target feature representation')
        print('-----------------------------')
        print(distribution.describe())
        print('-----------------------------')
    if plot:
        plot_hist(distribution, 'target feature representation distribution')
    return distribution
