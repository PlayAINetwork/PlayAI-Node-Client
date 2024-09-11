from apscheduler.schedulers.background import BackgroundScheduler
from flask import jsonify
import requests
import os
import logging
from dotenv import load_dotenv
import logging
from components.signer import signResponseObject, signResponse
from exec.flask_client import FlaskCustomClient
from exec.torchserve_model_client import TorchserveModelclient
from exec.inference import fetchModelResponse
from components.register_model import registerModel
load_dotenv()

flask_client = FlaskCustomClient(host='localhost')

def executeCompute(taskInfo):
    logging.info("Executing Compute on Task")
    MAIN_SERVER = os.getenv('MAIN_SERVER')
    token_id = os.getenv('NODE_TOKEN_ID')
    model_class = taskInfo['gameClass']
    if not checkModelPresence(model_class):
        registerModel(taskInfo)
    checkModelPresence(model_class)
    computeResponse=fetchModelResponse(taskInfo)
    logging.info("Compute Response")
    logging.info(computeResponse)
    if computeResponse['isSuccess'] == True:
        computeSignedResponse = signResponseObject(computeResponse)
        params = {
            'task':taskInfo['taskId'],
            'taskResponse':computeResponse,
            'tokenId':token_id,
            'signature':computeSignedResponse
        }
        if computeSignedResponse:
            logging.info("Sending verified task to backend")
            url = f"{MAIN_SERVER}/task/submit"
            headers = {"Content-Type": "application/json"}
            try:
                # Make POST request to /confrim endpoint
                response = requests.post(url, json=params, headers=headers)
                # Check if request was successful (status code 200)
                if response.status_code == 200:
                    return response.json()  
                else:
                    return {'error': f'Request failed with status code {response.status_code}'}
            except requests.exceptions.RequestException as e:
                return {'error': f'Request failed: {str(e)}'}
        else:
            return jsonify({'error': 'Signature process failed'}), 500
    

def checkModelPresence(model_class):
    response = flask_client.get_list_of_models()
    logging.info("List of Models")
    logging.info(response)
    if 'models' in response:
        available_models = response['models']
        for model in available_models:
            if model.get('modelName') == model_class:
                logging.info("Model Found skip register")
                return True
    return False




