"""
SOVD (Service-Oriented Vehicle Data) Server

A Flask-based server implementation for the SOVD standard,
providing vehicle data access through RESTful APIs.
"""

__version__ = "1.1.0"
__author__ = "SOVD Development Team"
__email__ = "dev@sovd.org"

from .enhanced_server import app
from .config_loader import config_loader

__all__ = ["app", "config_loader"]
