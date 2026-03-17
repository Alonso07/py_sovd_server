#!/usr/bin/env python3
"""
Simple test server without authentication for testing the SOVD API endpoints
"""

import connexion
import sys
import os

# Add the generated directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "generated"))

from sovd_server import encoder
from sovd_server.controllers import default_controller


def create_app():
    """Create the Flask app without authentication"""
    app = connexion.App(
        __name__,
        specification_dir=os.path.join(
            os.path.dirname(__file__), "..", "generated", "sovd_server", "openapi"
        ),
    )
    app.app.json_encoder = encoder.JSONEncoder

    # Add API without security requirements
    app.add_api(
        "openapi.yaml",
        arguments={"title": "SOVD API"},
        pythonic_params=True,
        strict_validation=False,
        validate_responses=False,
    )

    # Disable authentication for testing
    @app.app.before_request
    def disable_auth():
        pass

    return app


if __name__ == "__main__":
    app = create_app()
    print("Starting SOVD Server (no authentication)...")
    print("Available endpoints:")
    print("  GET /version-info - Get server version information")
    print("  GET /{entity-collection} - Get entities (areas, components, apps)")
    print("  GET /{entity-path}/faults - Get faults for an entity")
    print("  GET /{entity-path}/data - Get data resources for an entity")
    print("  And many more...")
    print("\nServer running on http://localhost:8080")
    app.run(port=8080)
