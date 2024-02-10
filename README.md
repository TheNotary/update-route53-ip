# Update Route53 IP

This script is meant to run from one of the VMs on the basement cloud, or ideally the k8s server.

It's a python3 script that runs via systemd and uses boto3 to interact with AWS Route53 based on credentials which should be collected at install time and populated in `/etc/update-route53-ip/config`.


## Dependencies

To build you'll need to have this stuff.  Make sure you're using those instead of Mac's built-ins (you've configured this in .mac_fixes)

```
brew install gnu-tar gnu-sed
gem install fpm
```

## Development Testing the Script

All of the python related command should be done within the `python` folder which encapsulates most of the python app.

```
cd python

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python update-route53-ip/main.py
```

## Build the Pip Package (academic)

```
python -m build
```

## Run the Tests

```
pytest
```

## Credentials

The credentials are generated in the terraform-aws.  They're named automated_tf, you can dig it out of the state file.


## Deploy

This service is tested against Raspbian.

###### Steps:
- build the deb package locally
- scp the .deb file to the target machine
- install the deb and fill in configuration values as prompted

```
./build_package.sh
scp update-route53-ip_1.0.0_all.deb target:/home/username/
ssh target
dpkg -i update-route53-ip_1.0.0_all.deb
```

