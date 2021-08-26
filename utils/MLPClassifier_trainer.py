from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
import pickle
import pandas as pd
from random import randint

def feature_label_split(df):
    return df.iloc[:, :-1], df.iloc[:, -1]

file = open("data.csv", "r+")
dataset = pd.read_csv(file, header=None)

train, test = feature_label_split(dataset)
X_train, X_test, y_train, y_test = train_test_split(train, test, test_size=.2, random_state=42)

model = MLPClassifier()
model.fit(X_train, y_train)

with open(f"{randint(1000, 9999)}.pkl", 'wb') as f:
    pickle.dump(model, f)
