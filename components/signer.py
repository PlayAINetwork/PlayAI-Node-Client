from eth_account import Account
from eth_account.messages import encode_defunct
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the node signer key from environment variables
NODE_SIGNER_KEY = os.getenv('NODE_SIGNER_KEY')

def signResponseObject(response_json):
    """
    Sign a JSON object (dictionary) by converting it to a sorted JSON string and then signing it.

    Args:
        response_json (dict): The JSON object to be signed.

    Returns:
        str: The hexadecimal representation of the signature.

    Raises:
        ValueError: If the input is not a dictionary.
    """
    # Check if the input is a dictionary
    if not isinstance(response_json, dict):
        raise ValueError("Input must be a dictionary (JSON object)")
    
    # Convert the dictionary to a JSON string with sorted keys
    json_string = json.dumps(response_json, sort_keys=True)
    
    # Sign the JSON string
    return signResponse(json_string)

def signResponse(message):
    """
    Sign a message using the node's private key.

    Args:
        message (str): The message to be signed.

    Returns:
        str: The hexadecimal representation of the signature.

    Raises:
        ValueError: If the input is not a string.
    """
    # Check if the input is a string
    if not isinstance(message, str):
        raise ValueError("Input must be a string")
    
    # Encode the message in the format expected by Ethereum
    encoded_message = encode_defunct(text=message)
    
    # Sign the encoded message using the node's private key
    signed_message = Account.sign_message(encoded_message, NODE_SIGNER_KEY)
    
    # Return the signature as a hexadecimal string
    return signed_message.signature.hex()