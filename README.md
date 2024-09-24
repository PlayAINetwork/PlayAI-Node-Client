# README

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

## Setup

### Step 1: Install or Clone the Repository

You can either use the installer by running the command below:

curl -sL https://raw.githubusercontent.com/PlayAINetwork/PlayAI-Node-Client/refs/heads/dev/playinstaller.sh -o playinstaller.sh && chmod +x playinstaller.sh && ./playinstaller.sh


Or clone the repository using the following command:


### Step 2: Create Environment Variables

This project requires specific environment variables to be set up. Follow these steps:

1. Create a file named `.env` in the root directory of your project.
2. Add the following content to the `.env.schema` file:

   ```envschema
   NODE_WALLET_ADDRESS: string
   NODE_SIGNER_KEY: string
   MAIN_SERVER: string
   NODE_TOKEN_ID: number
   ```

3. Replace the placeholders with your actual values. For example:

   ```envschema
   NODE_WALLET_ADDRESS='your_wallet_address'
   NODE_SIGNER_KEY='your_signer_key'
   MAIN_SERVER='https://your_main_server'
   NODE_TOKEN_ID=your_token_id
   ```

### Step 2: Docker Compose

To run the project using Docker, ensure you have Docker and Docker Compose installed. Then, use the following command to start the services:


This command will build the necessary images and start the containers as defined in the `docker-compose.yml` file. Make sure to check the `docker-compose.yml` for any additional configuration or services.

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
