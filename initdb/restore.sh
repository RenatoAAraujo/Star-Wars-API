#!/bin/bash
set -e

echo "Init databases restore"
mysql -quiet -uroot -p"$MYSQL_ROOT_PASSWORD" -e 'create database barber_dev'

echo "Restoring barber_dev"
gunzip < /docker-entrypoint-initdb.d/dumps/barber_dev.sql.gz | mysql -quiet -uroot -p"$MYSQL_ROOT_PASSWORD" barber_dev

echo "Database restored! ;)"