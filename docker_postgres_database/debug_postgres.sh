#!/bin/bash

# Variables
CONTAINER_NAME="postgres_collections_debug"
IMAGE_NAME="postgres:latest"
HOST_PORT=5432
CONTAINER_PORT=5432
# Stop and remove existing container if it exists
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
  echo "🛑 Stopping and removing existing container..."
  docker stop $CONTAINER_NAME
  docker rm $CONTAINER_NAME
fi

# Run PostgreSQL container
docker run \
  --name $CONTAINER_NAME \
  --network collections_debug \
  -p $HOST_PORT:$CONTAINER_PORT \
  -v $(pwd)/data:/var/lib/postgresql/data \
  $IMAGE_NAME
