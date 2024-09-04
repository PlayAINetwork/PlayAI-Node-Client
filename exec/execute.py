from apscheduler.schedulers.background import BackgroundScheduler
from flask import jsonify
import requests
import os
import logging
from dotenv import load_dotenv
import logging
from components.signer import signResponseObject, signResponse
load_dotenv()

def executeCompute(chunk_ID):
    # Akthar needs to fillup what the chunk info be
    NODE_SIGNER_KEY = os.getenv('NODE_SIGNER_KEY')
    MAIN_SERVER = os.getenv('MAIN_SERVER')
    NODE_WALLET_ADDRESS = os.getenv('NODE_WALLET_ADDRESS')
    api_url = f"{MAIN_SERVER}/chunkInfo/{chunk_ID}"
    headers = {"Content-Type": "application/json"}
    try:
        logging.info("Getting additional chunk info")
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            s3_url = data.get('s3_url')
            if not s3_url:
                logging.error("s3_url not found in API response.")
                return {'error':'s3_url not found in API response.'}
        else:
            logging.error(f"Failed to fetch data from API. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request to API failed: {str(e)}")
    
    #Call Compute AI here
    computeResponse = {"accuracy":99,"isPositive":True}
    computeSignedResponse = signResponseObject(computeResponse)
    params = {
        'chunk_ID':chunk_ID,
        'chunkResponse':computeResponse,
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



