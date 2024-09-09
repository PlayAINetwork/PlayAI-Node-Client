### Model Register/ Deregister/ Prediction requests


### What is there to test in this 
1. Verify that list model api return empty at the launch of service 
2. Verify that list model api does not return empty post registering a model from signed URL 
3. Verify that prediction call to the `model_name` and data is able go get the inference results


### Setup steps 
1. `./exec/flask_client.py` file have class `FlaskCustomClient` that have methods
to register model, list_models, running prediction from different url from flask app 
2. To understand more about how to register a model first launch the container
   - update the docker images by running `docker-compose pull`
   - run the services `docker-compose up --build`
   - go to `.\local\run_flask_client.py` and run different methods of custom_flask_client 
   - make sure to generate new signed_url for the event and model to download same