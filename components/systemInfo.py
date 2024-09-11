import logging
import platform
import socket
import psutil
import re
import uuid

def fetchSystemInfo():
    info = {}
    try:
        info['platform'] = platform.system()
        info['platform-release'] = platform.release()
        info['platform-version'] = platform.version()
        info['architecture'] = platform.machine()
        info['processor'] = platform.processor()
        info['ram'] = f"{round(psutil.virtual_memory().total / (1024.0 **3))} GB"
        info['physical_cores'] = psutil.cpu_count(logical=False)
        info['logical_cores'] = psutil.cpu_count(logical=True)
        return info
    except Exception as e:
        logging.exception(f"An error occurred while fetching system info: {e}")
        return None
