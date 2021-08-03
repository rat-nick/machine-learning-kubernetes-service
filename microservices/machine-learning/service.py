from flask.json import jsonify
from flask.wrappers import Request
import numpy as np
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.model_selection import train_test_split
from persistence_interface import load, load_all, save
from flask import Flask
from flask import request, Response
import io
import pandas as pd
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)
@app.route("/train/", methods=['POST'])
@cross_origin()
def train_model():
    
    # reading the dataset as a csv file with
    file = request.files['training_data']
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)   
    dataset = pd.read_csv(stream, header=None)
    
    # argument preparation
    print(request.args)
    args = request.args.to_dict()
    
    for k, v in args.items():
        try:
            args[k] = float(v) # convert to float if applicable
        except Exception:
            args[k] = v               
    
        try:
            if v.startswith('(') and v.endswith(')'): 
                print(args[k])
                args[k] = eval(v) # convert to tuple if applicable
        except Exception:
            args[k] = v
    
    model = MLPClassifier(**args)     
    print(model)
    # if args['modelType'] == 'Classifier':
    #     model = MLPClassifier(**args)
    # elif args['modelType'] == 'Regressor':
    #     model = MLPRegressor(**args)
    # else:
    #     return
    train, test = feature_label_split(dataset)
    X_train, X_test, y_train, y_test = train_test_split(train, test, test_size=.2, random_state=42)
    model.fit(X_train, y_train)

    
    accuracy = accuracy_score(y_test, model.predict(X_test))
    auc = roc_auc_score(y_test, model.predict(X_test))
    
    res = save(model, accuracy, auc)
    return Response(res)

def feature_label_split(df):
    return df.iloc[:, :-1], df.iloc[:, -1]

@app.route("/model/", methods=['GET'])
@cross_origin()    
def all_models():
    return Response(load_all())
    
@app.route("/predict/", methods=['GET'])
@cross_origin()        
def predict_value():
    model_id = request.args['modelID']
    model = load(model_id)    
    predictors = request.args['predictors']
    predictors = list(map(float, predictors.split(',')))
    predictors = [np.array(predictors)]
    predictions = model.predict(predictors)
    #print(prediction[0])
    return str(predictions[0])
    
if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True, port=8080)