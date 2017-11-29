import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import roc_curve, auc
from sklearn.utils import shuffle
import numpy as np

RANDOM_STATE = 0
scaler = MinMaxScaler()


def get_train_test_data():
    # read in data, drop CID, and drop columns that have any null values, e.g. NaN
    raw_data = pd\
        .read_csv('../../../data/pandas_input_combined.csv')\
        .dropna(axis=1, how='all')\
        .drop('CID', axis=1)
    # shuffle raw data
    raw_data = shuffle(raw_data, random_state=RANDOM_STATE)
    # build labels by squishing ADR columns
    labels = raw_data[raw_data.columns[raw_data.columns.str.contains('C')]].values
    # drop all ADR columns as they're captured in the labels
    cols_to_keep = [c for c in raw_data.columns if c[0] != 'C']
    raw_data = raw_data[cols_to_keep]
    # drop infrequent rows
    adr_count = np.sum(labels, axis=0)
    labels = labels[:, (adr_count < (labels.shape[0] * 0.9))]
    labels = labels[:, (adr_count > (labels.shape[0] * 0.1))]
    # min-max normalization of features
    normalized_data = pd.DataFrame(scaler.fit_transform(raw_data))
    print("normalized design matrix shape: " + str(normalized_data.shape))
    print("labels shape: " + str(labels.shape))
    return normalized_data, labels


def calculate_multiclass_micro_roc_auc(y, predictions):
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    # Compute micro-average ROC curve and ROC area
    fpr["micro"], tpr["micro"], _ = roc_curve(y.ravel(), predictions.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
    return fpr["micro"], tpr["micro"], roc_auc["micro"]


def calculate_overall_accuracy(y_true, predictions):
    total = 0.
    correct = 0.
    for y, p in zip(y_true, np.round(predictions)):
        and_operator = np.equal(y, p)
        total += and_operator.size
        correct += and_operator.sum()
    return correct / total
