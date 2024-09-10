from eth_account import Account
from eth_account.messages import defunct_hash_message
from exec.flask_client import FlaskCustomClient
import os
import requests
import logging
import json
from dotenv import load_dotenv
load_dotenv()

flask_client = FlaskCustomClient(host='localhost')

def registerModel(taskInfo):
    logging.info("Registering a new model")
    #Fetching model signedUrl from API
    MAIN_SERVER = os.getenv('MAIN_SERVER')
    model_class = taskInfo['gameClass']
    modelName = taskInfo['modelName']
    model_query_url=f"{MAIN_SERVER}/model/{model_class}"
    response = requests.get(model_query_url)
    data = response.json()
    modelUrl = data.get('url')
    logging.info("Model Download URL Found")
    logging.info(modelName)
    logging.info(modelUrl)
    try:
        response = flask_client.register_a_model(model_name=modelName, model_url=modelUrl)
        logging.info("New Model Registered")
        return True
    except Exception as e:
        logging.info("Model Registeration Failed",e)
        return False