import requests

def load(model_id):
    res = requests.get("http://persistence:5000/" + model_id)
    #print(res)
    return res.content

def load_all():
    res = requests.get("http://persistence:5000/models")
    #print(res)
    return res.content


def save(model, accuracy, auc):
    data = {
        "model" : model,
        "accuracy" : accuracy,
        "auc" : auc
    }
    res = requests.post("http://persistence:5000/", data=data)
    #print(res)
    return res.content