#!/bin/sh
set -e

until pg_isready -h db -p 5432 --quiet; do
  echo "Waiting for Postgres..."
  sleep 0.1
done

echo "Postgres is ready!"

python3 manage.py collectstatic --noinput
python3 manage.py migrate

exec gosu nonroot "$@"
