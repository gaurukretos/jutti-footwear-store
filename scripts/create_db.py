"""Create jutti_store database and jutti_user for the footwear project."""

import os
import sys

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def get_admin_password():
    password = os.environ.get("POSTGRES_PASSWORD")
    if password:
        return password
    if len(sys.argv) > 1:
        return sys.argv[1]
    print("PostgreSQL admin password required.")
    print("")
    print("Usage:")
    print('  $env:POSTGRES_PASSWORD="YOUR_POSTGRES_PASSWORD"')
    print("  python scripts/create_db.py")
    print("")
    print("Or:")
    print('  python scripts/create_db.py "YOUR_POSTGRES_PASSWORD"')
    print("")
    print("Use the password you set when installing PostgreSQL (postgres user).")
    sys.exit(1)


def main():
    admin_password = get_admin_password()
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", "5432")
    admin_user = os.environ.get("POSTGRES_ADMIN_USER", "postgres")

    print(f"Connecting to PostgreSQL at {host}:{port} as {admin_user}...")

    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=admin_user,
            password=admin_password,
            host=host,
            port=port,
        )
    except psycopg2.OperationalError as exc:
        print(f"Connection failed: {exc}")
        print("")
        print("Tips:")
        print("- Use the password from PostgreSQL installation (postgres user)")
        print("- PostgreSQL 18 uses port 5432, PostgreSQL 16 uses port 5433")
        print('- Try: $env:POSTGRES_PORT="5433" if port 5432 fails')
        sys.exit(1)

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_roles WHERE rolname = 'jutti_user'")
    if cur.fetchone():
        cur.execute("ALTER USER jutti_user WITH PASSWORD 'jutti_pass'")
        print("Updated password for user: jutti_user")
    else:
        cur.execute("CREATE USER jutti_user WITH PASSWORD 'jutti_pass'")
        print("Created user: jutti_user")

    cur.execute("SELECT 1 FROM pg_database WHERE datname = 'jutti_store'")
    if cur.fetchone():
        print("Database already exists: jutti_store")
    else:
        cur.execute("CREATE DATABASE jutti_store OWNER jutti_user")
        print("Created database: jutti_store")

    cur.execute("GRANT ALL PRIVILEGES ON DATABASE jutti_store TO jutti_user")
    cur.close()
    conn.close()

    print("")
    print("Database setup complete!")
    print("Next steps:")
    print("  python manage.py migrate")
    print("  python manage.py seed_data")
    print("  python manage.py runserver")


if __name__ == "__main__":
    main()
