#!/bin/bash
set -e

export PGPASSWORD="$DB_PASS"

psql -v ON_ERROR_STOP=1 --username "$DB_USER" <<-EOSQL
    CREATE DATABASE "$DB_NAME";
EOSQL