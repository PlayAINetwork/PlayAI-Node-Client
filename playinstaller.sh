#!/bin/bash

cat << "EOF"
 _____  _              ___    _ 
|  __ \| |            / _ \  (_)
| |__) | | __ _ _   _/ /_\ \  _ 
|  ___/| |/ _` | | | |  _  | | |
| |    | | (_| | |_| | | | | | |
|_|    |_|\__,_|\__, \_| |_/ |_|
                 __/ |         
                |___/          
    _   _           _        _____ _ _            _   
   | \ | |         | |      / ____| (_)          | |  
   |  \| | ___   __| | ___ | |    | |_  ___ _ __ | |_ 
   | . ` |/ _ \ / _` |/ _ \| |    | | |/ _ \ '_ \| __|
   | |\  | (_) | (_| |  __/| |____| | |  __/ | | | |_ 
   |_| \_|\___/ \__,_|\___| \_____|_|_|\___|_| |_|\__|
                                                      
EOF

echo "Welcome to the PlayAI Node Client Setup Script"
echo "----------------------------------------------"

read -p "Do you want to set up the PlayAI Node Client? (y/Y to continue): " answer </dev/tty
if [[ "$answer" != "y" && "$answer" != "Y" ]]; then
    echo "Setup cancelled."
    exit 1
fi

# Function to prompt for input
get_input() {
    local prompt="$1"
    local var_name="$2"
    
    read -p "$prompt: " input
    eval $var_name="$input"
}

# Install Docker
echo "Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
rm get-docker.sh

# Install specific version of Docker Compose
echo "Installing Docker Compose 2.17.2..."
curl -SL https://github.com/docker/compose/releases/download/v2.17.2/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify Docker Compose version
COMPOSE_VERSION=$(docker-compose version --short)
if [ "$(printf '%s\n' "2.17.2" "$COMPOSE_VERSION" | sort -V | head -n1)" != "2.17.2" ]; then
    echo "Error: Docker Compose version 2.17.2 or higher is required. Current version: $COMPOSE_VERSION"
    exit 1
fi

# Install additional dependencies
echo "Installing additional dependencies..."
sudo apt-get update && apt-get install -y git

# Clone the repository
echo "Cloning the PlayAI-Node-Client repository..."
git clone https://github.com/PlayAINetwork/PlayAI-Node-Client.git
cd PlayAI-Node-Client

# Create .env file
echo "Setting up .env file..."
get_input "Enter WALLET address" WALLET
get_input "Enter USER_PRIVATE_KEY" USER_PRIVATE_KEY
get_input "Enter MAIN_SERVER URL" MAIN_SERVER
get_input "Enter NFT_TOKEN_ID" NFT_TOKEN_ID

# Write to .env file
cat > .env << EOF
WALLET=$WALLET
USER_PRIVATE_KEY=$USER_PRIVATE_KEY
MAIN_SERVER=$MAIN_SERVER
NFT_TOKEN_ID=$NFT_TOKEN_ID
EOF

echo ".env file created successfully!"

# Build and start Docker containers
echo "Building and starting Docker containers..."
sudo docker-compose up --build -d

cat << "EOF"
 ____           _                ____                      _      _       _ 
/ ___|  ___ ___| |_ _   _ _ __  / ___|___  _ __ ___  _ __ | | ___| |_ ___| |
\___ \ / _ \ __| __| | | | '_ \| |   / _ \| '_ ` _ \| '_ \| |/ _ \ __/ _ \ |
 ___) |  __\__ \ |_| |_| | |_) | |__| (_) | | | | | | |_) | |  __/ ||  __/_|
|____/ \___|___/\__|\__,_| .__/ \____\___/|_| |_| |_| .__/|_|\___|\__\___(_)
                         |_|                        |_|                     
EOF

echo "Your PlayAI Node Client is now running."
echo "To stop the containers, run: docker-compose down"