import requests


class FlaskCustomClient:
    def __init__(self, host='torchserve'):
        # self.model_name = model_name
        # self.version = version
        self.host = host
        self.status_url = f"http://{host}:3000/list"
        self.list_model_url = f"http://{host}:3000/list_models"
        self.model_register_api = f"http://{host}:3000/register_model"
        self.deregister_model_url = f"http://{host}:3000/de_register_model"
        self.management_api_url = f'http://{host}:8081'

    def get_prediction_api_url(self):
        prediction_url = f"http://{self.host}:3000/predict"
        return prediction_url

    def register_a_model(self, model_name, model_url):
        # if model_url.startswith('s3://'):
        #     model_url = self.get_signed_url(model_url)
        if not model_url.startswith('https://'):
            raise ValueError(f'please provide the valid signed model URL, current URL {model_url}')
        url = f"{self.management_api_url}/models"
        data = {
            "model_name": model_name,
            "model_url": model_url,
            "initial_workers": 1,
            "synchronous": "true"
        }
        headers = {"Content-Type": "application/json"}

        response = requests.post(self.model_register_api, json=data, headers=headers)
        return response

    def get_prediction(self, data, model_name):
        response = requests.post(
            self.get_prediction_api_url(),
            json={'data': data, 'model_name':model_name}
        )
        return response.json()

    def get_status(self):
        response = requests.get(self.status_url)
        return response.json()

    def get_list_of_models(self):
        response = requests.get(self.list_model_url)
        return response.json()

    def de_register_model(self, model_name):
        # headers = {"Content-Type": "application/json"}
        response = requests.post(self.deregister_model_url, json= {'model_name':model_name})
        return response.json()