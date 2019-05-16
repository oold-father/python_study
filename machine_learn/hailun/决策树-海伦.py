
#%%
import pandas as pd
features=['km','game','ice','label']
dc_hailun = pd.read_csv('hailun.csv')
#dc_hailun.head(10)


#%%
from sklearn import tree
from sklearn.model_selection import train_test_split
data_train, data_test, target_train, target_test =     train_test_split(dc_hailun[features[:3]], dc_hailun[features[3]], test_size = 0.1,random_state = 42)
dtr = tree.DecisionTreeClassifier(max_depth = 3,random_state = 42)

dtr.fit(data_train, target_train)
dtr.score(data_test, target_test)


#%%
dot_data =     tree.export_graphviz(
        dtr,
        out_file = None,
        feature_names = features[:3],
        filled = True,
        impurity = False,
        rounded = True
    )
import pydotplus
graph = pydotplus.graph_from_dot_data(dot_data)


#%%
from IPython.display import Image
Image(graph.create_png())
graph.write_png("hailun.png")


#%%



#%%



