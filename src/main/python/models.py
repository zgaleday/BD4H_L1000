from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_auc_score
from utils import calculate_multiclass_micro_roc_auc, calculate_overall_accuracy
from plotting import plot_roc_curve

RANDOM_SEED = 0


def multiclass_one_vs_rest(x, y, model_type='svm', plot=False, verbose=False):
    if model_type is 'logistic':
        base_model = LogisticRegression(random_state=RANDOM_SEED, class_weight='balanced')
    elif model_type is 'tree':
        base_model = DecisionTreeClassifier(random_state=RANDOM_SEED, class_weight='balanced')
    else:
        base_model = SVC(kernel='linear', random_state=RANDOM_SEED, class_weight='balanced')
    model = OneVsRestClassifier(base_model, n_jobs=10)
    model.fit(x, y)
    predictions = model.predict(x)
    micro_fpr, micro_tpr, micro_roc_auc_score = calculate_multiclass_micro_roc_auc(y, predictions)
    if verbose:
        print('one vs all ' + model_type + ' is a multi-label classifier: ' + str(model.multilabel_))
        print('one vs all ' + model_type + ' number of classes: ' + str(model.classes_))
        print('one vs all ' + model_type + ' predictions shape: ' + str(predictions.shape))
        print('one vs all ' + model_type + ' accuracy score: ' + str(calculate_overall_accuracy(y, predictions)))
        print('one vs all ' + model_type +
              ' roc score sklearn default: ' + str(roc_auc_score(y, predictions)) +
              ' micro-averaged: ' + str(micro_roc_auc_score))
    if plot is True:
        plot_roc_curve(micro_fpr, micro_tpr, micro_roc_auc_score, model_type)
    return predictions
