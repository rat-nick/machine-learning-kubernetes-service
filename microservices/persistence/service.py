import pickledb
import uuid
from flask import Flask
from flask import request


app = Flask(__name__)

db = pickledb.load("models.db", False)

@app.route("/", methods=['POST'])
def save():
    key = str(uuid.uuid1())
    print(request.form)
    model = request.form['model']
    accuracy = request.form['accuracy']
    auc = request.form['auc']
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

@app.route("/models", methods=['GET'])
def load_all():
    
    res = []
    for key in db.getall():
        res.append(dict(key=key, data=db.get(key)))
    
    return {
        'models': res
    }

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)