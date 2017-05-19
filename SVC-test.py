from __future__ import print_function

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.metrics import f1_score

# 1. load data (DEV set)
X_dev, y_dev

# apply feature selection


# 2. scale data (TODO)

# # set the parameters by cross validation
tuning_params = [ {'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1,10,100,1000] },
                  {'kernel': ['linear'], 'C': [1,10,100,1000]}]
                  
clf = GridSerachCV(SVC(C=1), tuning_params, cv=5, scoring=f1_score)

clf.fit(X_dev, y_dev)
print clf.best_params