import requests

def load(model_id):
    response = requests.get("persistence-service/" + model_id)
    print(response)
    return response['model']

def save(model, accuracy, auc):
    data = {
        "model" : model,
        "accuracy" : accuracy,
        "auc" : auc
    }
    res = requests.post("persistence-service/", data = data)
    return res