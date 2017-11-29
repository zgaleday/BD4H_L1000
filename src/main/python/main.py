from utils import get_train_test_data
from models import multiclass_one_vs_rest
from features import compute_target_distribution
from plotting import plot_combined_roc_curve

x, y = get_train_test_data()
target_distribution = compute_target_distribution(y, plot=False, verbose=False)


plot_data = {}

for model_type in ["logistic", "tree", "forest", "nnet", "adaboost", "extra", "SVC"] :
# for model_type in ["logistic"] : #, "tree"] :
    plot_data[model_type] = multiclass_one_vs_rest(x, y, model_type, plot=False, verbose=True, run_cv=False)


plot_combined_roc_curve(plot_data)
