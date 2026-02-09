#!/bin/sh

# Wait for the database to be ready (optional, but good practice for race conditions)
if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for postgres..."
  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
  done
  echo "PostgreSQL started"
fi

# Run the database migration command (example for Django, adjust for your framework)
echo "Running database migrations..."
python manage.py migrate --noinput || exit 1

# Execute the main application command (from the Dockerfile's CMD)
exec "$@"
