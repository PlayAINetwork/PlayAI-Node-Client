from flask import Flask, jsonify
import os
from components.health_check import perform_health_check

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    #return jsonify({'status': 'healthy',}), 200
    health_status = perform_health_check()
    return jsonify(health_status), 200 if health_status['status'] == 'healthy' else 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    app.run(host='0.0.0.0', port=port)