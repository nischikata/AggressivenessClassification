from Utils.univariate_featureSelection import featureSelectionResults, get_selectedFeatures
import numpy as np
import pandas as pd



# computes
def get_stepwise_results(dev, val, rankfile, rfe_file):
    dfs = []
    for i in range(1, 69):
        results = featureSelectionResults(dev, val, rankfile, rfe_file, i)
        df = results.data_frame()
        dfs.append(df)
    return dfs



def get_stepwise_scores(dfs, scorename='f1', start=1, end=69):
    """
    this is mainly useful for plotting
    """
    noselection = []
    RFE = []
    combined= []
    chi = []
    mi = []
    ranksum = []
    ftest = []

    for df in dfs[start:end]:
        noselection.append(df[scorename]['no selection'])
        RFE.append(df[scorename]['RFE'])
        combined.append(df[scorename]['combined'])
        ftest.append(df[scorename]['f-test'])
        ranksum.append(df[scorename]['ranksum'])
        chi.append(df[scorename]['chi2'])
        mi.append(df[scorename]['mi'])
    
    return noselection, RFE, combined, ftest, ranksum, chi, mi


def get_logReg_featureSelectionResults(univariate_dfs, lasso_df, out="Datasets/MODEL_LR_results.csv"):
    """
    This very important function ranks the different selections by their f1 score. Awesome!
    """
    source_label = ["no selection (L1)", "f-test", "ranksum", "chi2", "mi", "combined", "RFE"]
    df0 = univariate_dfs[0]
    df0['source'] = source_label
    results = [df0]
    
    for df in univariate_dfs[1:]:
        df['source'] = source_label
        results.append(df[1:]) # do not add 'no selection' here (repeatedly)
        
    results.append(lasso_df)

    appended_results = pd.concat(results, axis=0)
    appended_results = appended_results.sort_values('f1', ascending=False)
    appended_results.index = range(len(appended_results))

    # save results in cvs
    appended_results.to_csv(out, sep='\t')
    
    return appended_results


def plot_stepwise_scores(noselection, RFE, combined, ftest, ranksum, chi, mi, start=0, end=68, title="my dataset", scorename='f1 score'):
    if end > len(noselection):
        end = len(noselection)
    x_axis = np.arange(start, end)

    plt.plot(x_axis,noselection[start:end], color="red", linewidth=3, linestyle="-", label="no selection")
    plt.plot(x_axis,RFE[start:end], color="green", linewidth=2, linestyle="-", label="RFE") 
    plt.plot(x_axis,ftest[start:end], color="blue", linewidth=2, linestyle="-", label="f-test") 
    plt.plot(x_axis,ranksum[start:end], color="pink", linewidth=2, linestyle="-", label="ranksum") 
    plt.plot(x_axis,chi[start:end], color="orange", linewidth=2, linestyle="-", label="chi2") 
    plt.plot(x_axis,mi[start:end], color="#98df8a", linewidth=2, linestyle="-", label="mi") 
    plt.plot(x_axis,combined[start:end], color="#aec7e8", linewidth=2, linestyle="-", label="combined") 
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.suptitle(title)
    plt.xlabel('n Features')
    plt.ylabel(scorename)
    plt.show()

# Usage:

# from Utils.setupDataset import get_dataset
# from Utils.lasso_selections import get_LassoSelectionResults

#m_dev = get_dataset("Datasets/M_DEV_dataset.pickle")
#w_dev = get_dataset("Datasets/W_DEV_dataset.pickle")
#m_val = get_dataset("Datasets/M_VAL_dataset.pickle")
#w_val = get_dataset("Datasets/W_VAL_dataset.pickle")

#m_filename = 'Datasets/M_SELECTIONS_univariate.csv'
#w_filename = 'Datasets/W_SELECTIONS_univariate.csv'


#m_rfe = 'Datasets/M_SELECTIONS_RFE.csv'
#w_rfe = 'Datasets/W_SELECTIONS_RFE.csv'

#m_dfs = get_stepwise_results(m_dev, m_val, m_filename, m_rfe)

#m_sel_lasso = "Datasets/M_SELECTIONS_lasso.pickle"
#w_sel_lasso = "Datasets/W_SELECTIONS_lasso.pickle"

#m_lasso = get_LassoSelectionResults(m_dev, m_val, m_sel_lasso)
#w_lasso = get_LassoSelectionResults(w_dev, w_val, w_sel_lasso)

# # compute the Ranking of the different Selections (Univariate, RFE, Lasso)
#m_lasso_df = get_logReg_featureSelectionResults(m_dfs, m_lasso, out="Datasets/M_MODEL_LR_results.csv")

#noselection, RFE, combined, ftest, ranksum, chi, mi = get_stepwise_scores(m_dfs, scorename='f1')
#plot_stepwise_scores(noselection, RFE, combined, ftest, ranksum, chi, mi)

# To Load Selections Ranking File:
# df_loaded = pd.read_csv("Datasets/M_MODEL_LR_results.csv", sep='\t', index_col=0)