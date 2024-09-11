import requests
import json
from exec.flask_client import FlaskCustomClient
import logging

flask_client = FlaskCustomClient(host='localhost')

def fetchModelResponse(resData):
    logging.info("Fetching Response from Model")
    model_name = resData['modelName']
    request_data = dict(
        game_id=resData['gameClass'],
        event_id=resData['id'],
        url=resData['data']
    )
    response = flask_client.get_prediction(
         data=request_data,
         model_name=model_name
    )
    logging.info("Model Response")
    logging.info(response)
    return response