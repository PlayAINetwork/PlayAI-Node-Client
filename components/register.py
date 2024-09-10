import requests
import os
import logging
from dotenv import load_dotenv
import logging
from components.signer import signResponseObject
from components.systemInfo import fetchSystemInfo
load_dotenv()

def register_node():
    MAIN_SERVER = os.getenv('MAIN_SERVER')
    api_url = f"{MAIN_SERVER}/register"
    headers = {"Content-Type": "application/json"}
    token_id = os.getenv('NODE_TOKEN_ID')
    #info=fetchSystemInfo()
    signature = signResponseObject(params)
    params['SIGNATURE']=signature
    try:
        # Get nonce from the server
        nonce_response = requests.get(api_url)
        if nonce_response.status_code != 200:
            logging.error(f"Failed to get nonce: {nonce_response.status_code}")
            return False
        nonce = nonce_response.json().get('nonce')
        params = {
            'id': token_id,
            "nonce": nonce
        }
        signature = signResponseObject(nonce)
        params['signature'] = signature

        # Make POST request to /register endpoint
        response = requests.post(api_url, json=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            nodehash = data.get('nodehash')
            logging.info('Node registration successful')
            logging.info(f"Your unique id is : {nodehash}")
            return True
        elif response.status_code == 201:
            logging.info('Node Already Linked & Registered')
            return True
        else:
            logging.error(f'Node registration unsuccessful: {response.status_code}')
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f'Request failed: {str(e)}')
        return False

