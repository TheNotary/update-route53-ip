import pytest
from unittest.mock import Mock, MagicMock, patch
import config_reader
from config_reader import read_configs
from configparser import ConfigParser
from pathlib import Path
import copy

valid_config_data = {
    'update-route53-ip': {
        'aws_key': 'testkey',
        'aws_key_id': 'testkeyid',
        'hosted_zone_id': 'testzoneid',
        'domain_name': 'example.com',
        'ip_lookup_url': 'http://ip.example.com',
        'record_type': 'A',
        'dry_run': 'true'
    }
}

incomplete_config_data = {
    'update-route53-ip': {
        'aws_key_id': 'testkeyid',
        # Missing other required keys
    }
}

@pytest.fixture
def mock_config(monkeypatch):
    # Mock Path.is_file() to always return True
    monkeypatch.setattr(Path, "is_file", Mock(return_value=True))
    mock_parser = create_mock_config_parser(valid_config_data)
    monkeypatch.setattr(config_reader, "configparser", Mock(ConfigParser=lambda: mock_parser))
    return valid_config_data['update-route53-ip']

def create_mock_config_parser(config_data):
    mock_parser = MagicMock(ConfigParser)
    mock_parser.__getitem__.side_effect = config_data.__getitem__
    mock_parser.read = Mock()
    return mock_parser


#########
# TESTS #
#########


def test_read_configs_success(mock_config):
    config = read_configs()

    assert config['aws_key'] == 'testkey'
    assert config['dry_run'] == 'true'


def test_validate_required_keys_missing(monkeypatch):
    monkeypatch.setattr(Path, "is_file", MagicMock(return_value=True))
    incomplete_config_data = copy.deepcopy(valid_config_data)
    del incomplete_config_data['update-route53-ip']['aws_key']
    mock_parser = create_mock_config_parser(incomplete_config_data)
    monkeypatch.setattr(config_reader, "configparser", MagicMock(ConfigParser=lambda: mock_parser))

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        read_configs()

    assert pytest_wrapped_e.type == SystemExit
    assert "ERROR: Config item aws_key was set incorrectly" in str(pytest_wrapped_e.value)


def test_raises_exception_when_key_has_tilde(monkeypatch):
    monkeypatch.setattr(Path, "is_file", MagicMock(return_value=True))
    misconfigured_config_data = copy.deepcopy(valid_config_data)
    misconfigured_config_data['update-route53-ip']['aws_key'] = "~AWS_KEY~"
    mock_parser = create_mock_config_parser(misconfigured_config_data)
    monkeypatch.setattr(config_reader, "configparser", MagicMock(ConfigParser=lambda: mock_parser))

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        read_configs()

    assert pytest_wrapped_e.type == SystemExit
    assert "ERROR: Config item aws_key was set incorrectly" in str(pytest_wrapped_e.value)


def test_validate_dry_run_value_invalid(monkeypatch):
    misconfigured_config_data = copy.deepcopy(valid_config_data)
    misconfigured_config_data['update-route53-ip']['dry_run'] = "maybe"
    mock_parser = create_mock_config_parser(misconfigured_config_data)
    monkeypatch.setattr(config_reader, "configparser", MagicMock(ConfigParser=lambda: mock_parser))
    monkeypatch.setattr(Path, "is_file", Mock(return_value=True))

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        read_configs()

    assert pytest_wrapped_e.type == SystemExit
    assert "ERROR: Config item dry_run must be set to either 'true' or 'false'" in str(pytest_wrapped_e.value)
