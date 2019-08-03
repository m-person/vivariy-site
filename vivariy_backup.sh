#!/usr/bin/env bash
# create a backup of vivariy site
# the result file is stored in the /home/www/vivariy/backups/ dir

set -e

echo "perform a db dump..."
rm -rf ./docker_share/*
docker exec -t vivariy_db_1 pg_dump -Upostgres --file=/tmp/docker_share/db_dump.sql vivariy_site

echo "create an archive..."
DEST=/home/www/vivariy/backups
rm $DEST/*
tar -czf $DEST/vivariy_`date +%F`.tar.gz --exclude "$DEST/" .

echo "done. The backup was created in $DEST"
