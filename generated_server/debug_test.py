#!/usr/bin/env python3
"""
Debug test for the enhanced server
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from config_loader import config_loader

# Load configuration
config_loader.load_all_configs()

# Test entity lookup
entity_path = "/engine/ecu"
print(f"Looking up entity: {entity_path}")

for entity_type in ['areas', 'components', 'apps']:
    print(f"  Checking {entity_type}...")
    entity = config_loader.get_entity_by_id(entity_type, entity_path)
    if entity:
        print(f"  Found in {entity_type}: {entity['name']}")
        print(f"  Entity data: {entity}")
        break
    else:
        print(f"  Not found in {entity_type}")

# Test data resource lookup
print(f"\nTesting data resource lookup for {entity_path}...")
entity = config_loader.get_entity_by_id('components', entity_path)
if entity:
    resource_files = entity.get('resources', {}).get('data_resources', [])
    print(f"Resource files: {resource_files}")
    
    for resource_file in resource_files:
        print(f"Loading resource file: {resource_file}")
        resource_config = config_loader.load_resource_config('data', resource_file)
        resources = resource_config.get('data_resources', [])
        print(f"Found {len(resources)} resources in {resource_file}")
        for resource in resources:
            print(f"  - {resource['id']}: {resource['name']}")

# Test specific data resource
print(f"\nTesting SoftwarePartNumber lookup...")
software_part = config_loader.get_data_resource(entity_path, "SoftwarePartNumber")
print(f"SoftwarePartNumber: {software_part}")
