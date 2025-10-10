#!/usr/bin/env python3
"""
Setup script for SOVD Server
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements_enhanced.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

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
