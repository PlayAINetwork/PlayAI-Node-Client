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


'''fetchModelResponse({
    "game_id":"1",
    "event_id":"1",
    "url": "https://playai-cv-video-filter-prod.s3.us-east-2.amazonaws.com/data/sample_data/gamecls%3DMINECRAFT/game_id%3D1/event_id%3D1.npy?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPH%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMiJHMEUCIQCKrV1A6wV5H3ukzb%2FxSnOEF8kAEfH48MzogDf4S3SyPwIgL%2FypD1d4Y%2BYTZsAp0V%2FTrPyAm0wUhE0cMdIKyfu8dfQqhQMIGhAAGgw2NTQ2NTQ0MTk1ODgiDHgf3GmmJRX11zOY2iriAh9U7po%2BM4QaCxP6br%2FV74S2MzkPbCfEoKC1SfAjTs%2BETloeTx51umeM3cx9spkpXgw4veqh1MH9Ico0xD9crcriS7TIJ5si7uekbnwwjhftaBjVMky03Ya0TjwD9DV8xqpl%2BSuKd6KvDs5RlQOOTlMnQJ5ml%2Fi45HwlwpRx%2FHEJ9lN9SB%2FCme%2BgcFkuXSqi9ECOOiEGkwYtM04oa3uTSY8J%2BKlTZ8EOmMPJkWwi5DEt5g1xxidmNFNGBopq27hZ%2FzaUcH1ndxdDzlJIE2rgyNt%2FBnmKnOBx4cDjhRXtl0332kzSGbrBlFUS8m11ogkmb5%2BKzas0cCZM4EiTW6SG%2F%2F9M2ly3I2oDiwwBZJW23n4FiBhNWJRl3C6hTQhXDzC4pvfmvCtPvOu5F0SUR3eEt99taEPAL9k6FUTZI2TZC%2B3NQo3eeRvbgDB4XBRNl7qGBgaeWkT0younYHNnuxkIs%2BYNGzCN8%2By2BjqzAtFXmfk%2BXTF1ghT59hBMMRpLPY8j4YppgL22vz3pfl65XXViTCcLuOqkumw4bykh6hfsg5Wdvs9S4hzUxnj5Noaww3elblmcxNP18gLR4yqWipvhFZoJLpcTFwahcTfLX%2FDoJaZTRznnp%2FF1nmUu7K8O0hwDP7DnTtYxHiY6iW6iJjGpKZGTbXTz4%2FuTTkF5yvN7%2FCeoDLC6HwYZeFWC0JoRo6pHm4udGxuxT0pncAYvMjdzwe%2F%2F6my%2B3cx%2FHI5XXI%2BKYn6rr%2BlQJ8qSp4kcwg6OtLni3e%2FpyGZ6CafpXiGfumaMBLkLUs0ogS8PXp%2FdvML9Bix4d08My0cEk%2BMrYP4DXH0a4q20%2ByUvrXESmD%2BpJEQsO2OtfQGYezTYzyrD4ZuTxLW0PyDuOn%2BOg7B%2F7ZSjviU%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240906T174129Z&X-Amz-SignedHeaders=host&X-Amz-Expires=3600&X-Amz-Credential=ASIAZQ3DRWKCCVTL3AAE%2F20240906%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Signature=701eb9a571e989f4fa57a7ec18b995a5e53490ff143d32c164aba804699ac80c",
    "model_name":"pubg_mvit_v3/3.0"
})'''