import requests
import os
import json
import logging
from dotenv import load_dotenv
import logging
from components.signer import signResponse
from components.systemInfo import fetchSystemInfo

# Load environment variables from .env file
load_dotenv()

# Set up constants from environment variables
MAIN_SERVER = os.getenv('MAIN_SERVER')
TOKEN_ID = os.getenv('NODE_TOKEN_ID')
HEADERS = {"Content-Type": "application/json"}

def get_nonce(url):
    """
    Fetch nonce from the server.
    
    Args:
        url (str): The URL to fetch the nonce from.
    
    Returns:
        str: The nonce received from the server.
    
    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()['nonce']

def create_registration_params(nonce):
    """
    Create parameters for registration request.
    
    Args:
        nonce (str): The nonce received from the server.
    
    Returns:
        dict: The parameters for the registration request.
    """
    # Sign the nonce
    signature = signResponse(nonce)
    
    # Create the parameter dictionary
    params = {
        'tokenId': int(TOKEN_ID),
        'nonce': nonce,
        'signature': signature
    }
    
    # Convert params to JSON-compatible format
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
    # Construct URLs
    nonce_url = f"{MAIN_SERVER}/nonce"
    register_url = f"{MAIN_SERVER}/register"

    try:
        # Get nonce from the server
        nonce = get_nonce(nonce_url)
        
        # Prepare registration parameters
        params = create_registration_params(nonce)
        
        # Make POST request to /register endpoint
        response = requests.post(register_url, json=params, headers=HEADERS)
        
        # Check response status
        if response.status_code == 204:
            logging.info('Node registration successful')
            return True
        else:
            logging.error(f'Node registration unsuccessful: {response.status_code}')
            return False

    except requests.RequestException as e:
        # Handle request-specific exceptions
        logging.error(f'Request failed: {str(e)}')
        return False
    except Exception as e:
        # Handle any other unexpected exceptions
        logging.error(f'Unexpected error during registration: {str(e)}')
        return False
    
# Entry point of the script
if __name__ == "__main__":
    register_node()