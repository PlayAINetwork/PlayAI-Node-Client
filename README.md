# README Update

## Overview

This repository contains a Docker Compose configuration for a client application that interacts with a machine learning inference service. It includes services for the main application, inference, and postprocessing.

## Services

- **playnode**: 
  - Image: `public.ecr.aws/j7l3n4i5/client/flask-app:latest`
  - Container Name: `playnode`
  - Ports: `3000:3000`
  - Environment Variables:
    - `FLASK_APP=app.py`
    - `TORCHSERVE_URL=http://torchserve:8080`
    - `NODE_WALLET_ADDRESS='0xC29657430Dd4a78ef0AA52Ba6D6FAB63b17fB55A'`
    - `NODE_SIGNER_KEY='0x74faa7eea8d93f94e932ba7058df5bc4c3eca518c77f80413d28af5dbbdebc24'`
    - `MAIN_SERVER="https://node-dev.up.railway.app"`
    - `NODE_TOKEN_ID=2`
  - Command: `"/app/start.sh"`
  - Depends on: `torchserve`

- **torchserve**: 
  - Image: `public.ecr.aws/j7l3n4i5/playai-node-ai-engine-public-test:inference-latest`
  - Container Name: `torchserve`
  - Ports: `8080:8080`, `8181:8181`

- **postprocessing**: 
  - Image: `public.ecr.aws/j7l3n4i5/playai-node-ai-engine-public-test:postprocessing-latest`
  - Container Name: `postprocessing`
  - Command: `"postprocess_lambda_function.lambda_handler"`
  - Networks: `internal_net`
  - Expose: `8080`

## Usage

1. Ensure you have Docker and Docker Compose installed.
2. Run the following command to start the services:
   ```bash
   docker-compose up
   ```
3. Access the services:
   - `playnode`: [http://localhost:3000](http://localhost:3000)
   - `torchserve`: [http://localhost:8080](http://localhost:8080) and [http://localhost:8181](http://localhost:8181)

## Notes

- The `postprocessing` service is currently set to expose port `8080` but does not publish it to the host. Adjust as necessary for your use case.
- Uncomment the environment variables and volumes in the `torchserve` service if needed for your model configuration.