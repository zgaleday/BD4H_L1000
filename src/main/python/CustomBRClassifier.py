import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin, clone, is_classifier
from sklearn.utils.validation import  check_is_fitted
from sklearn.feature_selection import *
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from utils import get_train_test_data
from sklearn.preprocessing import LabelBinarizer
import pickle
from joblib import Parallel, delayed
from ipyparallel import *


def _fit_binary(estimator, X, y, classes=None):
    """Fit a single binary estimator."""
    unique_y = np.unique(y)
    if len(unique_y) == 1:
        if classes is not None:
            if y[0] == -1:
                c = 0
            else:
                c = y[0]
            warnings.warn("Label %s is present in all training examples." %
                          str(classes[c]))
        estimator = _ConstantPredictor().fit(X, unique_y)
    else:
        estimator = clone(estimator)
        estimator.fit(X, y)
    return estimator


class _ConstantPredictor(BaseEstimator):

    def fit(self, X, y):
        self.y_ = y
        return self

    def predict(self, X):
        check_is_fitted(self, 'y_')

        return np.repeat(self.y_, X.shape[0])

    def decision_function(self, X):
        check_is_fitted(self, 'y_')

        return np.repeat(self.y_, X.shape[0])

    def predict_proba(self, X):
        check_is_fitted(self, 'y_')

        return np.repeat([np.hstack([1 - self.y_, self.y_])], X.shape[0], axis=0)


RANDOM_SEED = 0

class CustomBRClassifier(object):
    """A custom model following the sklearn api that will perform feature selection before model training.  Defines
    the minimal API"""
    def __init__(self, base_model, n_features, n_jobs=-1):
        """
        Initializes the model taking the base sklearn model type as input and the desired number of features after
        selection
        :param base_model: base model type from sklearn
        :param n_features: number of features to be used in the final OVR training
        :param n_jobs: number of cores to use, if -1 all available cores are used (see sklearn OneVsRest for details)
        """
        self.selectors = None
        self.estimator = base_model
        self.n_features = n_features
        self.n_jobs = n_jobs

    def fit(self, x_train, y_train, select_feats=True):
        """
        Trains the OVR with feature selection
        :param x_train: training data features
        :param y_train: training data classes
        :return:
        """
        self.X = x_train.values
        self.Y = y_train
        self.N = self.Y.shape[1]
        # c = Client(profile='myprofile')
        # bview = c.load_balanced_view()
        # register_parallel_backend('ipyparallel', lambda: IPythonParallelBackend(view=bview))
        if select_feats:
            lr = LogisticRegression(penalty='l1')
            selector = RFE(lr, 25, step=978, verbose=1)
            ovr_fs = OneVsRestClassifier(selector, n_jobs=-1)
            ovr_fs.fit(self.X, self.Y)
            self.selectors = ovr_fs.estimators_
            self.new_feats = np.array([model.get_support() for model in self.selectors])
            print self.new_feats
            np.save("../../../data/selected_features", self.new_feats)
        else:
            self._load_features()
        ###Modified version of the sklearn OneVsRestClassifier
        self.label_binarizer_ = LabelBinarizer(sparse_output=True)
        Y = self.label_binarizer_.fit_transform(self.Y)
        Y = Y.tocsc()
        self.classes_ = self.label_binarizer_.classes_
        columns = ((col.toarray().ravel(), self.X[:, self.new_feats[i, :]]) for i, col in enumerate(Y.T))
        self.estimators_ = Parallel(n_jobs=self.n_jobs)(delayed(_fit_binary)(
            self.estimator, column[1], column[0], classes=[
                "not %s" % self.label_binarizer_.classes_[i],
                self.label_binarizer_.classes_[i]])
            for i, column in enumerate(columns))
        print len(self.estimators_)
        return self


    def select_feature(self, index):
        """
        Method for use with pool for feature selection
        :param index: class number
        :return: trained selector
        """
        selector = SelectFromModel(estimator=LogisticRegression(penalty='l1', random_state=RANDOM_SEED)
                    )
        classes = self.Y[:, index]
        print index
        return selector.fit_transform(self.X, classes)

    def _load_features(self):
        self.new_feats = np.load("../../../data/selected_features.npy")

x, y = get_train_test_data()
base = LogisticRegression(penalty='l1', random_state=RANDOM_SEED)
br = CustomBRClassifier(base, 25)
br.fit(x,y, False)
