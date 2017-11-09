from utils import get_train_test_data
from models import multiclass_one_vs_rest
from features import compute_target_distribution

x, y = get_train_test_data()
distribution = compute_target_distribution(y, plot=False, verbose=True)
predictions = multiclass_one_vs_rest(x, y, 'tree', plot=False, verbose=True)
