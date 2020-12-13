# Automatically created by: scrapyd-deploy

from setuptools import setup, find_packages

setup(
    name         = 'project',
    version      = '1.0',
    packages     = find_packages(),
    package_data={
            'project': ['resources/*.txt']
    },
    entry_points = {'scrapy': ['settings = roc.settings']},
    zip_safe=False,
)
