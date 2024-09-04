import os
from dotenv import load_dotenv
import sys
load_dotenv()

def check_env_variables():
    # List of required environment variables
    required_vars = [
        'NODE_WALLET_ADDRESS',
        'NODE_SIGNER_KEY',
        'MAIN_SERVER',
        'NODE_TOKEN_ID',
        'IP',
        'PORT'
    ]

    missing_vars = []

    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print("Error: The following required environment variables are missing:")
        for var in missing_vars:
            print(f"- {var}")
        print("Please set these environment variables before running the application.")
        return False
    else:
        print("All required environment variables are set.")
        return True

if __name__ == "__main__":
    check_env_variables()