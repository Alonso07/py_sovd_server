#!/usr/bin/env python3
"""
Debug server to test entity lookup
"""

import os
import sys
from flask import Flask, jsonify

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from sovd_server.config_loader import config_loader

app = Flask(__name__)

# Load configuration
config_loader.load_all_configs()

@app.route('/debug/<entity_path>')
def debug_entity(entity_path):
    """Debug entity lookup"""
    try:
        print(f"Debug: Looking up entity: {entity_path}")
        
        # Find entity in any collection
        entity = None
        for entity_type in ['areas', 'components', 'apps']:
            print(f"Debug: Checking {entity_type}...")
            entity = config_loader.get_entity_by_id(entity_type, entity_path)
            if entity:
                print(f"Debug: Found in {entity_type}: {entity['name']}")
                break
            else:
                print(f"Debug: Not found in {entity_type}")
        
        if not entity:
            print(f"Debug: Entity not found: {entity_path}")
            return jsonify({"error": "Entity not found", "path": entity_path}), 404
        
        print(f"Debug: Entity found: {entity['name']}")
        return jsonify({
            "entity": entity,
            "message": "Entity found successfully"
        })
        
    except Exception as e:
        print(f"Debug: Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/debug/data/<entity_path>/<resource_id>')
def debug_data_resource(entity_path, resource_id):
    """Debug data resource lookup"""
    try:
        print(f"Debug: Looking up data resource {resource_id} for {entity_path}")
        
        resource = config_loader.get_data_resource(entity_path, resource_id)
        if not resource:
            print(f"Debug: Resource not found: {resource_id}")
            return jsonify({"error": "Resource not found"}), 404
        
        print(f"Debug: Resource found: {resource['name']}")
        return jsonify({
            "resource": resource,
            "message": "Resource found successfully"
        })
        
    except Exception as e:
        print(f"Debug: Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Debug Server...")
    print("Test endpoints:")
    print("  GET /debug/engine")
    print("  GET /debug/data/engine/SoftwarePartNumber")
    app.run(host='0.0.0.0', port=8081, debug=True)
