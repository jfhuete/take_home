#!/bin/bash

set -e

chown -R $USER:$USER data

docker-compose build
