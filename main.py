from apscheduler.schedulers.background import BackgroundScheduler
import requests
import os
import sys
import logging
import time
from dotenv import load_dotenv
from components.register import register_node
from exec.execute import executeCompute
from components.task_check import check_task
from components.check_env import check_env_variables
import threading
from queue import Queue

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

# Create a queue to hold tasks
task_queue = Queue()

# Flag to indicate if a task is currently being processed
is_processing = False

def process_task():
    global is_processing
    while True:
        task = task_queue.get()
        is_processing = True
        try:
            result = executeCompute(task)
            logging.info(f"Result of the task: {result}")
        except Exception as e:
            logging.error(f"Error processing task: {str(e)}")
        finally:
            is_processing = False
            task_queue.task_done()

# Start the task processing thread
threading.Thread(target=process_task, daemon=True).start()

def pollServer():
    logging.info("Polling Server")
    
    if is_processing or not task_queue.empty():
        logging.info("A task is currently being processed or queued. Skipping this poll.")
        return
    
    try:
        '''executeCompute({"taskId": "56c3643b-cfce-411d-8524-c71359f59658",
            "data": "https://playai-events-dev.s3.us-east-1.amazonaws.com/preprocess/gamecls%3DPUBG/game_id%3D60861996-6296-4323-9c0c-63ac26d09442/event_id%3D12.npy?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAZQ3DRWKCDZY6SQNH%2F20240910%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240910T143348Z&X-Amz-Expires=604800&X-Amz-Signature=b0fb0b7bfe9e7235e3f65f1f13b6714c3558ef3a155417871559573a22bafebc&X-Amz-SignedHeaders=host&x-id=GetObject",
            "gameClass": "PUBG",
            "modelName": "pubg_mvit_v4"
        })'''
        taskdata = check_task()
        logging.info(taskdata)
        if taskdata['task'] == 'null':
            logging.info("No Task Assigned")
            return
        logging.info("Task Recieved")
        logging.info(taskdata['task'])
        task_queue.put(taskdata['task'])
        logging.info("Task added to the queue")

    except requests.exceptions.RequestException as e:
        logging.error(f"Task Query Failed {str(e)}")

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