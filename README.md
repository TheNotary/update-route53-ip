# Update Route53 IP

This script is meant to run from one of the VMs on the basement cloud, or ideally the k8s server.

It's a python3 script that runs via systemd and uses boto3 to interact with AWS Route53 based on credentials which should be collected at install time and populated in `/etc/update-route53-ip/config`.  


## Development Testing

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python update_route53_ip.py
```


## Credentials

The credentials are generated in the terraform-aws.  They're named automated_tf, you can dig it out of the state file.


## Deploy

This service is tested against Raspbian.  

Run the installer to
- Automatically populate ~/.aws/credentials
- Populate the /etc/systemd/system/update-route53-ip.service service to run via the currently logged in user

```
./install.sh
Enter the aws secret access key (the long string): ...
Enter the aws key_id (the short string): ...
done :)
```
