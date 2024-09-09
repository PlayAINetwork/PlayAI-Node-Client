import json
import requests


class TorchserveModelclient:
    def __init__(self, host='torchserve'):
        # self.model_name = model_name
        # self.version = version
        self.host = host
        self.status_url = f"http://{host}:8080/ping"
        self.list_model_url = f"http://{host}:8081/models"
        self.management_api_url = f'http://{host}:8081'

    def get_prediction_api_url(self,model_name):
        prediction_url = f"http://{self.host}:8080/predictions/{model_name}"
        return prediction_url

    def register_a_model(self, model_name,model_url):
        # if model_url.startswith('s3://'):
        #     model_url = self.get_signed_url(model_url)
        if not model_url.startswith('https://'):
            raise ValueError(f'please provide the valid signed model URL, current URL {model_url}')
        url = f"{self.management_api_url}/models"
        data = {
            "model_name": model_name,
            "url": model_url,
            "initial_workers": 1,
            "synchronous": "true"
        }
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response.json()

    def get_prediction(self, data, model_name):
        response = requests.post(
            self.get_prediction_api_url(model_name=model_name),
            data={'data': data}
        )
        return response.json()

    def get_status(self):
        response = requests.get(self.status_url)
        return response.json()

    def get_list_of_models(self):
        response = requests.get(self.list_model_url)
        return response.json()

    # @staticmethod
    # def get_signed_url(url):
    #     io_strategy = S3Strategy(location=url)
    #     return io_strategy.get_signed_url(url)

    def de_register_model(self, model_name):
        url = f"{self.management_api_url}/models/{model_name}"
        # headers = {"Content-Type": "application/json"}

        response = requests.delete(url)
        return response.json()


