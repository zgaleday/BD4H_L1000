from utils import get_train_test_data
from models import multiclass_one_vs_rest, softmax_neural_network
from features import reduce_dimensionality

x_train, x_test, y_train, y_test, x, y = get_train_test_data()
print(x.head(2))
print(y[1])
# multiclass_one_vs_rest(x, y, 'logistic')
# softmax_neural_network(x.values, y)
# projected_data, alg_obj = reduce_dimensionality(x)
