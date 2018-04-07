#!/bin/bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $CURRENT_DIR

# database
dropdb rover
createdb rover

# django
cd Rover-Django/rover/

# should be able to remove this once I stop wiping out "makemigrations"
./manage.py makemigrations customer review util

# migrate schema
./manage.py migrate

./manage.py populate_raw_reviews
