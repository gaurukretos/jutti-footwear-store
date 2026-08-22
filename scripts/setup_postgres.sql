-- Run this in pgAdmin or psql as the postgres superuser
-- Creates the app database user and database for Raj Jutti House

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'jutti_user') THEN
        CREATE USER jutti_user WITH PASSWORD 'jutti_pass';
    ELSE
        ALTER USER jutti_user WITH PASSWORD 'jutti_pass';
    END IF;
END
$$;

SELECT 'CREATE DATABASE jutti_store OWNER jutti_user'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'jutti_store')\gexec

GRANT ALL PRIVILEGES ON DATABASE jutti_store TO jutti_user;
