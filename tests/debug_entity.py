#!/usr/bin/env python3
"""
Debug entity lookup in the server context
"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from sovd_server.config_loader import config_loader


def debug_entity_lookup():
    """Debug entity lookup with detailed logging"""

    print("Debugging Entity Lookup in Server Context")
    print("=" * 50)

    # Load all configs
    config_loader.load_all_configs()

    # Test the exact same logic as in the server
    entity_path = "/engine"
    print(f"Looking up entity: {entity_path}")

    entity = None
    for entity_type in ["areas", "components", "apps"]:
        print(f"  Checking {entity_type}...")
        entity = config_loader.get_entity_by_id(entity_type, entity_path)
        if entity:
            print(f"  ✓ Found in {entity_type}: {entity['name']}")
            break
        else:
            print(f"  ✗ Not found in {entity_type}")

    if not entity:
        print("  ✗ Entity not found in any collection")
        return False

    print(f"  Entity details:")
    print(f"    - ID: {entity['id']}")
    print(f"    - Name: {entity['name']}")
    print(f"    - Endpoints: {list(entity['endpoints'].keys())}")
    print(f"    - Resources: {list(entity.get('resources', {}).keys())}")

    # Test data resource lookup
    print(f"\nTesting data resource lookup for {entity_path}...")
    resource_files = entity.get("resources", {}).get("data_resources", [])
    print(f"  Resource files: {resource_files}")

    for resource_file in resource_files:
        print(f"  Loading resource file: {resource_file}")
        try:
            resource_config = config_loader.load_resource_config("data", resource_file)
            resources = resource_config.get("data_resources", [])
            print(f"    Found {len(resources)} resources")
            for resource in resources:
                print(f"      - {resource['id']}: {resource['name']}")
        except Exception as e:
            print(f"    Error loading {resource_file}: {e}")

    return True


if __name__ == "__main__":
    debug_entity_lookup()
