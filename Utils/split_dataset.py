import numpy as np
from sklearn.utils import shuffle
from setupDataset import get_dataset, save

def separateByCategory(dataset):
    """
    splits the given dataset into two arrays
    good: containing not aggressive data
    bad: containing aggressive data
    """
    X = dataset["data"]
    y = dataset["target"]

    # 1. separate into good / bad
    indices_good = np.where(y == 0)
    indices_bad = np.where(y == 1)
    
    good = X[indices_good]
    bad = X[indices_bad]
    return good, bad


def concatSets(good, bad, random_state=4):
    """
    combines two given arrays (first: non aggressive data, second: aggressive data)
    into a single dataset (target included)
    """
        # create target X for good/bad
    gy = np.zeros(len(good))
    by = np.ones(len(bad))
    
    # now combine the good & bad chunk
    data = np.concatenate([good, bad])
    target = np.concatenate([gy, by])
    
    # shuffling must use same random state!
    shuffle(data, random_state=4)
    shuffle(target, random_state=4)
    
    return { "data": data, "target": target}
    

def getTestSets(good, bad, k=5):
    """
    good: array containing non aggressive data
    bad: array containing aggressive data
    k: the number of test datasets the given data should be split into
    
    returns a list of k datasets (each  { "data": data, "target": target})
    """
    # shuffle the rows first (always shuffle the same for reproducible results)
    shuffle(good, random_state=3)
    shuffle(bad, random_state=7)
    
    #split the dataset into k equal-sized chunks 
    g = np.array_split(good, k)
    b = np.array_split(bad, k)
    
    datasets = []
    
    for i in range(k):     
        datasets.append(concatSets(g[i], b[i]))
    
    return datasets


def get_devSet_validationSet(good, bad):
    """
    seperates the dataset into 3/4 for initial testing (used for grid tests)
    and 1/4 for the final test
    """
    frac = 4
    # shuffle the rows first
    shuffle(good, random_state=0)
    shuffle(bad, random_state=1)
    
    validatationSet = concatSets(good[:len(good)//frac], bad[:len(bad)//frac], 3) # // ... integer division
    devSet = concatSets(good[len(good)//frac:], bad[len(bad)//frac:], 7)
   
    #newgood = good[len(good)//frac:] # 3/4 of good
    #newbad = bad[len(bad)//frac:] # 3/4 of bad
    
    return devSet, validatationSet
 
  
def save_devSet_valSet(inFile, devFile="DEV_DATASET.pickle", valFile="VAL_DATASET.pickle"):
    dataset = get_dataset(inFile)
    good, bad = separateByCategory(dataset)
    devSet, valSet = get_devSet_validationSet(good, bad)
    print "devset ", len(devSet["target"]), "  valset: ", len(valSet["target"])
    save(devSet, devFile)
    save(valSet, valFile)
    
# Usage:
"""   
dataset = get_dataset("dataset.pickle")
good, bad = separateByCategory(dataset)
good, bad, validate = get_testSet_validationSet(good, bad)
sets = getTestSets(good, bad)
""" 