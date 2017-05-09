import numpy as np
import pandas as pd

class SelectionMetrics:
    def __init__(self, metrics, ranks, n):
        self.metrics = np.array(metrics)
        self.noSelection = metrics[0]
        self.ranks = ranks.T
                
        all = range(len(self.ranks[0]))
        self.selections = [all]
        
        for rank in self.ranks:
            self.selections.append(rank[:n].tolist())

        self.df = self.compute_df()
        
                  
    def compute_df(self):
        np.set_printoptions(precision=3, suppress=True)
        
        row_label = ["no selection", "f-test", "ranksum", "chi2", "mi", "combined", "RFE"]
        col_label = ["f1", "precision", "recall", "accuracy", "TN", "FP", "FN", "TP"]

        df = pd.DataFrame(self.metrics, index=row_label, columns=col_label)

        df['TN'] = df['TN'].astype(int)
        df['FP'] = df['FP'].astype(int)
        df['FN'] = df['FN'].astype(int)
        df['TP'] = df['TP'].astype(int)

        # add the number of selected features, and the selection list
        ns = [len(li) for li in self.selections]
        df_ranks = pd.DataFrame({'n': ns, 'selection': self.selections}, index=row_label)

        df = df.join(df_ranks, how='right')
        return df
    
      
    def sort_f1():
        return self.df.sort_values('f1', ascending=False)
        
    def sort_recall():
        return self.df.sort_values('recall', ascending=False)
        
    def sort_precision():
            return self.df.sort_values('precision', ascending=False)
          
    def data_frame(self):
        return self.df
        
    def df(self):
        return self.data_frame()
        