# Use the official PostgreSQL image as the base
FROM postgres:latest

# Set environment variables
# These can be overridden using --build-arg during docker build if needed
ARG POSTGRES_USER=admin
ARG POSTGRES_PASSWORD=password
ARG POSTGRES_DB=default

ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_DB=$POSTGRES_DB

# Expose the PostgreSQL default port
EXPOSE 5432

# The official postgres image already has an entrypoint
# No CMD or ENTRYPOINT override needed unless custom behavior is required
