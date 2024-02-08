import boto3


def update_route53_record(config, ip):
    """Update the Route 53 record."""
    client = boto3.client(
        'route53',
        aws_access_key_id=config['aws_key_id'],
        aws_secret_access_key=config['aws_key']
    )
    response = client.change_resource_record_sets(
        HostedZoneId=config['hosted_zone_id'],
        ChangeBatch={
            'Comment': 'update IP address',
            'Changes': [{
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': config['domain_name'],
                    'Type': config['record_type'],
                    'TTL': 300,
                    'ResourceRecords': [{'Value': ip}],
                }
            }]
        }
    )
    print(f"Updated IP address in Route 53 to {ip}: {response}")
