import sys
from setuptools import setup, find_packages

NAME = "sovd_server"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion>=2.0.2",
    "swagger-ui-bundle>=0.0.2",
    "python_dateutil>=2.6.0"
]

setup(
    name=NAME,
    version=VERSION,
    description="SOVD (Service-Oriented Vehicle Diagnostics) API",
    author_email="",
    url="",
    keywords=["OpenAPI", "SOVD (Service-Oriented Vehicle Diagnostics) API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['sovd_server=sovd_server.__main__:main']},
    long_description="""\
    This API specification defines the Service-Oriented Vehicle Diagnostics (SOVD) interface  according to ISO/DIS 17978-3:2025. The SOVD API provides access to vehicle diagnostics,  fault handling, data resources, operations, target modes, and configuration management. 
    """
)

