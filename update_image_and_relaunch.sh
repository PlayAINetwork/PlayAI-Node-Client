echo "Shutting down services"
docker-compose down
echo "Pulling latest containers"
docker-compose pull
echo "Building and starting services"
docker-compose up --build