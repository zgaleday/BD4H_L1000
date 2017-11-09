from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, roc_auc_score

RANDOM_SEED = 0


def multiclass_one_vs_rest(x, y, model_type='svm'):
    if model_type is 'logistic':
        base_model = LogisticRegression(random_state=RANDOM_SEED)
    elif model_type is 'neural_network':
        base_model = MLPClassifier(hidden_layer_sizes=(1000,), max_iter=5000, random_state=RANDOM_SEED)
    else:
        base_model = SVC(kernel='linear', random_state=RANDOM_SEED)
    model = OneVsRestClassifier(base_model, n_jobs=10)
    model.fit(x, y)
    predictions = model.predict(x)
    print(predictions.shape)
    print('one vs all ' + model_type + ' accuracy score: ' + str(accuracy_score(y, predictions)))
    print('one vs all ' + model_type + ' roc score: ' + str(roc_auc_score(y, predictions)))
    return predictions


def softmax_neural_network(x, y):
    model = MLPClassifier(hidden_layer_sizes=(1000,), max_iter=5000, random_state=RANDOM_SEED)
    model.fit(x, y)
    predictions = model.predict(x)
    print('neural network accuracy score: ' + str(accuracy_score(y, predictions)))
    print('neural network roc score: ' + str(roc_auc_score(y, predictions)))
    return predictions
