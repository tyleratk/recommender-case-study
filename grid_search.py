from surprise import AlgoBase, Dataset, evaluate, SVD, SVDpp
from surprise.evaluate import GridSearch

# ----------------  default params  --------------------
# SVD(n_factors=100, n_epochs=20, biased=True, init_mean=0, init_std_dev=0.1, lr_all=0.005, reg_all=0.02, lr_bu=None, lr_bi=None, lr_pu=None, lr_qi=None, reg_bu=None, reg_bi=None, reg_pu=None, reg_qi=None, verbose=False)


# param_grid = {'n_factors': [140, 160],
#               'n_epochs': [20, 30],
#               'lr_all': [0.001, 0.002],
#               'reg_all': [0.01, 0.02]}

param_grid = {'n_factors': [60, 70, 80, 90, 100]}
              
grid_search = GridSearch(SVD, param_grid, measures=['RMSE'])

data = Dataset.load_builtin('ml-100k')
data.split(n_folds=3)

grid_search.evaluate(data)

# best RMSE score
print('Best RMSE: {:.3f}'.format(grid_search.best_score['RMSE']))
print('Best RMSE params:{}'.format(grid_search.best_params['RMSE']))

