#!/bin/bash
echo "Building Docker containers..."
docker-compose up -d --build

echo "Initializing Elasticsearch..."
python services/database/scripts/init_es.py