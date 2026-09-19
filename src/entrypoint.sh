#!/bin/sh
set -e

python3 manage.py collectstatic --noinput

#exec gosu nonroot "$@"
exec "$@"
