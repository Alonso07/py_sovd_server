#!/usr/bin/env python3
"""
Run Enhanced SOVD Server using Poetry
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import and run the enhanced server
from enhanced_server import app, gateway_config

if __name__ == '__main__':
    # Get configuration
    host = gateway_config['gateway']['network']['host']
    port = 8087  # Use different port to avoid conflicts
    debug = gateway_config['gateway']['network']['debug']
    
    print("Starting Enhanced SOVD Server...")
    print(f"Configuration loaded from: config/")
    print(f"Available endpoints:")
    print("  GET /version-info - Get server version information")
    print("  GET /{entity-collection} - Get entities (areas, components, apps)")
    print("  GET /{entity-path} - Get entity capabilities")
    print("  GET /{entity-path}/data - Get data resources")
    print("  GET /{entity-path}/data/{data_id} - Get specific data resource")
    print("  GET /{entity-path}/operations - Get operations")
    print("  GET /{entity-path}/operations/{operation_id} - Get specific operation")
    print("  POST /{entity-path}/operations/{operation_id} - Start operation execution")
    print("  GET /{entity-path}/faults - Get faults")
    print("  GET /{entity-path}/modes - Get modes")
    print("  GET /health - Health check")
    print(f"\nServer running on http://{host}:{port}")
    
    app.run(host=host, port=port, debug=debug)
