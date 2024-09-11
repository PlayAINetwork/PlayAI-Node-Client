import os
import logging
import requests
from dotenv import load_dotenv
from flask import jsonify
from components.signer import signResponseObject
from components.register_model import register_model
from exec.flask_client import FlaskCustomClient
from exec.inference import fetchModelResponse

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask client
flask_client = FlaskCustomClient(host='localhost')

# Environment variables
MAIN_SERVER = os.getenv('MAIN_SERVER')
NODE_TOKEN_ID = os.getenv('NODE_TOKEN_ID')

def executeCompute(taskInfo):
    """
    Execute the computation task and submit results to the main server.
    """
    logging.info("Executing Compute on Task")
    model_class = taskInfo['gameClass']
    
    # Ensure model is registered
    if not checkModelPresence(model_class):
        register_model(taskInfo)
        if not checkModelPresence(model_class):
            logging.error(f"Failed to register model: {model_class}")
            return jsonify({'error': 'Model registration failed'}), 500

    # Fetch model response
    computeResponse = fetchModelResponse(taskInfo)
    logging.info("Compute Response: %s", computeResponse)

    if not computeResponse['isSuccess']:
        logging.error("Compute failed")
        return jsonify({'error': 'Computation failed'}), 500

    # Sign the response
    computeSignedResponse = signResponseObject(computeResponse)
    if not computeSignedResponse:
        logging.error("Signature process failed")
        return jsonify({'error': 'Signature process failed'}), 500

    # Prepare parameters for submission
    params = {
        "data": {
            "tokenId": int(NODE_TOKEN_ID),
            "taskId": taskInfo['taskId'],
            "inference": computeResponse,
        },
        "signature": computeSignedResponse
    }

    # Submit task to backend
    return submitTaskToBackend(params)

def checkModelPresence(model_class):
    """
    Check if the required model is present in the list of available models.
    """
    response = flask_client.get_list_of_models()
    logging.info("List of Models: %s", response)
    
    if 'models' in response:
        return any(model.get('modelName') == model_class for model in response['models'])
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
        if response.status_code == 200:
            return response.json()
        else:
            logging.error("Request failed with status code %d", response.status_code)
            return {'error': f'Request failed with status code {response.status_code}'}
    except requests.exceptions.RequestException as e:
        logging.error("Request failed: %s", str(e))
        return {'error': f'Request failed: {str(e)}'}