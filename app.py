import json
import requests
from flask import Flask, jsonify, request, Response
import os
from components.health_check import perform_health_check
from exec.torchserve_model_client import TorchserveModelclient
app = Flask(__name__)
TORCHSERVE_CLIENT = TorchserveModelclient(host='torchserve')

@app.route('/health', methods=['GET'])
def health_check():
    health_status = perform_health_check()
    return jsonify(health_status), 200 if health_status['status'] == 'healthy' else 500

@app.route('/register_model', methods = ['POST'])
def register_torchserve_model():
    data = request.get_json()
    response = TORCHSERVE_CLIENT.register_a_model(
        model_url=data['model_url'], #model url should be a signed URL
        model_name=data['model_name']
    )
    return response

@app.route('/predict', methods=['POST'])
def predict_torchserve_model():
    data = request.get_json()
    response = TORCHSERVE_CLIENT.get_prediction(
        data=json.dumps([data['data']]),
        model_name=data['model_name']
    )
    return response


@app.route('/list_models', methods=['GET'])
def list_torchserve_model():
    response = TORCHSERVE_CLIENT.get_list_of_models()
    return response


@app.route('/de_register_model', methods=['POST'])
def de_register_torchserve_model():
    data = request.get_json()
    response = TORCHSERVE_CLIENT.de_register_model(model_name=data['model_name'])
    return response

@app.route('/postprocess', methods=['POST'])
def postprocessing():
    events = request.get_json()
    url = "http://postprocessing:8080/2015-03-31/functions/function/invocations"
    lambda_response = requests.post(url, data=json.dumps(events), headers={"Content-Type": "application/json"})
    flask_response = Response(
        lambda_response.content,
        status=lambda_response.status_code,
        headers=dict(lambda_response.headers)
    )
    return flask_response


if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    app.run(host='0.0.0.0', port=port)