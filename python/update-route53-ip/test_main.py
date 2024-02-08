import pytest
from main import IpMonitor
import pdb

@pytest.fixture
def mock_config():
    return {
        'dry_run': 'true',
        'domain_name': 'example.com',
    }

@pytest.fixture
def ip_monitor(mock_config, mocker):
    mocker.patch('main.read_configs', return_value=mock_config)
    mocker.patch('main.update_route53_record')
    mocker.patch('main.resolve_domain_name', return_value="1.2.3.4")
    ip_lookup_client_mock = mocker.patch('main.IpLookupClient')
    ip_lookup_client_mock.return_value.check_ip_change.return_value = True
    ip_lookup_client_mock.return_value.ip = "1.2.3.4"
    return IpMonitor(mock_config, interval=0.1)

def create_mock_ip_lookup_client(mocker):
    mock_ip_lookup_client = mocker.Mock()
    mock_ip_lookup_client.ip = "1.2.3.4"
    mock_ip_lookup_client.check_ip_change.return_value = True
    return mock_ip_lookup_client

def test_ip_monitor_infinite_loop_prints_expected_messages(ip_monitor, mocker, capsys):
    mocker.patch('time.sleep', side_effect=InterruptedError) # allows our infinate loop to end

    with pytest.raises(InterruptedError):
        ip_monitor.monitor()

    captured = capsys.readouterr()

    assert "IP Change detected as: " in captured.out
    assert "INFO: dry_run was set, skipping." in captured.out


def test_ip_monitor_updates_route53_on_first_run_only_once(ip_monitor, mocker, capsys):
    ip_monitor.config['dry_run'] = 'false'
    mock_update_route53_record = mocker.patch('main.update_route53_record')
    mock_ip_lookup_client = create_mock_ip_lookup_client(mocker)

    ip_monitor._conduct_monitoring_cycle(mock_ip_lookup_client)

    mock_update_route53_record.assert_called_once_with(ip_monitor.config, "1.2.3.4")


def test_ip_monitor_checks_if_route53_record_changed_externally_regularly(ip_monitor, mocker, capsys):
    ip_monitor.config['dry_run'] = 'false'
    stubbed_resolve_domain_name = mocker.patch('main.resolve_domain_name')
    mock_ip_lookup_client = create_mock_ip_lookup_client(mocker)

    ip_monitor._conduct_monitoring_cycle(mock_ip_lookup_client)
    mock_ip_lookup_client.check_ip_change.return_value = False

    for i in range(20):
        ip_monitor._conduct_monitoring_cycle(mock_ip_lookup_client)

    # assert that _has_route53_record_changed_externally was called once
    stubbed_resolve_domain_name.assert_called_once_with(ip_monitor.config)
