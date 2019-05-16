
#%%
get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib.pyplot as plt

import pandas as pd


#%%
Hl = pd.read_csv("hailun.csv")
cols=['km','game','ice']
label=['label']


#%%
from sklearn import tree
dtr=tree.DecisionTreeClassifier(max_depth = 3)
dtr.fit(Hl[cols], Hl[label])


#%%
dot_data =     tree.export_graphviz(
        dtr,
        out_file = None,
        feature_names = cols,
        filled = True,
        impurity = False,
        rounded = True
    )


#%%
import pydotplus
graph = pydotplus.graph_from_dot_data(dot_data)
from IPython.display import Image
Image(graph.create_png())


#%%
from sklearn.model_selection import train_test_split
data_train, data_test, target_train, target_test =     train_test_split(Hl[cols], Hl[label], test_size = 0.1, random_state = 42)
dtr = tree.DecisionTreeClassifier(random_state = 42)
dtr.fit(data_train, target_train)

dtr.score(data_test, target_test)


#%%



#%%



