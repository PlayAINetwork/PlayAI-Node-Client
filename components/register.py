import requests
import os
import json
import logging
from dotenv import load_dotenv
import logging
from components.signer import signResponse
from components.systemInfo import fetchSystemInfo
load_dotenv()

MAIN_SERVER = os.getenv('MAIN_SERVER')
TOKEN_ID = os.getenv('NODE_TOKEN_ID')
HEADERS = {"Content-Type": "application/json"}

def get_nonce(url):
    """Fetch nonce from the server."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()['nonce']

def create_registration_params(nonce):
    """Create parameters for registration request."""
    signature = signResponse(nonce)
    params = {
        'tokenId': int(TOKEN_ID),
        'nonce': nonce,
        'signature': signature
    }
    json_compatible_params = json.loads(json.dumps(params))
    # Uncomment the next line if you want to include system info
    # params['systemInfo'] = fetchSystemInfo()
    logging.info(f"Registration params: {params}")
    return json_compatible_params

def register_node():
    """
    Register the node with the main server.

    Returns:
        bool: True if registration is successful, False otherwise.
    """
    nonce_url = f"{MAIN_SERVER}/nonce"
    register_url = f"{MAIN_SERVER}/register"

    try:
        # Get nonce from the server
        nonce = get_nonce(nonce_url)
        
        # Prepare registration parameters
        params = create_registration_params(nonce)
        
        # Make POST request to /register endpoint
        response = requests.post(register_url, json=params, headers=HEADERS)
        
        if response.status_code == 204:
            logging.info('Node registration successful')
            return True
        else:
            logging.error(f'Node registration unsuccessful: {response.status_code}')
            return False

    except requests.RequestException as e:
        logging.error(f'Request failed: {str(e)}')
        return False
    except Exception as e:
        logging.error(f'Unexpected error during registration: {str(e)}')
        return False
    
if __name__ == "__main__":
    register_node()
