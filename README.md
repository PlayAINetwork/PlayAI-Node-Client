# README Update

This repository is responsible for the client that fetches two public images from ECR and runs the containers.

## Services

- **playnode**: 
  - Fetches the Flask application image and runs the client.
  
- **torchserve**: 
  - Fetches the AI engine image for inference.

## Usage

1. Ensure you have Docker and Docker Compose installed.
2. Run the following command to start the services:
   ```bash
   docker-compose up
   ```
3. The `playnode` service will be accessible at `http://localhost:3000`.
4. The `torchserve` service will be accessible at `http://localhost:8080` and `http://localhost:8181`.

Make sure to configure the environment variables as needed for your setup.