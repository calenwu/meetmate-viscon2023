#!/bin/bash
# check who owns the working directory
echo "Running command '$*'"
exec /bin/bash -c "$*"

#echo "Running command '$*'"
#exec $*
#exec python manage.py runserver 0.0.0.0:8000