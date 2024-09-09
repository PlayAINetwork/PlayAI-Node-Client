### Model Register/ Deregister/ Prediction requests

1. `./exec/flask_client.py` file have class `FlaskCustomClient` that have methods
to register model, list_models, running prediction from different url from flask app 
2. To understand more about how to register a model first launch the container
   - update the docker images by running `docker-compose pull`
   - run the services `docker-compose up --build`
   - go to `.\local\run_flask_client.py` and run different methods of custom_flask_client 
   - make sure to generate new signed_url for the event and model to download same