from sklearn.neural_network import MLPClassifier
from persistence_interface import load, save
from flask import Flask
from flask import request
import io
import csv
app = Flask(__name__)

@app.route("/", methods=['POST'])
def train_model(*args):
    file = request.files['training_data']
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)   
    csv_content = csv.reader(stream)
    
    print(csv_content)
    for row in csv_content:
        print(row)
    
    # model = MLPClassifier(args, request.args) # request.args is a dictionary like kwargs
    
    # model.fit(features, labels)
    # save(model)

@app.route("/<model_id>")        
def predict_value(model_id, predictors):
    model = load(model_id)
    prediction = model.predict(predictors)
    return {
        "prediction" : prediction    
    }
    
if __name__ == "__main__":
   app.run(host='0.0.0.0')