import json

import pytest


FOREMAN_HOST = 'localhost'
FOREMAN_PORT = 3000


@pytest.fixture(scope="module")
def foreman_status_curl(server):
    return server.run(f"curl --silent --write-out '%{{stderr}}%{{http_code}}' http://{FOREMAN_HOST}:{FOREMAN_PORT}/api/v2/ping")


@pytest.fixture(scope="module")
def foreman_status(foreman_status_curl):
    return json.loads(foreman_status_curl.stdout)


def test_foreman_service(server):
    foreman = server.service("foreman")
    assert foreman.is_running
    assert foreman.is_enabled


def test_foreman_port(server):
    foreman = server.addr(FOREMAN_HOST)
    assert foreman.port(FOREMAN_PORT).is_reachable


def test_foreman_status(foreman_status_curl):
    assert foreman_status_curl.succeeded
    assert foreman_status_curl.stderr == '200'


def test_foreman_status_database(foreman_status):
    assert foreman_status['results']['foreman']['database']['active']


def test_foreman_status_cache(foreman_status):
    assert foreman_status['results']['foreman']['cache']['servers']
    assert foreman_status['results']['foreman']['cache']['servers'][0]['status'] == 'ok'


@pytest.mark.parametrize("katello_service", ['candlepin', 'candlepin_auth', 'candlepin_events', 'foreman_tasks', 'katello_events', 'pulp3', 'pulp3_content'])
def test_katello_services_status(foreman_status, katello_service):
    if katello_service == 'foreman_tasks':
        pytest.xfail("Foreman Tasks needs to boot workers, we don't wait enough")
    assert foreman_status['results']['katello']['services'][katello_service]['status'] == 'ok'


@pytest.mark.parametrize("dynflow_instance", ['orchestrator', 'worker', 'worker-hosts-queue'])
def test_foreman_dynflow_container_instances(server, dynflow_instance):
    file = server.file(f"/etc/containers/systemd/dynflow-sidekiq@{dynflow_instance}.container")
    assert file.exists
    assert file.is_symlink


@pytest.mark.parametrize("dynflow_instance", ['orchestrator', 'worker', 'worker-hosts-queue'])
def test_foreman_dynflow_service_instances(server, dynflow_instance):
    service = server.service(f"dynflow-sidekiq@{dynflow_instance}")
    assert service.is_running
    assert service.is_enabled
