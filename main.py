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