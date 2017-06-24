import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.pyplot import cm
import pandas as pd
import numpy as np
from cycler import cycler
from Utils.split_dataset import separateByCategory
from Utils.feature_vector import get_feature_names
from matplotlib.ticker import MaxNLocator
from Utils.feature_ranking import load_rankSelections

plt.style.use('seaborn-poster')
plt.style.use('seaborn-darkgrid')

# get f1 value for a specific n; if there are no values for a specific x value the value will be set to None
get_y = lambda df, n, score: None if (len(df.loc[df['n'] == n]) == 0) else df.loc[df['n'] == n][score].iloc[0]


def plot_results(df, start=1, end=68, title='Feature Selection Results', score=None, ybottom=0.65):
    if score==None:
        score='f1'
        
    end += 1
    if end > 69:
        end = 69
    
    x_axis = np.arange(start, end)
    y_axis = {}
    # 1. unique sources
    sources = df['source'].unique()
    sources = sorted(sources, key=len, reverse=True)
    
    #color_sequence = ['r', 'crimson', 'blue', 'dodgerblue', 'lightskyblue', 'aqua', 'orange', 'gold', 'greenyellow']
    #color=cm.rainbow([0.01,0.19,0.29,0.43,0.59, 0.69, 0.75,0.82,0.9]) #np.linspace(0,0.95,9))
    color=cm.rainbow([0.01,0.19,0.43,0.62, 0.71, 0.82,0.9]) #np.linspace(0,0.95,9))
    colors = []
    for i,c in zip(range(9),color):
        colors.append(c)
    np.linspace(0,0.95,9)
    colors = reversed(colors)
    
    plt.rc('axes', prop_cycle=(cycler('color', colors))) 
    plt.rcParams['axes.facecolor'] = 'whitesmoke' #plot bg color
    
    source_dict = {'f-test': 'T-Test', 'mi': 'Mutal Information', 'ranksum': 'Wilcoxon Rank-Sum Test', 'Lasso': 'Lasso', 'RFE': 'RFE', 'combined': 'combined', 'no selection': 'no selection'}
    
    for source in sources:
        # new dataframe with only a specific source (like 'Lasso' or 'ranksum')
        sdf = df.loc[df['source'] == source]
        if len(sdf) == 1: # no selection - print one line
            y = [sdf[score].iloc[0] for n in x_axis]
            plt.plot(x_axis, y, linestyle='-', linewidth=5, label=source)
        # define values for this sources y-axis, 
        else:
            y = [get_y(sdf, n, score) for n in x_axis]       
            series = np.array(y).astype(np.double)
            mask = np.isfinite(series) #mask out None values
        
            plt.plot(x_axis[mask], series[mask], linestyle='-', linewidth=3, marker='h', markersize=9, alpha=0.65,
                     label=source_dict[source], path_effects=[pe.SimpleLineShadow(shadow_color='#999999'), pe.Normal()]) 
    
    plt.xticks(np.arange(start, max(x_axis)+1, 5.0))
    plt.yticks(np.arange(ybottom, max(df[score])+0.01, 0.01)) # y-axis spacing of grid
    axes = plt.gca()
    axes.set_ylim([ybottom, max(df[score])+0.01])
    plt.gca().set_ylim(ybottom) # start
    #plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.3)
    plt.legend(loc=5, borderaxespad=0.3)
    #plt.legend(loc=5)
    plt.suptitle(title, fontsize=24)
    plt.xlabel('n Features')
    plt.ylabel(score + "-score")
      
    plt.show()
    
def get_plotableFeatures():
     return [1,2,3,7,8,9,10,12,15,16,17,18,21,36,37,38,39,40,41,42,43,44,45]
     

def plot_featureDistribution(dataset, f_index):
    
    ok = get_plotableFeatures()
    fnames = get_feature_names()
    fname = fnames[f_index][8:]
    
    if f_index in ok:
    
        good, bad = separateByCategory(dataset)

        max_val = max(dataset["data"][:,f_index]).astype(int)

        fig = plt.figure()
        ax = fig.add_subplot(111)

        numBins = max_val
        ax.hist(good[:,f_index].astype(int),numBins, color='lime', alpha=0.9, label='ok')
        ax.hist(bad[:,f_index],numBins,color='orangered', alpha=0.6, label='aggressive')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True)) # force x labels to be integer
        ax.yaxis.set_major_locator(MaxNLocator(integer=True)) # force y labels to be integer
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.suptitle("\n" + fname + " [" + str(f_index) + "]", fontsize=24)
        plt.xlabel('feature value')
        plt.ylabel("frequency")
        plt.show()
    else:
        print "Feature ", fname ," (", f_index, ") cannot be plotted (integer features only)"
    
 
def plot_topRanked(file, n=5, title=""):
    df = pd.read_csv(file, sep='\t', index_col=0)
    
    combined = df['combined']
    x_axis = np.arange(0,n)
    ftest = []
    ranksum = []
    #chi = []
    mi = []
    for i, c in enumerate(combined[:n]):
       
        index = np.where(df['f']==c)[0][0]
        ftest.append(index+1)
        index = np.where(df['ranksum']==c)[0][0]
        ranksum.append(index+1)
        #index = np.where(df['chi']==c)[0][0]
        #chi.append(index+1)
        index = np.where(df['mi']==c)[0][0]
        mi.append(index+1)
    
    color=cm.rainbow([0.2, 0.35,0.67,0.8])
    #color=cm.rainbow([0.02, 0.32,0.68])
    colors = []
    for i,c in zip(range(9),color):
        colors.append(c)
    #np.linspace(0,0.95,9)
    
    #colors = ['yellow', 'blue', 'pink']
    plt.rc('axes', prop_cycle=(cycler('color', colors))) 
    fig, ax = plt.subplots()
    index = x_axis
    bar_width = 0.15
    opacity = 0.8
    
    
    
    ax.yaxis.set_major_locator(MaxNLocator(integer=True)) # force y labels to be integer
    
    fbar = plt.bar(x_axis, ftest, bar_width, alpha=opacity, label="T-Test")
    rankbar = plt.bar(x_axis + bar_width, ranksum, bar_width, alpha=opacity, label="Wilcoxon Rank-Sum Test")
    #chibar = plt.bar(x_axis + bar_width*2, chi, bar_width, alpha=opacity, label="chi2")
    mibar = plt.bar(x_axis + bar_width*2, mi, bar_width, alpha=opacity, label="Mutual Information")
    plt.xticks(x_axis + bar_width*1.5, combined[:n])
    plt.suptitle("\n"+ title +" - Top " + str(n) + " Univariate Features", fontsize=24)
    plt.xlabel("feature index")
    plt.ylabel('feature rank')
    plt.legend()
    plt.show()
    
    
def plot_uni_VS_RFE(uni_file, rfe_file,n=30): #15 or 30 seems resonable
    uni_df = pd.read_csv(uni_file, sep='\t', index_col=0)
    RFE_df = pd.read_csv(rfe_file, sep='\t', index_col=0)
    
    combined = uni_df['combined']
    RFE = RFE_df['RFE']
    scatterplot_2rankings(combined, RFE, n, title_x="Combined Univariate", title_y="RFE")
    #scatterplot_2rankings(RFE,combined, n, title_y="Combined Univariate", title_x="RFE")
    
    
def plot_ftest_VS_RFE(uni_file, rfe_file,n=30): #15 or 30 seems resonable
    uni_df = pd.read_csv(uni_file, sep='\t', index_col=0)
    RFE_df = pd.read_csv(rfe_file, sep='\t', index_col=0)
    
    combined = uni_df['f']
    RFE = RFE_df['RFE']
    scatterplot_2rankings(combined, RFE, n, title_x="F-Test", title_y="RFE")
    #scatterplot_2rankings(RFE,combined, n, title_y="Combined Univariate", title_x="RFE")
    
def plot_ranksum_VS_RFE(uni_file, rfe_file,n=30): #15 or 30 seems resonable
    uni_df = pd.read_csv(uni_file, sep='\t', index_col=0)
    RFE_df = pd.read_csv(rfe_file, sep='\t', index_col=0)
    
    combined = uni_df['ranksum']
    RFE = RFE_df['RFE']
    scatterplot_2rankings(combined, RFE, n, title_x="Ranksum", title_y="RFE")
    #scatterplot_2rankings(RFE,combined, n, title_y="Combined Univariate", title_x="RFE")
    
def plot_mi_VS_RFE(uni_file, rfe_file,n=30): #15 or 30 seems resonable
    uni_df = pd.read_csv(uni_file, sep='\t', index_col=0)
    RFE_df = pd.read_csv(rfe_file, sep='\t', index_col=0)
    
    combined = uni_df['mi']
    RFE = RFE_df['RFE']
    scatterplot_2rankings(combined, RFE, n, title_x="Mutual Information", title_y="RFE")
    
    
def plot_f_VS_mi(uni_file,n=30): #15 or 30 seems resonable
        uni_df = pd.read_csv(uni_file, sep='\t', index_col=0)
        f = uni_df['f']
        ranksum = uni_df['combined']

        scatterplot_2rankings(f, ranksum, n, title_x="T-test", title_y="Mutual Information (MI)")
    



def scatterplot_2rankings(df_x, df_y, n, title_x, title_y):

    x_axis = np.arange(0,n)
    
    matplotlib.rc('xtick', labelsize=16) 
    matplotlib.rc('ytick', labelsize=16)

    ys = []
    for i in range(0,n):
        #TODO check wo wert in combined[i] ist welcher index von RFE
        # dieser index ist hier das y        
        val = df_x[i]
        y = list(np.where(df_y == val))[0][0]
        ys.append(y)
        
    
    max_y = max(ys)
    y_axis= np.arange(0, max_y + 1)
    print max_y
    
    y_stretch = n*1.5 # the y_axis is 1.5 times the tick-size of the x-axis (n ticks)
    
    paperheight = y_stretch* 0.75
    paperwidth = n * 0.75
    margin = 1.0
    
    plt.figure(figsize=(paperwidth - 2*margin, paperheight - 2*margin))
        
    plt.scatter(x_axis, ys)    
    plt.yticks(y_axis, df_y)
    plt.xticks(x_axis, df_x)
    plt.xlabel("Feature Indices  -  " + title_x +" Ranking")
    plt.ylabel("Feature Indices  -  " + title_y + "Ranking")
    
    axes = plt.gca()
    axes.set_xlim([-1,n])

    axes.set_ylim([-1,y_stretch])
    #axes.set_ylim([-1,max_y+1])
    
    plt.legend()
    
    plt.show()
    
# USAGE
# from Utils.plot_results import plot_results
# df = pd.read_csv("Datasets/M_MODEL_LR_results.csv", sep='\t', index_col=0)
# plot_results(df, score="f1")
