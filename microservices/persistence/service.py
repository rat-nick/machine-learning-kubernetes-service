import pickledb
import uuid
from flask import Flask
from flask import request
app = Flask(__name__)

db = pickledb.load("models.db", False)

@app.route("/", methods=['POST'])
def save():
    key = str(uuid.uuid1())
    
    model = request.args['model']
    accuracy = request.args['accuracy']
    auc = request.args['auc']
    data = {
        'model': model,
        'accuracy': accuracy,
        'auc' : auc
    }
    db.set(key, data)
    
    return {
        "key": key,
        "data" : data,
    }

@app.route("/<model_id>", methods=['GET'])
def load(model_id):
    
    data = db.get(model_id)
    return {
        "model_id": model_id,
        "data" : data
    }

if __name__ == "__main__":
   app.run(host='0.0.0.0')