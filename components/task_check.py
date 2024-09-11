import os
import requests
from dotenv import load_dotenv
from components.signer import signResponse

# Load environment variables
load_dotenv()

# Constants
MAIN_SERVER = os.getenv('MAIN_SERVER')
TOKEN_ID = int(os.getenv('NODE_TOKEN_ID'))
NONCE_URL = f"{MAIN_SERVER}/nonce"
TASK_CHECK_URL = f"{MAIN_SERVER}/task"

# Configure session for reuse
session = requests.Session()

def get_nonce():
    """
    Fetch nonce from the server.

    Returns:
        str: The nonce received from the server.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    try:
        response = session.get(NONCE_URL, timeout=10)
        response.raise_for_status()
        return response.json()['nonce']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching nonce: {e}")
        raise

def check_task():
    """
    Fetch task from server after signing the nonce.

    Returns:
        dict: The task data received from the server.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    try:
        # Get and sign the nonce
        nonce = get_nonce()
        signed_nonce = signResponse(nonce)

        # Prepare parameters for task check
        params = {
            "tokenId": TOKEN_ID,
            "nonce": nonce,
            "signature": signed_nonce
        }

        # Send request to check task
        response = session.post(TASK_CHECK_URL, json=params, timeout=10)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error checking task: {e}")
        raise