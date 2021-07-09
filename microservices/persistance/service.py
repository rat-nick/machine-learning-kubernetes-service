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
    db.set(key, model)
    return {
        "key": key,
        "model" : model
    }

@app.route("/<model_id>", methods=['GET'])
def load(model_id):
    
    model = db.get(model_id)
    return {
        "model" : model
    }

if __name__ == "__main__":
   app.run(host='0.0.0.0')