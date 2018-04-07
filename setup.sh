#!/bin/bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $CURRENT_DIR

# database
DB_NAME=rover
psql -U rover -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity \
WHERE pg_stat_activity.datname = '${DB_NAME}' AND pid <> pg_backend_pid();"

dropdb rover
createdb rover

# django
cd Rover-Django/rover/

# should be able to remove this once I stop wiping out "makemigrations"
./manage.py makemigrations customer review util

# migrate schema
./manage.py migrate

./manage.py populate_tables
