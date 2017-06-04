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
get_y = lambda df, n, score='f1': None if (len(df.loc[df['n'] == n]) == 0) else df.loc[df['n'] == n][score].iloc[0]

def plot_results(df, start=1, end=68, title='Feature Selection Results', score='f1', ybottom=0.65):
    end += 1
    if end > 69:
        end = 69
    
    x_axis = np.arange(start, end)
    y_axis = {}
    # 1. unique sources
    sources = df['source'].unique()
    sources = sorted(sources, key=len, reverse=True)
    
    #color_sequence = ['r', 'crimson', 'blue', 'dodgerblue', 'lightskyblue', 'aqua', 'orange', 'gold', 'greenyellow']
    color=cm.rainbow([0.01,0.19,0.29,0.43,0.59, 0.69, 0.75,0.82,0.9]) #np.linspace(0,0.95,9))
    colors = []
    for i,c in zip(range(9),color):
        colors.append(c)
    np.linspace(0,0.95,9)
    colors = reversed(colors)
    
    plt.rc('axes', prop_cycle=(cycler('color', colors))) 
    plt.rcParams['axes.facecolor'] = 'whitesmoke' #plot bg color
    
    for source in sources:
        # new dataframe with only a specific source (like 'Lasso' or 'ranksum')
        sdf = df.loc[df['source'] == source]
        if len(sdf) == 1: # no selection - print one line
            y = [sdf[score].iloc[0] for n in x_axis]
            plt.plot(x_axis, y, linestyle='-', linewidth=5, label=source)
        # define values for this sources y-axis, 
        else:
            y = [get_y(sdf, n) for n in x_axis]       
            series = np.array(y).astype(np.double)
            mask = np.isfinite(series) #mask out None values
        
            plt.plot(x_axis[mask], series[mask], linestyle='-', linewidth=3, marker='h', markersize=9, alpha=0.65,
                     label=source, path_effects=[pe.SimpleLineShadow(shadow_color='#999999'), pe.Normal()]) 
    
    plt.xticks(np.arange(start, max(x_axis)+1, 5.0))
    plt.yticks(np.arange(ybottom, max(df['f1'])+0.01, 0.01)) # y-axis spacing of grid
    plt.gca().set_ylim(ybottom) # start
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.suptitle(title, fontsize=24)
    plt.xlabel('n Features')
    plt.ylabel(score + "-score")
      
    plt.show()
    
def get_plotableFeatures():
     return [1,2,3,7,8,9,10,12,15,16,17,18,21,36,37,38,39,40,41,42,43,44,45]
     

def plot_featureDistribution(dataset, f_index):
    
    ok = get_plotableFeatures()
    fnames = get_feature_names()
    fname = fnames[f_index]
    
    if f_index in ok:
    
        good, bad = separateByCategory(dataset)

        max_val = max(dataset["data"][:,f_index]).astype(int)

        fig = plt.figure()
        ax = fig.add_subplot(111)

        numBins = max_val
        ax.hist(good[:,f_index].astype(int),numBins, color='lime', alpha=0.9, label='ok')
        ax.hist(bad[:,f_index],numBins,color='orangered', alpha=0.6, label='aggressive')
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
    chi = []
    mi = []
    for i, c in enumerate(combined[:n]):
       
        index = np.where(df['f']==c)[0][0]
        ftest.append(index+1)
        index = np.where(df['ranksum']==c)[0][0]
        ranksum.append(index+1)
        index = np.where(df['chi']==c)[0][0]
        chi.append(index+1)
        index = np.where(df['mi']==c)[0][0]
        mi.append(index+1)
    
    color=cm.rainbow([0.2, 0.35,0.67,0.8])
    colors = []
    for i,c in zip(range(9),color):
        colors.append(c)
    np.linspace(0,0.95,9)
    
    plt.rc('axes', prop_cycle=(cycler('color', colors))) 
    fig, ax = plt.subplots()
    index = x_axis
    bar_width = 0.15
    opacity = 0.8
    
    
    
    ax.yaxis.set_major_locator(MaxNLocator(integer=True)) # force y labels to be integer
    
    fbar = plt.bar(x_axis, ftest, bar_width, alpha=opacity, label="f-test")
    rankbar = plt.bar(x_axis + bar_width, ranksum, bar_width, alpha=opacity, label="ranksum")
    chibar = plt.bar(x_axis + bar_width*2, chi, bar_width, alpha=opacity, label="chi2")
    mibar = plt.bar(x_axis + bar_width*3, mi, bar_width, alpha=opacity, label="mi")
    plt.xticks(x_axis + bar_width*1.5, combined[:n])
    plt.suptitle("\n"+ title +" - Top " + str(n) + " univariate Features", fontsize=24)
    plt.xlabel("feature index")
    plt.ylabel('feature rank')
    plt.legend()
    plt.show()
    
# USAGE
# from Utils.plot_results import plot_results
# df = pd.read_csv("Datasets/M_MODEL_LR_results.csv", sep='\t', index_col=0)
# plot_results(df, score="f1")
