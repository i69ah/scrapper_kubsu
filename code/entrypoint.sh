#!/bin/sh

groupadd -g 10000 www-data
useradd -u 10000 -g 10000 scrapper

mkdir -p "/app/static/" "/app/media/"

chown -R scrapper:www-data "/app"

if [ "$DATABASE" = "postgres" ]
then
  echo "Waiting for postgres db..."

  while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

#python manage.py flush --no-input
#python manage.py migrate

python3 manage.py collectstatic

exec "$@"