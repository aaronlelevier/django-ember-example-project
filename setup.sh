#!/bin/bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $CURRENT_DIR

# ember
cd Rover-Ember/rover/

echo "Build Ember assets"
ember build --env=production

echo "Copy over static assets"
cd $CURRENT_DIR/Rover-Django/rover

# remove old files
rm -rf ember/*
rm -rf static/*
rm templates/index.html
# copy over new
cp -r ../../Rover-Ember/rover/dist/assets ember
cp -r ../../Rover-Ember/rover/dist/fonts ember
cp -r ../../Rover-Ember/rover/dist/index.html templates

echo "Activate virtualenv"
cd $CURRENT_DIR/Rover-Django

if [ ! -d venv ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt

cd $CURRENT_DIR/Rover-Django/rover

echo "Collect static assets"
./manage.py collectstatic --noinput

echo "Populate database"
DB_NAME=rover
psql -U rover -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity \
WHERE pg_stat_activity.datname = '${DB_NAME}' AND pid <> pg_backend_pid();"
dropdb rover
createdb rover

# django
./manage.py migrate
./manage.py populate_tables
