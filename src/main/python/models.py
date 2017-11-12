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

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import make_scorer

RANDOM_SEED = 0


def check_predictions(model, model_type, x, y, plot, verbose) :
    
    predict_start = time.time()
    predictions = model.predict(x)
    predict_end = time.time()

    micro_fpr, micro_tpr, micro_roc_auc_score = calculate_multiclass_micro_roc_auc(y, predictions)

    if verbose:
        print('one vs all ' + model_type + ' elapsed predicting time: ' + str(predict_end - predict_start))
        print('one vs all ' + model_type + ' predictions shape: ' + str(predictions.shape))
        print('one vs all ' + model_type + ' accuracy score: ' + str(calculate_overall_accuracy(y, predictions)))
        print('one vs all ' + model_type +
              ' roc score sklearn default: ' + str(roc_auc_score(y, predictions)) +
              ' micro-averaged: ' + str(micro_roc_auc_score))

    if plot is True:
        plot_roc_curve(micro_fpr, micro_tpr, micro_roc_auc_score, model_type)


    return micro_fpr, micro_tpr, micro_roc_auc_score




def multiclass_one_vs_rest(x, y, model_type='svm', plot=False, verbose=False, run_cv=False):

    # First split the data into training and test sets
    x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.33, random_state=RANDOM_SEED)
    

    # pick the base classifier based on the model_type paramemter
    if model_type is 'logistic':
        base_model = LogisticRegression(random_state=RANDOM_SEED, class_weight='balanced')

    elif model_type is 'tree':
        base_model = DecisionTreeClassifier(random_state=RANDOM_SEED, class_weight='balanced')

    elif model_type is 'adaboost':
        base_model = AdaBoostClassifier(random_state=RANDOM_SEED)

    elif model_type is 'forest':
        # base case
        base_model = RandomForestClassifier(random_state=RANDOM_SEED, class_weight='balanced')

        # this gives no improvement over base case
        #base_model = RandomForestClassifier(random_state=RANDOM_SEED, class_weight='balanced', n_estimators = 50, max_depth=20)
        
        # no improvement here either
        #base_model = RandomForestClassifier(random_state=RANDOM_SEED, class_weight='balanced', n_estimators = 100, max_depth=40)

    elif model_type is 'nnet':
        base_model = MLPClassifier(random_state=RANDOM_SEED)

    else:
        #base case
        base_model = SVC(kernel='linear', random_state=RANDOM_SEED, class_weight='balanced')

        # no improvement here 
        #base_model = SVC(kernel='linear', random_state=RANDOM_SEED, class_weight='balanced', activation="logistic", max_iter=500)

    # create the OvR model using the base classifier
    model = OneVsRestClassifier(base_model, n_jobs=10)

    # train the model using the training data
    fit_start = time.time()
    model.fit(x_train, y_train)
    fit_end = time.time()

    if verbose:
        print('------ model info ----------')
        print('one vs all ' + model_type + ' is a multi-label classifier: ' + str(model.multilabel_))
        print('one vs all ' + model_type + ' number of classes: ' + str(model.classes_))
        print('one vs all ' + model_type + ' elapsed training time: ' + str(fit_end - fit_start))

    # check the accuracy on the training data
    if verbose:
        print('------ training data ----------')

    fpr_train, tpr_train, auc_train = check_predictions(model, (model_type + " - train"), x_train, y_train, plot, verbose)
    
    # check the accuracy on the test data
    if verbose:
        print('------ test data ----------')

    fpr_test, tpr_test, auc_test =  check_predictions(model, (model_type + " - test"), x_test, y_test, plot, verbose)

    # get the cross-validation score
    if run_cv :
        
        accuracy_scorer = make_scorer(calculate_overall_accuracy)
        cv_accuracy_scores = cross_val_score(model, x, y, scoring=accuracy_scorer, cv=5)
        cv_auc_scores = cross_val_score(model, x, y, scoring="roc_auc", cv=5)
    
        if verbose:
            print('------ CV scores ----------')
            print('one vs all ' + model_type + ' CV accuracy scores ' + str(cv_accuracy_scores))
            print('one vs all ' + model_type + ' CV AUC scores ' + str(cv_auc_scores))

            
    return fpr_train, tpr_train, auc_train, fpr_test, tpr_test, auc_test
