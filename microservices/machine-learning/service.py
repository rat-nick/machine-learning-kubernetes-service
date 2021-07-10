from scipy.sparse import data
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from persistence_interface import load, save
from flask import Flask
from flask import request
import io
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=['POST'])
def train_model():
    
    # reading the dataset as a csv file with
    file = request.files['training_data']
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)   
    dataset = pd.read_csv(stream, header=None)
    
    # argument preparation
    args = request.args.to_dict()
    for k, v in args.items():
        try:
            args[k] = float(v) # convert to float if applicable
        except Exception:
            args[k] = v               
    
        try:
            if v.startswith('(') and v.endswith(')'): 
                args[k] = eval(v) # convert to tuple if applicable
        except Exception:
            args[k] = v     

    model = MLPClassifier(**args)
    train, test = feature_label_split(dataset)
    X_train, X_test, y_train, y_test = train_test_split(train, test, test_size=.2, random_state=42)
    model.fit(X_train, y_train)

    
    accuracy = accuracy_score(y_test, model.predict(X_test))
    auc = roc_auc_score(y_test, model.predict(X_test))
    
    
    save(model, accuracy, auc)

def feature_label_split(df):
    return df.iloc[:, :-1], df.iloc[:, -1]
    
    
@app.route("/<model_id>")        
def predict_value(model_id, predictors):
    model = load(model_id)
    prediction = model.predict(predictors)
    return {
        "prediction" : prediction    
    }
    
if __name__ == "__main__":
   app.run(host='0.0.0.0')