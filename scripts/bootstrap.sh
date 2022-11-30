#!/bin/bash

set -e

# Build and configure environment

echo "Build containers"

docker-compose build
docker-compose -f docker-compose-test.yml build

echo "Applying migrations"

docker-compose run --rm api python manage.py migrate

echo "Finished"
