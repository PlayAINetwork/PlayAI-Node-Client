# PlayNode AI Application

This project combines a Flask-based web application (PlayNode) with a TorchServe instance for AI model inference, designed for processing and analyzing PUBG game data.

## Project Structure

- `app.py`: Main Flask application serving the web interface and API endpoints
- `Dockerfile`: Defines the PlayNode container environment
- `docker-compose.yaml`: Orchestrates PlayNode and TorchServe services
- `requirements.txt`: Python dependencies for PlayNode
- `start.sh`: Startup script for the PlayNode container
- `model_store/`: Directory containing AI models for TorchServe
- `components/`: Directory containing modular components of the application
  - `systemInfo.py`: Module for fetching system information

## Detailed Component Overview

### PlayNode (Flask Application)

The PlayNode application is built with Flask and serves as the main interface for users. It handles:
- Web interface rendering
- API endpoints for data processing
- Communication with TorchServe for model inference
- System information retrieval

Key features:
- RESTful API design
- Integration with TorchServe
- Dynamic system information display

### TorchServe

TorchServe is used for serving the AI model (`pubg_mvit_v3.mar`). It provides:
- High-performance model inference
- Model management API
- Scalable architecture for handling multiple models

### Docker Configuration

The application is containerized using Docker for easy deployment and scaling:
- `Dockerfile`: Builds the PlayNode environment
  - Based on Python 3.9-slim
  - Installs necessary system dependencies and Python packages
  - Sets up the application directory and entry point
- `docker-compose.yaml`: Defines and links the PlayNode and TorchServe services
  - Manages port mappings
  - Sets environment variables
  - Handles volume mounting for the model store

## Prerequisites

- Docker (version 19.03.0+)
- Docker Compose (version 1.27.0+)
- At least 4GB of RAM available for Docker

## Detailed Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <project-directory>
   ```

2. Prepare the AI model:
   - Ensure you have the `pubg_mvit_v3.mar` file
   - Place it in the `model_store/` directory

3. Configure environment variables (optional):
   - Create a `.env` file in the project root
   - Add any necessary environment variables, e.g.:
     ```
     FLASK_ENV=production
     DEBUG=False
     ```

4. Build and start the services:
   ```
   docker-compose up --build
   ```

5. Verify the services are running:
   - PlayNode: http://localhost:3000
   - TorchServe Inference API: http://localhost:8080
   - TorchServe Management API: http://localhost:8181

## Advanced Usage

### Scaling the Application

To scale the PlayNode service:


### Updating the AI Model

1. Place the new model file in the `model_store/` directory
2. Update the `MODEL_NAME` environment variable in `docker-compose.yaml`
3. Restart the services:
   ```
   docker-compose down
   docker-compose up --build
   ```

### Customizing TorchServe Configuration

1. Create a `config.properties` file with your TorchServe configurations
2. Add a volume mount in `docker-compose.yaml` for TorchServe:
   ```yaml
   volumes:
     - ./config.properties:/home/model-server/config.properties
   ```

## Troubleshooting

- **Issue**: Services fail to start
  **Solution**: Check Docker logs, ensure all ports are available, and verify system resources

- **Issue**: Model inference errors
  **Solution**: Confirm the model file is correctly placed and named in the `model_store/` directory

- **Issue**: High latency in API responses
  **Solution**: Consider scaling the PlayNode service or optimizing the AI model

## Performance Considerations

- The application is designed to run on systems with at least 4GB of RAM
- CPU usage may vary based on the complexity of the AI model and request volume
- Consider monitoring system resources and scaling horizontally for high-traffic scenarios

## Security Notes

- The application uses HTTP by default. For production, configure HTTPS
- Implement proper authentication and authorization mechanisms for API endpoints
- Regularly update dependencies to patch any security vulnerabilities

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

[Specify your license here]

For more detailed information about each component, refer to the comments in the respective files.