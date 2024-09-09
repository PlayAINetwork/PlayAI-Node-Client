import json
from exec.flask_client import FlaskCustomClient

if __name__ == '__main__':

    flask_client = FlaskCustomClient(host='localhost')
    print(flask_client.get_list_of_models())

    model_url = "s3://playai-cv-video-filter-prod/model-store/pubg_mvit_v4.mar"
    model_name = 'pubg_mvit_v4'
    model_signed_url = 'https://playai-cv-video-filter-prod.s3.amazonaws.com/model-store/pubg_mvit_v4.mar?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAZQ3DRWKCEAJT7U5P%2F20240909%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20240909T094113Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=a93d4e98156b17039486e18a259dbbd432b27e575ad379ebcd33a0f0c2d50c83'
    #please use updated signed url, above url might have expired"

    try:
        response = flask_client.register_a_model(model_name=model_name, model_url=model_signed_url)
        print(response)
    except Exception as e:
        print(e)
        pass
    print(flask_client.get_list_of_models())



    game_id = '1'
    event_id = '1'
    # url = "s3://playai-cv-video-filter-prod/data/sample_data/gamecls=MINECRAFT/game_id=1/event_id=1.npy"
    # get signed url from above url, below signed_url might have become dead
    signed_url ="https://playai-cv-video-filter-prod.s3.amazonaws.com/data/sample_data/gamecls%3DMINECRAFT/game_id%3D1/event_id%3D1.npy?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAZQ3DRWKCEAJT7U5P%2F20240909%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20240909T095220Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=da68c8f197283d21b527687ca6c304cc539bbf52c58fe8f88a201c785c361066"
    if len(signed_url) == 0:
        raise ValueError('please provide the signed URL of event')
    request_data = dict(
        game_id=game_id,
        event_id=event_id,
        url=signed_url
    )

    # response = flask_client.get_prediction(
    #     data=request_data,
    #     model_name='pubg_mvit_v4'
    # )
    # print(response)

    #Sample request to deregister a models
    response = flask_client.de_register_model(model_name='pubg_mvit_v4')
    print(response)

    print(flask_client.get_list_of_models())