import matplotlib.pyplot as plt


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


    
