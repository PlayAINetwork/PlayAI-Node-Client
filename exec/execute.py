import os
import logging
import requests
import json
from dotenv import load_dotenv
from flask import jsonify
from components.signer import signResponse 
from components.register_model import register_model
from exec.flask_client import FlaskCustomClient
from exec.inference import fetchModelResponse
from app import TORCHSERVE_CLIENT

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Environment variables
MAIN_SERVER = os.getenv('MAIN_SERVER')
NODE_TOKEN_ID = os.getenv('NODE_TOKEN_ID')

def executeCompute(taskInfo):
    """
    Execute the computation task and submit results to the main server.
    """
    logging.info("Executing Compute on Task")
    model_class = taskInfo['gameClass']
    modelName = taskInfo['modelName']
    
    # Ensure model is registered
    if not checkModelPresence(modelName):
        register_model(taskInfo)
        if not checkModelPresence(modelName):
            logging.error(f"Failed to register model: {model_class}")
            return jsonify({'error': 'Model registration failed'}), 500

    # Fetch model response
    computeResponse = fetchModelResponse(taskInfo)
    logging.info("Compute Response: %s", computeResponse)

    if not computeResponse['IsSuccess']:
        logging.error("Compute failed")
        return jsonify({'error': 'Computation failed'}), 500
    
    # Prepare data for signing
    data = {
        "data": {
            "tokenId": int(NODE_TOKEN_ID),
            "taskId": taskInfo['id'],
            "inference": computeResponse,
        }
    }
    # Convert data to a JSON string
    data_string = json.dumps(data['data'], separators=(',', ':'))

    # Sign the response
    signature = signResponse(data_string)
    if not signature:
        logging.error("Signature process failed")
        return jsonify({'error': 'Signature process failed'}), 500

    # Prepare parameters for submission
    params = {
        **data,
        "signature": signature
    }
    
    logging.info("Submitting Response to Backend %s", params)
    # Submit task to backend
    return submitTaskToBackend(params)

def checkModelPresence(model_class):
    """
    Check if the required model is present in the list of available models.
    """
    response = TORCHSERVE_CLIENT.get_list_of_models()
    logging.info("List of Models: %s", response)
    
    if 'models' in response:
        return any(model_class in model.get('modelName', '') for model in response['models'])
    return False

def submitTaskToBackend(params):
    """
    Submit the task results to the backend server.
    """
    logging.info("Sending verified task to backend")
    url = f"{MAIN_SERVER}/task/submit"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=params, headers=headers)
        if response.status_code == 204:
            return True
        else:
            logging.error("Request failed with status code %d", response.status_code)
            return {'error': f'Request failed with status code {response.status_code}'}
    except requests.exceptions.RequestException as e:
        logging.error("Request failed: %s", str(e))
        return {'error': f'Request failed: {str(e)}'}