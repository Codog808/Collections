#!/bin/bash

# Variables
IMAGE_NAME="display_app_image"
CONTAINER_NAME="display_app_debug"
PORT=5000

# Build the Docker image
echo "🔨 Building Docker image..."
docker build -t $IMAGE_NAME ./ # Ensure the context is the current directory

# Stop and remove existing container if it exists
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
  echo "🛑 Stopping and removing existing container..."
  docker stop $CONTAINER_NAME
  docker rm $CONTAINER_NAME
fi

# Run the container
echo "🚀 Running the container on port $PORT..."
docker run --name $CONTAINER_NAME --network collections_debug -p $PORT:5000 $IMAGE_NAME
