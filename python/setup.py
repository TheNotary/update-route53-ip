from setuptools import setup

setup(
    name='update_route53_ip',
    use_scm_version=True,  # Use setuptools_scm to get the version from the git tag
    description='Keeps Route53 up to date.',
    author='TheNotary',
    author_email='no@email.plz',
    py_modules=['update_route53_ip'],
    install_requires=['boto3', 'requests'],
    entry_points={
        'console_scripts': [
            'update-route53-ip=main:main',
        ],
    },
)
