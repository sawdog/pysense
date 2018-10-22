from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'pysense',
    packages = ['pysense'], 
    install_requires=[
        'click',
        'confuse',
        'requests',
        'websocket-client',
    ],
    version = '0.7.0',
    description = 'API for the Sense Energy Monitor, forked from the sense project by scottbonline/sense',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = 'Andrew Sawyers',
    author_email = 'andrew@sawdog.com',
    url = 'https://github.com/sawdog/sense',
    keywords = ['sense', 'energy', 'monitot' 'api', 'pytest', 'python3',
                'python2'],
    classifiers = [],
    entry_points='''
        [console_scripts]
        sensecli=pysense.cli:cli
    ''',
)
