from eth_account import Account
from eth_account.messages import defunct_hash_message
import os
import json
from dotenv import load_dotenv
load_dotenv()

def signResponseObject(signResponseJSON):
    if not isinstance(signResponseJSON, dict):
            raise ValueError("Input must be a dictionary (JSON object)")
    json_string = json.dumps(signResponseJSON, sort_keys=True)
    NODE_SIGNER_KEY = os.getenv('NODE_SIGNER_KEY')
    msghash = defunct_hash_message(text="\x19Ethereum Signed Message:\n32" + json_string)
    signedMesaage=Account.signHash(msghash,NODE_SIGNER_KEY)
    signature=signedMesaage['signature'].hex()
    return signature

def signResponse(signResponseMessage):
    message=str(signResponseMessage)
    NODE_SIGNER_KEY = os.getenv('NODE_SIGNER_KEY')
    msghash = defunct_hash_message(text="\x19Ethereum Signed Message:\n32" + message)
    signedMesaage=Account.signHash(msghash,NODE_SIGNER_KEY)
    signature=signedMesaage['signature'].hex()
    print(signature)
    return signature