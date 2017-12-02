import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_auc_score

def plot_hist(y, title):
    plt.hist(y)
    plt.title(title)
    plt.ylabel('frequency')
    plt.show()


def plot_roc_curve(fpr, tpr, roc_auc, title_prefix):
    plt.figure()
    lw = 2
    plt.plot(fpr, tpr, color='darkorange', lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(title_prefix + ' receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.show()



def plot_combined_roc_curve(plot_data):
    
    lw = 2

    # plot the training curves first
    plt.figure(1)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')

    for model_type, data in plot_data.iteritems() :
        fpr, tpr, roc_auc, _, _, _ = data
        plt.plot(fpr, tpr, lw=lw, label= model_type + ' - ROC curve (area = %0.2f)' % roc_auc)

    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic - train')
    plt.legend(loc="lower right")


    plt.figure(2)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')

    for model_type, data in plot_data.iteritems() :
        _, _, _, fpr, tpr, roc_auc = data
        plt.plot(fpr, tpr, lw=lw, label=model_type + ' - ROC curve (area = %0.2f)' % roc_auc)

    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic - test')
    plt.legend(loc="lower right")

    plt.show()


def generate_accuracy_hist(y_test, predictions):
    """
    Read in the testing labels and the predicted labels on the test data and produced a histogram of accuracies (defined
    by assigning a higher probability to the correct label)
    :param y_test: the true labels on the test data used to generate predictions
    :param predictions: the predicted labels generate from the training data
    """
    hard_labels = np.round(predictions)
    diff_matrix = np.abs(y_test - hard_labels)
    perlabel_accuacy = 1 - np.mean(diff_matrix, axis=0)
    plt.hist(perlabel_accuacy, bins=7)
    plt.title("Accuracy of estimators")
    plt.show()


def generate_roc_hist(y_test, predictions):
    """
    See generate_accuracy hist only difference is the plot show AUCROC as opposed to accuracy.
    """
    roc_scores = []
    for col in range(y_test.shape[1]):
        y_col = y_test[:, col]
        pred_col = predictions[:, col]
        score = roc_auc_score(y_col, pred_col)
        roc_scores.append(score)
    roc_scores = np.array(roc_scores)
    plt.hist(roc_scores, bins=7, edgecolor='black')
    plt.title("ROCAUC of estimators")
    plt.show()