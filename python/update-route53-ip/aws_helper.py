import boto3

def update_route53_record(config, ip):
    """Update the Route 53 record."""
    if config['dry_run'] == 'true':
        print("INFO: dry_run was set, skipping update_route53_record.")
        return
    client = _get_client(config)
    response = client.change_resource_record_sets(
        HostedZoneId=config['hosted_zone_id'],
        ChangeBatch={
            'Comment': 'update IP address',
            'Changes': [{
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': config['domain_name'],
                    'Type': config['record_type'],
                    'TTL': 5,
                    'ResourceRecords': [{'Value': ip}],
                }
            }]
        }
    )
    print(f"Updated IP address in Route 53 to {ip}: {response}")


def resolve_domain_name(config):
    if config['dry_run'] == 'true':
        print("INFO: dry_run was set, skipping resolve_domain_name.")
        return
    client = _get_client(config)
    response = client.list_resource_record_sets(
        HostedZoneId=config['hosted_zone_id'],
        StartRecordName=config['domain_name'],
        StartRecordType=config['record_type'],
        MaxItems='1'
    )
    for record_set in response['ResourceRecordSets']:
        if record_set['Type'] == config['record_type'] and record_set['Name'][:-1] == config['domain_name']:
            for record in record_set['ResourceRecords']:
                return record['Value']
            break
    print(f"WARN: No A record found for {config['domain_name']}")
    return None


def _get_client(config):
    return boto3.client(
        'route53',
        aws_access_key_id=config['aws_key_id'],
        aws_secret_access_key=config['aws_key']
    )
