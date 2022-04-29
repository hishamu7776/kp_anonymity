import os
import random

import numpy as np
import pandas as pd
import utility as Utility
import top_down as TopDown
from node import Node



k_val = 5
p_val = 2
max_level = 5
paa_val = 8

logger = Utility.create_logging(path='')
path = 'dataset/Sales_Transactions_Dataset_Weekly.csv'
Utility.clean_data(path=path,final_column='W51')
dataset = pd.read_csv("dataset/Sales_Transactions_Dataset_Weekly_Cleaned.csv")
QI_names = dataset.columns[1:]
id_col = dataset.columns[0]
min_attr,max_attr = Utility.get_min_max_attributes(dataset)
data_dict = dict()
for idx, row in dataset.iterrows():
  data_dict[row[id_col]] = list(row[QI_names])
duplicate = data_dict.copy()
k_anonymized_data = list()
TopDown.topdown_greedy(data=duplicate, k_val=5, max_val=max_attr, min_val=min_attr, k_anonymized=k_anonymized_data,columns=QI_names)
anonymized_groups = list()
pattern_anonymized = list()
kp_anonymized = dict()

for group in k_anonymized_data:
  anonymized_groups.append(group)
  good_leaves = list()
  bad_leaves = list()
  node = Node(level=1, group=group, paa_value=paa_val)
  node.start_splitting(p_val, max_level, good_leaves, bad_leaves)
  if len(bad_leaves) > 0:
    Utility.postprocessing(good_leaves, bad_leaves)
  pattern_anonymized.append(good_leaves)
Utility.compute_anonymized_data(k_anonymized=anonymized_groups,p_anonymized=pattern_anonymized,kp_anonymized=kp_anonymized)
Utility.save_anonymized('output.csv',kp_anonymized)