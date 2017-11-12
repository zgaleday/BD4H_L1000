from utils import get_train_test_data
from models import multiclass_one_vs_rest
from features import compute_target_distribution

x, y = get_train_test_data()
target_distribution = compute_target_distribution(y, plot=False, verbose=False)


#for model_type in ["logistic", "tree", "forest", "nnet", "adaboost"] :
for model_type in ["nnet"] :
    multiclass_one_vs_rest(x, y, model_type, plot=False, verbose=True, run_cv=False)
