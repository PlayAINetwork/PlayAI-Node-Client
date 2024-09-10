from eth_account import Account
from eth_account.messages import encode_defunct
import os
import json
from dotenv import load_dotenv

load_dotenv()

NODE_SIGNER_KEY = os.getenv('NODE_SIGNER_KEY')

def signResponseObject(response_json):
    if not isinstance(response_json, dict):
        raise ValueError("Input must be a dictionary (JSON object)")
    
    json_string = json.dumps(response_json, sort_keys=True)
    return signResponse(json_string)

def signResponse(message):
    if not isinstance(message, str):
        raise ValueError("Input must be a string")
    
    encoded_message = encode_defunct(text=message)
    signed_message = Account.sign_message(encoded_message, NODE_SIGNER_KEY)
    return signed_message.signature.hex()