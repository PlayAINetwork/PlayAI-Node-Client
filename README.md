# README

## Overview

This repository contains a Docker Compose configuration for a client application that interacts with a machine learning inference service. It includes services for the main application, inference, and postprocessing.

## Services

- **Playnode**:
  - PlayaAI node for pulling task and registering node
  - Port: 3000
  - To run service on multinode Node change `HOST_NAME=localhost` 
    without any quotes in `docker-compose.yml` file

- **Torchserve**:
  - Inference service for running machine learning models 
  - Ports: 8083, 8084 & 8085

- **Postprocessing**: 
  - Other ML tasks
  - port: 8080

- More details is there about variable and service in the `docker-compose.yml` file


## Setup

### Step 1: Install or Clone the Repository

You can either use the installer by running the command below:

```
curl -sL https://playinstaller.playai.network -o playinstaller.sh && chmod +x playinstaller.sh && ./playinstaller.sh
 ```


Or clone the repository using the following command:

```
git clone https://github.com/PlayAINetwork/PlayAI-Node-Client.git
 ```

### Step 2: Create Environment Variables

This project requires specific environment variables to be set up. Follow these steps:

1. Create a file named `.env.schema` in the root directory of your project.
2. Add the following content to the `.env.schema` file:

   ```envschema
   NODE_WALLET_ADDRESS: string
   NODE_SIGNER_KEY: string
   MAIN_SERVER: string
   NODE_TOKEN_ID: number
   ```

3. Replace the placeholders with your actual values. For example:

   ```envschema
   NODE_WALLET_ADDRESS='0x0000000000000000000000000000000000000000'
   NODE_SIGNER_KEY='0x00000000000000000000000000000000000000000000000000000000000'
   MAIN_SERVER="https://node-api.playai.network"
   NODE_TOKEN_ID=0
   ```

### Step 2: Docker Compose

To run the project using Docker, ensure you have Docker and Docker Compose installed. Then, use the following command to start the services:


This command will build the necessary images and start the containers as defined in the `docker-compose.yml` file. Make sure to check the `docker-compose.yml` for any additional configuration or services.

## Usage

1. Ensure you have Docker and Docker Compose installed.
2. Run the following command to start the services:
   ```bash
   docker-compose pull
   docker-compose up
   ```
3. Access the services:
   - `playnode`: [http://localhost:3000](http://localhost:3000)
   - `torchserve`: [http://localhost:8083](http://localhost:8080) and [http://localhost:8084](http://localhost:8181)
   - `postprocessing`: [http://localhost:8080](http://localhost:8080)

