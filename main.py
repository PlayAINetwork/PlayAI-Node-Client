
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import os
import sys
import logging
from dotenv import load_dotenv
import logging
from components.register import register_node
from exec.execute import executeCompute
from exec.inference import fetchModelResponse
from components.check_env import check_env_variables
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

def pollServer():
    logging.info("Polling Server")
    NODE_TOKEN_ID = os.getenv('NODE_TOKEN_ID')
    MAIN_SERVER = os.getenv('MAIN_SERVER')
    api_url = f"{MAIN_SERVER}/chunks/{NODE_TOKEN_ID}"
    headers = {"Content-Type": "application/json"}
    '''fetchModelResponse({
    "game_id":"1",
    "event_id":"1",
    "url": "s3://playai-cv-video-filter-prod/data/sample_data/gamecls=MINECRAFT/game_id=1/event_id=1.npy",
    "model_name":"pubg_mvit_v2/2.0"
    })'''
    try:
        logging.info("Calling the backend for active tasks")
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            chunk_ID = data.get('chunk_id')
            if not chunk_ID:
                logging.info("No task assigned at the moment")
                return
            # Execution is invoked here below
            result = executeCompute(chunk_ID)
            logging.info(f"Result of the task: {result}")
        else:
            logging.error(f"Failed to fetch data from API. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request to API failed: {str(e)}")


if __name__ == '__main__':
    if not check_env_variables():
        logging.error("Environment variables are not set correctly. Exiting.")
        sys.exit()
    # Configure the scheduler with a timezone
    if register_node():
            logging.info("Node Registered")
    else:
        exit()
    scheduler = BackgroundScheduler(timezone='UTC')
    # Add a job that calls the external API every minute to get the task
    scheduler.add_job(pollServer, 'interval', minutes=0.5)
   # logging.info('Scheduler started. Press Ctrl+C to exit.')
    scheduler.start()
    # Keep the script running
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        logging.info("Exiting...")