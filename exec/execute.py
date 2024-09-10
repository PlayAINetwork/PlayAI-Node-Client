from apscheduler.schedulers.background import BackgroundScheduler
from flask import jsonify
import requests
import os
import logging
from dotenv import load_dotenv
import logging
from components.signer import signResponseObject, signResponse
from exec.flask_client import FlaskCustomClient
from exec.inference import fetchModelResponse
from components.register_model import registerModel
load_dotenv()

def executeCompute(taskInfo):
    MAIN_SERVER = os.getenv('MAIN_SERVER')
    token_id = os.getenv('NODE_TOKEN_ID')
    model_class = taskInfo['class']
    if not checkModelPresence(model_class):
        registerModel(model_class)
    computeResponse=fetchModelResponse(taskInfo['data'])
    computeSignedResponse = signResponseObject(computeResponse)
    params = {
        'task':taskInfo['id'],
        'taskResponse':computeResponse,
        'tokenId':token_id,
        'signature':computeSignedResponse
    }
    # if the process was completed, calling the /confrim endpoint in the main function to confrim the task
    if computeSignedResponse:
        logging.info("Sending verified task to backend")
        url = f"{MAIN_SERVER}/confirm"
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
    flask_client = FlaskCustomClient(host='localhost')
    availableModels = flask_client.get_list_of_models()
    logging.info("Available Models",availableModels)
    if model_class in availableModels:
        return True




