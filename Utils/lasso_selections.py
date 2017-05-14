from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LassoCV
import numpy as np
from Utils.setupDataset import get_dataset, save, load


def get_LassoSelections(dataset, out='SELECTIONS_lasso.pickle', step=0.005, maxThresh=0.25, minThresh=0.000005):
    X = dataset["data"]
    y = dataset["target"]
    
    thr_range =  np.arange(0.000005, 0.25, 0.005)
    no_selection = np.arange(0,68)
    
    selections = [no_selection]
    
    for thresh in thr_range:
        
        clf = LassoCV()
        sfm = SelectFromModel(clf, threshold=thresh)
        sfm.fit(X,y)
        sel = sfm.get_support(indices=True)
        n_features = sfm.transform(X).shape[1]
        
        if len(sel) > 0 and len(sel) != len(selections[-1]):
            selections.append(sel)
          
    selections.reverse()
    save(selections, out)
    return selections


"""
    # USAGE
from Utils.setupDataset import get_dataset, save, load

m_devSet = get_dataset("Datasets/M_DEV_dataset.pickle")
w_devSet = get_dataset("Datasets/W_DEV_dataset.pickle")

get_LassoSelections(m_devSet, out='Datasets/M_SELECTIONS_lasso.pickle')
get_LassoSelections(w_devSet, out='Datasets/W_SELECTIONS_lasso.pickle')

m_lasso_selections = load('Datasets/M_SELECTIONS_lasso.pickle')
w_lasso_selections = load('Datasets/W_SELECTIONS_lasso.pickle')

print m_lasso_selections, "\n\n"
print w_lasso_selections
"""