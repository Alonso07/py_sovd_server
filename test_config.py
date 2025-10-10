#!/usr/bin/env python3
"""
Test SOVD Configuration
Tests the YAML configuration loading and data retrieval
"""

import sys
import os
import json
from config_loader import config_loader

def test_configuration():
    """Test the configuration loading and data retrieval"""
    
    print("Testing SOVD Configuration System")
    print("=" * 40)
    
    try:
        # Test gateway config loading
        print("1. Loading gateway configuration...")
        gateway_config = config_loader.load_gateway_config()
        print(f"   ✓ Gateway config loaded: {gateway_config['gateway']['name']} v{gateway_config['gateway']['version']}")
        
        # Test entity config loading
        print("\n2. Loading entity configurations...")
        for entity_type in ['areas', 'components', 'apps']:
            try:
                entity_config = config_loader.load_entity_config(entity_type)
                entity_count = len(entity_config.get('entities', []))
                print(f"   ✓ {entity_type}: {entity_count} entities")
            except FileNotFoundError:
                print(f"   ✗ {entity_type}: Configuration file not found")
        
        # Test data resource loading
        print("\n3. Testing data resource retrieval...")
        
        # Test engine data resources
        engine_data = config_loader.get_data_resource('/engine', 'SoftwarePartNumber')
        if engine_data:
            print(f"   ✓ Engine SoftwarePartNumber: {engine_data['data']['value']}")
        else:
            print("   ✗ Engine SoftwarePartNumber: Not found")
            
        # Test ECU data resources
        ecu_data = config_loader.get_data_resource('/engine/ecu', 'ECUSerialNumber')
        if ecu_data:
            print(f"   ✓ ECU Serial Number: {ecu_data['data']['value']}")
        else:
            print("   ✗ ECU Serial Number: Not found")
        
        # Test operation loading
        print("\n4. Testing operation retrieval...")
        camera_op = config_loader.get_operation('/camera/front', 'calibratecamera')
        if camera_op:
            print(f"   ✓ Camera Calibration: {camera_op['name']}")
            print(f"     - Type: {camera_op.get('execution', {}).get('type', 'unknown')}")
            print(f"     - Timeout: {camera_op.get('execution', {}).get('timeout', 'unknown')}s")
        else:
            print("   ✗ Camera Calibration: Not found")
        
        # Test fault loading
        print("\n5. Testing fault retrieval...")
        engine_faults = config_loader.get_faults('/engine')
        if engine_faults:
            print(f"   ✓ Engine faults: {len(engine_faults)} found")
            for fault in engine_faults[:2]:  # Show first 2
                print(f"     - {fault['id']}: {fault['name']} (Severity: {fault['severity']})")
        else:
            print("   ✗ Engine faults: Not found")
        
        # Test mode loading
        print("\n6. Testing mode retrieval...")
        engine_modes = config_loader.get_modes('/engine')
        if engine_modes:
            print(f"   ✓ Engine modes: {len(engine_modes)} found")
            for mode in engine_modes:
                print(f"     - {mode['id']}: {mode['name']} (Status: {mode['details']['status']})")
        else:
            print("   ✗ Engine modes: Not found")
        
        print("\n" + "=" * 40)
        print("Configuration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n✗ Configuration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoints():
    """Test API endpoint responses"""
    
    print("\nTesting API Endpoint Responses")
    print("=" * 40)
    
    try:
        # Test entity collection
        print("1. Testing entity collections...")
        for entity_type in ['areas', 'components', 'apps']:
            entity_config = config_loader.load_entity_config(entity_type)
            entities = entity_config.get('entities', [])
            print(f"   ✓ {entity_type}: {len(entities)} entities available")
            for entity in entities[:2]:  # Show first 2
                print(f"     - {entity['id']}: {entity['name']}")
        
        print("\n2. Testing data resource schemas...")
        engine_data = config_loader.get_data_resource('/engine', 'EngineRPM')
        if engine_data and 'schema' in engine_data:
            schema = engine_data['schema']
            print(f"   ✓ EngineRPM schema: {schema['type']} with {len(schema.get('properties', {}))} properties")
        
        print("\n3. Testing operation payloads...")
        camera_op = config_loader.get_operation('/camera/front', 'calibratecamera')
        if camera_op and 'request_payload' in camera_op:
            payload = camera_op['request_payload']
            print(f"   ✓ Camera calibration payload: {len(payload)} parameters")
            for param, details in payload.items():
                print(f"     - {param}: {details.get('type', 'unknown')} (default: {details.get('default', 'none')})")
        
        print("\n" + "=" * 40)
        print("API endpoint test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n✗ API endpoint test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("SOVD Configuration Test Suite")
    print("=" * 50)
    
    # Run configuration tests
    config_success = test_configuration()
    
    # Run API endpoint tests
    api_success = test_api_endpoints()
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"Configuration Loading: {'PASS' if config_success else 'FAIL'}")
    print(f"API Endpoint Testing: {'PASS' if api_success else 'FAIL'}")
    
    if config_success and api_success:
        print("\n🎉 All tests passed! The configuration system is ready to use.")
        print("\nTo start the enhanced server, run:")
        print("  python enhanced_server.py")
        print("  or")
        print("  python run_enhanced_server.py")
    else:
        print("\n❌ Some tests failed. Please check the configuration files.")
        sys.exit(1)
