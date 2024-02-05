from setuptools import setup

setup(
    name='update_route53_ip',
    version='1.0.0',
    description='Keeps Route53 up to date.',
    author='TheNotary',
    author_email='no@email.plz',
    py_modules=['update_route53_ip'],
    install_requires=['boto3', 'requests'],
    entry_points={
        'console_scripts': [
            'update-route53-ip=update_route53_ip:main',
        ],
    },
)
