import time
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.metrics import roc_auc_score
from utils import calculate_multiclass_micro_roc_auc, calculate_overall_accuracy
from sklearn.neural_network import MLPClassifier
from plotting import plot_roc_curve

RANDOM_SEED = 0


def multiclass_one_vs_rest(x, y, model_type='svm', plot=False, verbose=False):
    if model_type is 'logistic':
        base_model = LogisticRegression(random_state=RANDOM_SEED, class_weight='balanced')
    elif model_type is 'tree':
        base_model = DecisionTreeClassifier(random_state=RANDOM_SEED, class_weight='balanced')
    elif model_type is 'adaboost':
        base_model = AdaBoostClassifier(random_state=RANDOM_SEED)
    elif model_type is 'forest':
        base_model = RandomForestClassifier(random_state=RANDOM_SEED, class_weight='balanced')
    elif model_type is 'nnet':
        base_model = MLPClassifier(random_state=RANDOM_SEED)
    else:
        base_model = SVC(kernel='linear', random_state=RANDOM_SEED, class_weight='balanced')
    model = OneVsRestClassifier(base_model, n_jobs=10)
    fit_start = time.time()
    model.fit(x, y)
    fit_end = time.time()
    predict_start = time.time()
    predictions = model.predict(x)
    predict_end = time.time()
    micro_fpr, micro_tpr, micro_roc_auc_score = calculate_multiclass_micro_roc_auc(y, predictions)
    if verbose:
        print('one vs all ' + model_type + ' elapsed training time: ' + str(fit_end - fit_start))
        print('one vs all ' + model_type + ' elapsed predicting time: ' + str(predict_end - predict_start))
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
