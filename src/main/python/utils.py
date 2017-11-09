import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import numpy as np

scaler = MinMaxScaler()


def get_train_test_data():
    # read in data, drop CID, and drop columns that have any null values, e.g. NaN
    raw_data = pd\
        .read_csv('../../../data/pandas_input_combined.csv')\
        .dropna(axis=1, how='all')\
        .drop('CID', axis=1)
    # build labels by squishing ADR columns
    labels = raw_data[raw_data.columns[raw_data.columns.str.contains('C')]].values
    # drop all ADR columns as they're captured in the labels
    cols_to_keep = [c for c in raw_data.columns if c[0] != 'C']
    raw_data = raw_data[cols_to_keep]
    #drop infrequent rows
    adr_count = np.sum(labels, axis=0)
    labels = labels[:, (adr_count < (labels.shape[0] * 0.9))]
    labels = labels[:, (adr_count > (labels.shape[0] * 0.1))]
    # min-max normalization of features
    normalized_data = pd.DataFrame(scaler.fit_transform(raw_data))
    print("normalized design matrix shape: " + str(normalized_data.shape))
    print("labels shape: " + str(labels.shape))
    # cross-validate split
    x_train, x_test, y_train, y_test = train_test_split(normalized_data, labels, test_size=0.4, random_state=0)
    print("training data shape: " + str(x_train.shape) + ' ' + str(y_train.shape))
    print("test data shape: " + str(x_test.shape) + ' ' + str(y_test.shape))
    return x_train, x_test, y_train, y_test, normalized_data, labels


