from exec.flask_client import FlaskCustomClient

if __name__ == '__main__':
    flask_client = FlaskCustomClient(host='localhost')

    events = [
        {
        "game_id": "1",
        "event_id": "1",
        "video_class": "OTHER",
        "video_type": "LIVE",
        "class_probability": 1.0,
        "video_type_probability": 1.0,
        "IsSuccess": True,
        "downloaded_successfully": True,
        "loaded_successfully": True,
        "error_msgs": []
    },
        {
            "game_id": "1",
            "event_id": "1",
            "video_class": "OTHER",
            "video_type": "LIVE",
            "class_probability": 1.0,
            "video_type_probability": 1.0,
            "IsSuccess": True,
            "downloaded_successfully": True,
            "loaded_successfully": True,
            "error_msgs": []
        },
    ]

    event = {
        "Items": [
            {
                "GameId": 1,
                "events": events
                # "GameCls": "MINECRAFT",
                # 'BasePath': base_path
            },
        ],
        "BatchInput": {
            "postprocess_config": {
                "io_strategy": 'local',
                "output_path": f"s3://some-bucket/some-url/postprocess",
            }
        },
    }

    response = flask_client.postprocess(data=event)
    print(response.text)