import pandas as pd
import numpy as np
import array
from sklearn.base import BaseEstimator, ClassifierMixin, clone, is_classifier
from sklearn.base import MetaEstimatorMixin, is_regressor
from sklearn.utils.validation import check_is_fitted, _num_samples
import scipy.sparse as sp
from sklearn.feature_selection import *
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from utils import get_train_test_data
from sklearn.preprocessing import LabelBinarizer
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

def _predict_binary(estimator, X):
    """Make predictions using a single binary estimator."""
    if is_regressor(estimator):
        return estimator.predict(X)
    try:
        score = np.ravel(estimator.decision_function(X))
    except (AttributeError, NotImplementedError):
        # probabilities of the positive class
        score = estimator.predict_proba(X)[:, 1]
    return score


RANDOM_SEED = 0

class CustomBRClassifier(object):
    """A custom model following the sklearn api that will perform feature selection before model training.  Defines
    the minimal API"""
    def __init__(self, base_model, n_features=25, n_jobs=-1):
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

    def fit(self, x_train, y_train, select_feats=False):
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
            selector = RFE(lr, 25, step=10, verbose=1)
            ovr_fs = OneVsRestClassifier(selector, n_jobs=-1)
            ovr_fs.fit(self.X, self.Y)
            self.selectors = ovr_fs.estimators_
            self.new_feats = np.array([model.get_support() for model in self.selectors])
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
        return selector.fit_transform(self.X, classes)

    def predict(self, X):
        """Predict multi-class targets using underlying estimators.
        Parameters
        ----------
        X : (sparse) array-like, shape = [n_samples, n_features]
            Data.
        Returns
        -------
        y : (sparse) array-like, shape = [n_samples, ], [n_samples, n_classes].
            Predicted multi-class targets.
        """
        X = X.values
        check_is_fitted(self, 'estimators_')
        if (hasattr(self.estimators_[0], "decision_function") and
                is_classifier(self.estimators_[0])):
            thresh = 0
        else:
            thresh = .5

        n_samples = _num_samples(X)
        if self.label_binarizer_.y_type_ == "multiclass":
            maxima = np.empty(n_samples, dtype=float)
            maxima.fill(-np.inf)
            argmaxima = np.zeros(n_samples, dtype=int)
            for i, e in enumerate(self.estimators_):
                pred = _predict_binary(e, X[:, self.new_feats[i, :]])
                np.maximum(maxima, pred, out=maxima)
                argmaxima[maxima == pred] = i
            return self.classes_[np.array(argmaxima.T)]
        else:
            indices = array.array('i')
            indptr = array.array('i', [0])
            for i, e in enumerate(self.estimators_):
                indices.extend(np.where(_predict_binary(e, X[:, self.new_feats[i, :]]) > thresh)[0])
                indptr.append(len(indices))
            data = np.ones(len(indices), dtype=int)
            indicator = sp.csc_matrix((data, indices, indptr),
                                      shape=(n_samples, len(self.estimators_)))
            return self.label_binarizer_.inverse_transform(indicator)

    def predict_proba(self, X):
        """Probability estimates.
        The returned estimates for all classes are ordered by label of classes.
        Note that in the multilabel case, each sample can have any number of
        labels. This returns the marginal probability that the given sample has
        the label in question. For example, it is entirely consistent that two
        labels both have a 90% probability of applying to a given sample.
        In the single label multiclass case, the rows of the returned matrix
        sum to 1.
        Parameters
        ----------
        X : array-like, shape = [n_samples, n_features]
        Returns
        -------
        T : (sparse) array-like, shape = [n_samples, n_classes]
            Returns the probability of the sample for each class in the model,
            where classes are ordered as they are in `self.classes_`.
        """
        X = X.values
        check_is_fitted(self, 'estimators_')
        # Y[i, j] gives the probability that sample i has the label j.
        # In the multi-label case, these are not disjoint.
        Y = np.array([e.predict_proba(X[:, self.new_feats[i, :]])[:, 1] for i, e in enumerate(self.estimators_)]).T

        if len(self.estimators_) == 1:
            # Only one estimator, but we still want to return probabilities
            # for two classes.
            Y = np.concatenate(((1 - Y), Y), axis=1)

        if not self.multilabel_:
            # Then, probabilities should be normalized to 1.
            Y /= np.sum(Y, axis=1)[:, np.newaxis]
        return Y

    def _load_features(self):
        self.new_feats = np.load("../../../data/selected_features.npy")

    def multilabel_(self):
        """Whether this is a multilabel classifier"""
        return self.label_binarizer_.y_type_.startswith('multilabel')



