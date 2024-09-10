import requests
import json
import logging
def fetchModelResponse(resData):
    model_name = resData['model_name']
    events = [
        {'event_id':resData['event_id'], 'game_id':resData['game_id'],'url':resData['url']}
    ]
    response = requests.post(f"http://localhost:8080/predictions/{model_name}", data={'data':json.dumps(events)})
    print(response.json())
    logging.info("Model Response",response)
    return response.json()