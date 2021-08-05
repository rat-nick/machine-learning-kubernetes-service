import pickle
import requests
import inspect
def load(model_id):
    res = requests.get("http://persistence:5000/" + model_id)
    res.headers["Access-Control-Allow-Origin"] = "*"
    return pickle.loads(res.content)

def load_all():
    res = requests.get("http://persistence:5000/models")
    #print(res)
    res.headers["Access-Control-Allow-Origin"] = "*"
    return res


def save(model, accuracy, auc):
    data = pickle.dumps(model)
    
    params = {
        "modelType": str(model).split('(')[0],
        #"hyperparameters": inspect.getfullargspec(model.__init__),
        "accuracy" : accuracy,
        "auc" : auc
    }
    
    res = requests.post("http://persistence:5000/", data=data, params=params)
    #print(res)
    res.headers["Access-Control-Allow-Origin"] = "*"
    return res