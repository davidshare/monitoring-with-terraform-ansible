#!/bin/bash

# Update package index
echo "Updating package index..."
sudo yum update -y

# Install Docker
echo "Installing Docker..."
sudo yum install -y docker
sudo service docker start
sudo systemctl enable docker  # Ensures Docker starts on boot
sudo usermod -aG docker ec2-user

# Install jq (needed to parse JSON for Docker Compose version)
echo "Installing jq..."
sudo yum install -y jq

# Install Docker Compose (latest version)
echo "Installing Docker Compose..."
DOCKER_COMPOSE_LATEST_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | jq -r .tag_name)
sudo curl -L "https://github.com/docker/compose/releases/download/$DOCKER_COMPOSE_LATEST_VERSION/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Git
echo "Installing Git..."
sudo yum install -y git

# Set the path for cloning the repository
CLONE_DIR="/home/ec2-user/monitoring"

# Check if the directory exists
if [ -d "$CLONE_DIR" ]; then
  echo "Directory '$CLONE_DIR' already exists. Skipping git clone."
else
  echo "Cloning repository into '$CLONE_DIR'..."
  git clone https://github.com/davidshare/monitoring-project.git "$CLONE_DIR"
  if [ $? -eq 0 ]; then
    echo "Repository cloned successfully."
  else
    echo "Failed to clone the repository. Please check the URL and network connectivity."
    exit 1
  fi
fi

mkdir -p "{$CLONE_DIR}/letsencrypt"
touch "{$CLONE_DIR}/letsencrypt/acme-staging.json"
touch "{$CLONE_DIR}/letsencrypt/acme-production.json"
chmod 600 "{$CLONE_DIR}/letsencrypt/acme-staging.json"  # Set proper permissions
chmod 600 "{$CLONE_DIR}/letsencrypt/acme-production.json"  # Set proper permissions

# Verify installations
echo "Verifying installations..."
docker version
docker-compose version

# Print success message
echo "Docker, Docker Compose, and Git have been successfully installed. The repository is cloned into '$CLONE_DIR'."
