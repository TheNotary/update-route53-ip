import pytest
import requests_mock
from ip_lookup_client import IpLookupClient

@pytest.fixture
def ip_lookup_client():
    config = {'ip_lookup_url': 'https://example.com/ip'}
    return IpLookupClient(config)

def test_ip_change_detected(ip_lookup_client):
    with requests_mock.Mocker() as m:
        m.get('https://example.com/ip', text='1.2.3.4')
        assert ip_lookup_client.check_ip_change() == True, "IP change should be detected"

def test_ip_no_change(ip_lookup_client):
    ip_lookup_client.ip = '1.2.3.4'  # Set initial IP
    with requests_mock.Mocker() as m:
        m.get('https://example.com/ip', text='1.2.3.4')  # Same IP as initial
        assert ip_lookup_client.check_ip_change() == False, "No IP change should be detected"

def test_malformed_ip(ip_lookup_client):
    with requests_mock.Mocker() as m:
        m.get('https://example.com/ip', text='999.999.999.9999')  # Malformed IP
        assert ip_lookup_client.check_ip_change() == False, "Malformed IP should not be considered a change"

def test_error_handling_with_invalid_ip(ip_lookup_client, capsys):
    with requests_mock.Mocker() as m:
        m.get('https://example.com/ip', text='not.an.ip')
        ip_lookup_client.check_ip_change()
        captured = capsys.readouterr()
        assert "Error: Recieved invalid ip from lookup url." in captured.out

def test_error_handling_when_(ip_lookup_client, capsys):
    with requests_mock.Mocker() as m:
        m.get('https://example.com/ip', text='not.an.ip')
        ip_lookup_client.check_ip_change()
        captured = capsys.readouterr()
        assert "Error: Recieved invalid ip from lookup url." in captured.out

def test_get_external_ip_catches_exceptions_and_prints_them(ip_lookup_client, capsys):
    with requests_mock.Mocker() as m:
        m.get('https://example.com/ip', status_code=500)
        result = ip_lookup_client._get_external_ip()
        assert result is None
        captured = capsys.readouterr()
        assert "ERROR: Something went wrong trying to get our ip" in captured.out
