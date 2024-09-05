import requests
import json
import logging
def fetchModelResponse(resData):
    model_name = resData['model_name']
    response = requests.post(f"http://localhost:8080/predictions/{model_name}", data={'data':json.dumps(resData)})
    logging.info("Model Response",response.json())
    #return {"accuracy":99,"isPositive":True}
    return response.json()