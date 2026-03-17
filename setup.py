#!/usr/bin/env python3
"""
Setup script for SOVD Server
"""

import os

from setuptools import setup, find_packages

_ROOT = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(_ROOT, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements_path = os.path.join(_ROOT, "requirements.txt")
if os.path.isfile(requirements_path):
    with open(requirements_path, "r", encoding="utf-8") as fh:
        requirements = []
        for line in fh:
            line = line.strip()
            if line.startswith("# Development"):
                break
            if line and not line.startswith("#"):
                requirements.append(line)
else:
    # Fallback when building from sdist without requirements.txt (use pyproject.toml deps)
    requirements = [
        "flask>=3.1.0",
        "flask-cors>=3.0.0",
        "pyyaml>=6.0",
        "connexion[swagger-ui]>=3.0.0,<=3.3.0",
        "jsonschema>=4.0.0",
    ]

setup(
    name="sovd-server",
    version="1.0.0",
    author="SOVD Development Team",
    author_email="dev@sovd.org",
    description="SOVD (Service-Oriented Vehicle Data) Server Implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sovd/sovd-server",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
        ],
    },
    entry_points={
        "console_scripts": [
            "sovd-server=src.sovd_server.run_enhanced_server:main",
        ],
    },
    include_package_data=True,
    package_data={
        "sovd_server": [
            "config/*.yaml",
            "config/**/*.yaml",
        ],
    },
)
