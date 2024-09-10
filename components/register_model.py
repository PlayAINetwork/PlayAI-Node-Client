from eth_account import Account
from eth_account.messages import defunct_hash_message
from exec.flask_client import FlaskCustomClient
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

def registerModel(model_class):
    #Fetching model signedUrl from API
    MAIN_SERVER = os.getenv('MAIN_SERVER')
    model_query_url=f"{MAIN_SERVER}/model/{model_class}"
    response = requests.get(model_query_url)
    data = response.json()
    modelUrl = data.get('downloadurl')
    flask_client = FlaskCustomClient(host='localhost')
    try:
        response = flask_client.register_a_model(model_name=model_class, model_url=modelUrl)
        print(response)
        return True
    except Exception as e:
        print(e)
        return False