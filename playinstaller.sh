#!/bin/bash

# Function to run commands with sudo
sudo_run() {
    sudo "$@"
}

# Display ASCII art and welcome message
sudo_run bash << EOF
cat << "EOT"
 _____  _              ___    _ 
|  __ \| |            / _ \  (_)
| |__) | | __ _ _   _/ /_\ \  _ 
|  ___/| |/ _\` | | | |  _  | | |
| |    | | (_| | |_| | | | | | |
|_|    |_|\__,_|\__, \_| |_/ |_|
                 __/ |         
                |___/          
    _   _           _        _____ _ _            _   
   | \ | |         | |      / ____| (_)          | |  
   |  \| | ___   __| | ___ | |    | |_  ___ _ __ | |_ 
   | . \` |/ _ \ / _\` |/ _ \| |    | | |/ _ \ '_ \| __|
   | |\  | (_) | (_| |  __/| |____| | |  __/ | | | |_ 
   |_| \_|\___/ \__,_|\___| \_____|_|_|\___|_| |_|\__|
                                                      
EOT

echo "Welcome to the PlayAI Node Client Setup Script"
echo "----------------------------------------------"
EOF

# Prompt for setup confirmation
read -p "Do you want to set up the PlayAI Node Client? (y/Y to continue): " answer
if [[ "$answer" != "y" && "$answer" != "Y" ]]; then
    echo "Setup cancelled."
    exit 1
fi

# Install Docker
echo "Installing Docker..."
sudo_run curl -fsSL https://get.docker.com -o get-docker.sh
sudo_run sh get-docker.sh
sudo_run rm get-docker.sh

# Install Docker Compose
echo "Installing Docker Compose 2.17.2..."
sudo_run curl -SL https://github.com/docker/compose/releases/download/v2.17.2/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
sudo_run chmod +x /usr/local/bin/docker-compose

# Verify Docker Compose version
COMPOSE_VERSION=$(docker-compose version --short)
if [ "$(printf '%s\n' "2.17.2" "$COMPOSE_VERSION" | sort -V | head -n1)" != "2.17.2" ]; then
    echo "Error: Docker Compose version 2.17.2 or higher is required. Current version: $COMPOSE_VERSION"
    exit 1
fi

# Install additional dependencies
echo "Installing additional dependencies..."
sudo_run apt-get update && sudo_run apt-get install -y git

# Clone the repository
echo "Cloning the PlayAI-Node-Client repository..."
sudo_run git clone https://github.com/PlayAINetwork/PlayAI-Node-Client.git
cd PlayAI-Node-Client

# Create .env file
echo "Setting up .env file..."
read -p "Enter WALLET address: " WALLET
read -p "Enter USER_PRIVATE_KEY: " USER_PRIVATE_KEY
read -p "Enter MAIN_SERVER URL: " MAIN_SERVER
read -p "Enter NODE_TOKEN_ID: " NODE_TOKEN_ID

# Write to .env file
sudo_run bash << EOF
cat > .env << EOT
NODE_WALLET_ADDRESS=$WALLET
NODE_SIGNER_KEY=$USER_PRIVATE_KEY
MAIN_SERVER=$MAIN_SERVER
NODE_TOKEN_ID=$NODE_TOKEN_ID
EOT
EOF

echo ".env file created successfully!"

# Build and start Docker containers
echo "Pulling latest Docker containers..."
sudo_run docker-compose pull
echo "Building and starting Docker containers..."
sudo_run docker-compose up --build

sudo_run bash << EOF
cat << "EOT"
 ____       _               ____                      _      _           _ 
/ ___|  ___| |_ _   _ _ __ / ___|___  _ __ ___  _ __ | | ___| |_ ___  __| |
\___ \ / _ \ __| | | | '_ \| |   / _ \| '_ \` _ \| '_ \| |/ _ \ __/ _ \/ _\` |
 ___) |  __/ |_| |_| | |_) | |__| (_) | | | | | | |_) | |  __/ ||  __/ (_| |
|____/ \___|\__|\__,_| .__/ \____\___/|_| |_| |_| .__/|_|\___|\__\___|\__,_|
                     |_|                        |_|
EOT

echo "Your PlayAI Node Client is now running."
echo "To stop the containers, run: docker-compose down"
EOF
