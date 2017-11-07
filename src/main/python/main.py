from utils import get_train_test_data
from models import multiclass_one_vs_rest
from features import reduce_dimensionality

x_train, x_test, y_train, y_test, x, y = get_train_test_data()
# multiclass_one_vs_rest(x, y, 'logistic')
projected_data, alg = reduce_dimensionality(x)
print(alg.singular_values_)
