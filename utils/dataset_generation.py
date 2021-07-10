from pandas.core.frame import DataFrame
from sklearn.datasets import make_blobs, make_classification
import numpy as np
import csv

X, y = make_classification(1000)

data = [tuple(x) + (y,) for x, y in zip(X,y)]

with open('data.csv', 'w') as f:
    writer = csv.writer(f , lineterminator='\n')
    for tup in data:
        writer.writerow(tup)

# print(X)
# print(y)
# df = DataFrame(dict(x=X, y=y, label=y))
# print(df)
