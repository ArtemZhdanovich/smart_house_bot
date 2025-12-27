#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$DB_USER" <<-EOSQL
DO
$$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_database WHERE datname = '$DB_NAME'
    ) THEN
        CREATE DATABASE "$DB_NAME";
    END IF;
END
$$;
EOSQL
