#!/bin/bash

set -e

docker-compose -f docker-compose-test.yml up --abort-on-container-exit
