import requests
import json
def fetchModelResponse(resData):
    modelname=resData['modelname']
    data = json.dumps(resData)
    res = requests.post(f"http://localhost:8000/check_data",  data={'data':data})#{'data':"s3://playai-cv-video-filter/inference/data/dummy_data/videoplayback (2)_chunk_output_003.pt"})
    print(res.json())
    return {"accuracy":99,"isPositive":True}
    #return res.json()