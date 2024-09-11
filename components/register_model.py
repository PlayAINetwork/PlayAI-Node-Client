from eth_account import Account
from eth_account.messages import defunct_hash_message
from exec.flask_client import FlaskCustomClient
from exec.torchserve_model_client import TorchserveModelclient
import os
import requests
import logging
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Initialize clients
TORCHSERVE_CLIENT = TorchserveModelclient(host='torchserve')

# Get main server URL from environment variables
MAIN_SERVER = os.getenv('MAIN_SERVER')


def register_model(task_info):
    """
    Register a new model based on the task information.

    Args:
        task_info (dict): A dictionary containing task information including 'gameClass' and 'modelName'.

    Returns:
        bool: True if registration is successful, False otherwise.
    """
    logging.info("Registering a new model")

    model_class = task_info['gameClass']
    model_name = task_info['modelName']

    # Construct URL for model query
    model_query_url = f"{MAIN_SERVER}/model/{model_class}"

    try:
        # Fetch model URL from API
        response = requests.get(model_query_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        model_url = data.get('url')

        if not model_url:
            logging.error("Model URL not found in response")
            return False

        logging.info(f"Model Download URL Found: {model_url}")
        logging.info(f"Model Name: {model_name}")
        logging.info(f"Current models: {TORCHSERVE_CLIENT.get_list_of_models()}")

        # Register the model

        response = TORCHSERVE_CLIENT.register_a_model(model_name=model_name, model_url=model_url)
        print(response)
        logging.info(f"New Model Registered Successfully  {response}")
        return True

    except requests.RequestException as e:
        logging.error(f"Error fetching model URL: {str(e)}")
        return False
    except Exception as e:
        logging.error(f"Model Registration Failed: {str(e)}")
        return False
