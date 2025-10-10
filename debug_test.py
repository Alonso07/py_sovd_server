#!/usr/bin/env python3
"""
Debug test for entity lookup
"""

import sys
import os
from config_loader import config_loader

def debug_entity_lookup():
    """Debug entity lookup functionality"""
    
    print("Debugging Entity Lookup")
    print("=" * 30)
    
    # Load all configs
    config_loader.load_all_configs()
    
    # Test entity lookup for /engine
    print("1. Looking up /engine entity...")
    entity = config_loader.get_entity_by_id('areas', '/engine')
    if entity:
        print(f"   ✓ Found entity: {entity['name']}")
        print(f"   - ID: {entity['id']}")
        print(f"   - Endpoints: {list(entity['endpoints'].keys())}")
    else:
        print("   ✗ Entity not found")
    
    # Test entity lookup for /engine/ecu
    print("\n2. Looking up /engine/ecu entity...")
    entity = config_loader.get_entity_by_id('components', '/engine/ecu')
    if entity:
        print(f"   ✓ Found entity: {entity['name']}")
        print(f"   - ID: {entity['id']}")
        print(f"   - Endpoints: {list(entity['endpoints'].keys())}")
    else:
        print("   ✗ Entity not found")
    
    # Test data resource lookup
    print("\n3. Looking up SoftwarePartNumber data resource...")
    resource = config_loader.get_data_resource('/engine', 'SoftwarePartNumber')
    if resource:
        print(f"   ✓ Found resource: {resource['name']}")
        print(f"   - Data: {resource['data']['value']}")
    else:
        print("   ✗ Resource not found")
    
    # Test operation lookup
    print("\n4. Looking up calibratecamera operation...")
    operation = config_loader.get_operation('/camera/front', 'calibratecamera')
    if operation:
        print(f"   ✓ Found operation: {operation['name']}")
        print(f"   - Type: {operation.get('execution', {}).get('type', 'unknown')}")
    else:
        print("   ✗ Operation not found")

if __name__ == '__main__':
    debug_entity_lookup()
