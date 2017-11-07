from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score


def multiclass_one_vs_rest(x, y, model_type='svm'):
    if model_type is 'logistic':
        base_model = LogisticRegression()
    else:
        base_model = SVC(kernel='linear')
    model = OneVsRestClassifier(base_model, n_jobs=10)
    model.fit(x, y)
    predictions = model.predict(x)
    print('one vs all ' + model_type + ' accuracy score: ' + str(accuracy_score(y, predictions)))
    print('one vs all ' + model_type + ' roc score: ' + str(roc_auc_score(y, predictions)))
    return predictions
