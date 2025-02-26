def test_postgresql_service(server):
    postgresql = server.service("postgresql")
    assert postgresql.is_running
    assert postgresql.is_enabled

def test_postgresql_port(server):
    postgresql = server.addr("localhost")
    assert postgresql.port("5432").is_reachable

def test_postgresql_databases(server):
    result = server.run("podman exec postgresql psql -U postgres -c '\\l'")
    assert "foreman" in result.stdout
    assert "candlepin" in result.stdout
    assert "pulp" in result.stdout

def test_postgresql_users(server):
    result = server.run("podman exec postgresql psql -U postgres -c '\\du'")
    assert "foreman" in result.stdout
    assert "candlepin" in result.stdout
    assert "pulp" in result.stdout

def test_postgresql_hba_config(server):
    result = server.run("podman exec postgresql cat /var/lib/pgsql/data/pg_hba.conf")
    assert "host all all 127.0.0.1/32 md5" in result.stdout
    assert "host all all ::1/128 md5" in result.stdout
