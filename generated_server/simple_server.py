#!/usr/bin/env python3
"""
Simple working SOVD server for testing
"""

from flask import Flask, jsonify
from sovd_server.controllers.default_controller import get_version_info, get_entities

app = Flask(__name__)

@app.route('/version-info', methods=['GET'])
def version_info():
    """Get server version information"""
    try:
        result = get_version_info()
        # Convert model to dict for JSON serialization
        if hasattr(result, 'to_dict'):
            return jsonify(result.to_dict())
        else:
            return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/<entity_collection>', methods=['GET'])
def entities(entity_collection):
    """Get entities for a collection"""
    try:
        result = get_entities(entity_collection)
        # Convert model to dict for JSON serialization
        if hasattr(result, 'to_dict'):
            return jsonify(result.to_dict())
        else:
            return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "SOVD Server is running"})

if __name__ == '__main__':
    print("Starting Simple SOVD Server...")
    print("Available endpoints:")
    print("  GET /version-info - Get server version information")
    print("  GET /{entity-collection} - Get entities (areas, components, apps)")
    print("  GET /health - Health check")
    print("\nServer running on http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)
