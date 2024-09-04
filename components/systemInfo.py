import logging
import platform
import socket
import psutil
import re
import uuid

def get_ip_address():
    try:
        # Try to get the IP address by creating a socket connection
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        try:
            # If that fails, try to get the IP from the hostname
            return socket.gethostbyname(socket.gethostname())
        except:
            # If all else fails, return localhost
            return '127.0.0.1'

def fetchSystemInfo():
    info = {}
    try:
        info['platform'] = platform.system()
        info['platform-release'] = platform.release()
        info['platform-version'] = platform.version()
        info['architecture'] = platform.machine()
        info['hostname'] = socket.gethostname()
        info['ip-address'] = get_ip_address()
        info['mac-address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor'] = platform.processor()
        info['ram'] = f"{round(psutil.virtual_memory().total / (1024.0 **3))} GB"
        info['physical_cores'] = psutil.cpu_count(logical=False)
        info['logical_cores'] = psutil.cpu_count(logical=True)
        info['cpu_usage'] = psutil.cpu_percent(interval=1)
        return info
    except Exception as e:
        logging.exception(f"An error occurred while fetching system info: {e}")
        return None
