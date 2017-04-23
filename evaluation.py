from sklearn.grid_search import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from setupDataset import get_dataset
from sklearn.linear_model import LogisticRegressionCV
import numpy as np
from sklearn.cross_validation import KFold




#TODO load data
dataset = get_dataset()

X = dataset["data"]
y = dataset["target"]

#fold = KFold(len(y), n_folds=5, shuffle=True)

knn = KNeighborsClassifier()


# 1. define the paramter values that should be searched
# TODO: LASSSOOOO
k_range = range(21, 40)
"""
# 2. create a paramteter gridL map the parameter names to the values that should be searched
param_grid = dict(n_neighbors=k_range)
print param_grid

# 3. instantiate the grid
grid = GridSearchCV(knn, param_grid, cv=5, scoring='precision')

# 4. fit the grid with data

grid.fit(X, y)


# view the complete results (list of named tuples)
print grid.grid_scores_

print grid.best_score_
print grid.best_params_
print grid.best_estimator_

"""
searchCV = LogisticRegressionCV(
    penalty='l1'
#    ,scoring='accuracy_score'
    ,cv=5
    ,max_iter=10000
    ,fit_intercept=True
    ,solver='liblinear'
)
searchCV.fit(X, y)

print ('Max prec:', searchCV.scores_[1].max())
print "score: ", searchCV.scores_

#print "best score", searchCV.best_score_
#print "best params", searchCV.best_params_
#print "best estimator", searchCV.best_estimator_