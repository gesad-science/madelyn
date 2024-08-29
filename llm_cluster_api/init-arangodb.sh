#!/bin/sh
set -e

ARANGO_ROOT_PASSWORD=${ARANGO_ROOT_PASSWORD:-"123"}

arangod --database.password '123' &

echo "Initializing Arangodb..."
sleep 2

echo "Creating 'madelyn_model_storage_database' database"

curl -X POST http://0.0.0.0:8529/_db/_system/_api/database \
  -H 'Content-Type: application/json' \
  -u root:$ARANGO_ROOT_PASSWORD \
  -d '{"name": "madelyn_model_storage_database"}'

echo "'madelyn_model_storage_database' created"

wait
