import pytest
from unittest.mock import patch, MagicMock
import aws_helper


mock_config = {
    'dry_run': 'true',
    'aws_key_id': 'dummyId',
    'aws_key': 'dummySecret',
    'hosted_zone_id': 'dummyZone',
    'domain_name': 'example.com',
    'record_type': 'A'
}


def test_update_route53_record_dry_run():
    with patch('aws_helper._get_client') as mock_get_client:
        aws_helper.update_route53_record(mock_config, '1.2.3.4')
        mock_get_client.assert_not_called()


def test_update_route53_record_actual():
    mock_client = MagicMock()
    mock_response = {'ChangeInfo': {'Id': '12345'}}
    mock_client.change_resource_record_sets.return_value = mock_response
    with patch('aws_helper._get_client', return_value=mock_client):
        mock_config['dry_run'] = 'false'
        aws_helper.update_route53_record(mock_config, '1.2.3.4')
        mock_client.change_resource_record_sets.assert_called_once_with(HostedZoneId='dummyZone', ChangeBatch={'Comment': 'update IP address', 'Changes': [{'Action': 'UPSERT', 'ResourceRecordSet': {'Name': 'example.com', 'Type': 'A', 'TTL': 5, 'ResourceRecords': [{'Value': '1.2.3.4'}]}}]})


def test_resolve_domain_name_dry_run():
    with patch('aws_helper._get_client') as mock_get_client:
        aws_helper.resolve_domain_name(mock_config)
        mock_get_client.assert_not_called()


def test_resolve_domain_name_actual():
    mock_client = MagicMock()
    mock_response = {
        'ResourceRecordSets': [{
            'Type': 'A',
            'Name': 'example.com.',
            'ResourceRecords': [{'Value': '1.2.3.4'}]
        }]
    }
    mock_client.list_resource_record_sets.return_value = mock_response
    with patch('aws_helper._get_client', return_value=mock_client):
        mock_config['dry_run'] = 'false'
        result = aws_helper.resolve_domain_name(mock_config)
        assert result == '1.2.3.4'
        mock_client.list_resource_record_sets.assert_called_once_with(HostedZoneId='dummyZone', StartRecordName='example.com', StartRecordType='A', MaxItems='1')


@pytest.fixture(autouse=True)
def reset_config():
    """Reset mock config to dry_run true after each test."""
    mock_config['dry_run'] = 'true'
