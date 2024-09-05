import requests
import os
import logging
from dotenv import load_dotenv
import logging
from components.signer import signResponseObject
from components.systemInfo import fetchSystemInfo
load_dotenv()

def register_node():
    #skipping registration for now
    return True
    '''MAIN_SERVER = os.getenv('MAIN_SERVER')
    api_url = f"{MAIN_SERVER}/register"
    headers = {"Content-Type": "application/json"}
    token_id = os.getenv('NODE_TOKEN_ID')
    ip= os.getenv('IP')
    port = os.getenv('PORT')
    info=fetchSystemInfo()
    params = {
        'NODE_TOKEN_ID':token_id,
        'NODE_IP':ip,
        'NODE_PORT':port,
        "SYSTEM_INFO":info,
    }
    signature = signResponseObject(params)
    params['SIGNATURE']=signature
    #print("Sending Regsitration Info to Server",params)
    try:
            # Make POST request to /register endpoint
            response = requests.post(api_url, json=params, headers=headers)
            # Check if request was successful (status code 200)
            if response.status_code == 200:
                 data = response.json()
                 id = data.get('id')
                 logging.info('Node regsitration successful')
                 logging.info(f"Your unique id is : {id}")
                 return True
            elif response.status_code == 201:
                  logging.info('Node Already Linked & Registered')
                  return True
            else:
                logging.info('Node registration unsuccesful')
                return False
    except requests.exceptions.RequestException as e:
            return {'error': f'Request failed: {str(e)}'}'''

