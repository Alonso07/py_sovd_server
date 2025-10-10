#!/usr/bin/env python3
"""
Test server configuration loading
"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from sovd_server.config_loader import config_loader

def test_server_config():
    """Test configuration loading in server context"""
    
    print("Testing Server Configuration Loading")
    print("=" * 40)
    
    # Test the exact same initialization as in the server
    print("1. Loading all configurations...")
    config_loader.load_all_configs()
    
    print("2. Testing entity lookup...")
    entity_path = "/engine"
    entity = None
    for entity_type in ['areas', 'components', 'apps']:
        print(f"  Checking {entity_type}...")
        entity = config_loader.get_entity_by_id(entity_type, entity_path)
        if entity:
            print(f"  ✓ Found in {entity_type}: {entity['name']}")
            break
        else:
            print(f"  ✗ Not found in {entity_type}")
    
    if not entity:
        print("  ✗ Entity not found!")
        return False
    
    print(f"  Entity details:")
    print(f"    - ID: {entity['id']}")
    print(f"    - Name: {entity['name']}")
    print(f"    - Resources: {list(entity.get('resources', {}).keys())}")
    
    print("\n3. Testing data resource lookup...")
    resource_files = entity.get('resources', {}).get('data_resources', [])
    print(f"  Resource files: {resource_files}")
    
    for resource_file in resource_files:
        print(f"  Loading {resource_file}...")
        try:
            resource_config = config_loader.load_resource_config('data', resource_file)
            resources = resource_config.get('data_resources', [])
            print(f"    ✓ Loaded {len(resources)} resources")
            for resource in resources:
                print(f"      - {resource['id']}: {resource['name']}")
        except Exception as e:
            print(f"    ✗ Error: {e}")
    
    print("\n4. Testing specific resource lookup...")
    resource = config_loader.get_data_resource(entity_path, 'SoftwarePartNumber')
    if resource:
        print(f"  ✓ SoftwarePartNumber found: {resource['data']['value']}")
    else:
        print(f"  ✗ SoftwarePartNumber not found")
    
    return True

if __name__ == '__main__':
    test_server_config()
