import pickle
import re
import uuid
from flask import Flask
from flask import request
from flask import jsonify
import os

app = Flask(__name__)



@app.route("/", methods=['POST'])
def save():
    key = str(uuid.uuid1())
    
    model = request.data
    model_type = request.args['modelType']
    accuracy = request.args['accuracy']
    auc = request.args['auc']
    #hp = request.args['hyperparameters']
    data = (model, model_type, accuracy, auc)

    with open(key+".pkl", 'wb') as f:
        pickle.dump(data, f)
        
    with open(key+".pkl", 'rb') as f:
        model, _, __, ___ = pickle.load(f)
    
    return jsonify({
        "key": key,
        "modelType" : model_type.split('(')[0],
        #'hyperparameters': hp,
        'accuracy': accuracy,
        'auc': auc
    })
    

@app.route("/<model_id>", methods=['GET'])
def load(model_id):
    
    with open(model_id+".pkl", 'rb') as f:
        model, model_type, accuracy, auc = pickle.load(f)

    return model

@app.route("/models", methods=['GET'])
def load_all():
    
    res = []
    for file in os.listdir("./"):
        if file.endswith(".pkl"):
            with open(file, "rb") as f:
                model, model_type, accuracy, auc = pickle.load(f)
                res.append({
                    'key' : file[:-4],
                    #'model' : model,
                    'modelType': model_type,
                    'accuracy' : accuracy,
                    'auc' : auc
                })
                
    return jsonify(res)

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)