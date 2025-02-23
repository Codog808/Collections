#!/bin/bash

# Define variables
CONTAINER_NAME="postgres_interface_debug"
IMAGE_NAME="postgres_interface:latest"
HOST_PORT=8000
CONTAINER_PORT=8000

# Build the Docker image
echo "Building Docker image..."
docker build -t $IMAGE_NAME .

# Stop and remove existing container if it exists
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
  echo "🛑 Stopping and removing existing container..."
  docker stop $CONTAINER_NAME
  docker rm $CONTAINER_NAME
fi

# Run the container normally for debugging purposes
echo "Running container..."
docker run \
  --name $CONTAINER_NAME \
  --network collections_debug \
  -p $HOST_PORT:$CONTAINER_PORT \
  $IMAGE_NAME
