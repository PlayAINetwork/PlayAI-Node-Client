import os
import psutil
import requests
from flask import jsonify
from components.systemInfo import fetchSystemInfo
from dotenv import load_dotenv
load_dotenv()

def perform_health_check():
    health_status = {
        'status': 'healthy',
        'details': {}
    }
    try:
        # Check CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)
        health_status['details']['cpu_usage'] = f"{cpu_usage}%"
        if cpu_usage > 90:
            health_status['status'] = 'unhealthy'

        # Check memory usage
        memory = psutil.virtual_memory()
        health_status['details']['memory_usage'] = f"{memory.percent}%"
        if memory.percent > 90:
            health_status['status'] = 'unhealthy'

        # Check disk usage
        disk = psutil.disk_usage('/')
        health_status['details']['disk_usage'] = f"{disk.percent}%"
        if disk.percent > 90:
            health_status['status'] = 'unhealthy'

        # Check if required environment variables are set
        required_env_vars = ['NODE_WALLET_ADDRESS', 'NODE_SIGNER_KEY', 'MAIN_SERVER', 'NODE_TOKEN_ID']
        missing_env_vars = [var for var in required_env_vars if not os.getenv(var)]
        health_status['details']['missing_env_vars'] = missing_env_vars
        if missing_env_vars:
            health_status['status'] = 'unhealthy'

        # Add system info
        # Hiding System info for now
        '''system_info = fetchSystemInfo()
        if system_info:
            health_status['details']['system_info'] = system_info
        else:
            health_status['status'] = 'unhealthy'
            health_status['details']['system_info'] = 'Failed to fetch system information'''

    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['details']['error'] = str(e)

    return health_status