from apscheduler.schedulers.background import BackgroundScheduler
import requests
import os
import sys
import logging
from dotenv import load_dotenv
from components.register import register_node
from exec.execute import executeCompute
from exec.inference import fetchModelResponse
from components.check_env import check_env_variables
import threading

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),  # Log to a file
        logging.StreamHandler()          # Log to the console
    ]
)

class ExcludeJobLogFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        return not ("Added job" in msg or "Job " in msg or "Running job" in msg)

# Apply the filter to all handlers
for handler in logging.root.handlers:
    handler.addFilter(ExcludeJobLogFilter())

# Create a lock
execute_lock = threading.Lock()

def pollServer():
    logging.info("Polling Server")
    
    # Try to acquire the lock, but don't block if it's not available
    if not execute_lock.acquire(blocking=False):
        logging.info("Another task is currently being executed. Skipping this poll.")
        return

    try:
        NODE_TOKEN_ID = os.getenv('NODE_TOKEN_ID')
        MAIN_SERVER = os.getenv('MAIN_SERVER')
        api_url = f"{MAIN_SERVER}/tasks/{NODE_TOKEN_ID}"
        headers = {"Content-Type": "application/json"}
        
        logging.info("Calling the backend for active tasks")
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            taskInfo = data.get('task')
            if not taskInfo:
                logging.info("No task assigned at the moment")
                return
            # Execution is invoked here below
            result = executeCompute(taskInfo)
            logging.info(f"Result of the task: {result}")
        else:
            logging.error(f"Failed to fetch data from API. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request to API failed: {str(e)}")
    finally:
        # Always release the lock, even if an exception occurred
        execute_lock.release()

if __name__ == '__main__':
    if not check_env_variables():
        logging.error("Environment variables are not set correctly. Exiting.")
        sys.exit()
    
    if register_node():
        logging.info("Node Registered")
    else:
        exit()
    
    scheduler = BackgroundScheduler(timezone='UTC')
    scheduler.add_job(pollServer, 'interval', minutes=0.5)
    scheduler.start()
    
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        logging.info("Exiting...")
        scheduler.shutdown()