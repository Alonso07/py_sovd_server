#!/usr/bin/env python3
"""
Test SOVD Server Endpoints
Tests all the enhanced server endpoints
"""

import requests
import json
import sys

def test_endpoint(url, expected_status=200, description=""):
    """Test a single endpoint"""
    try:
        response = requests.get(url, timeout=5)
        print(f"✓ {description or url}")
        print(f"  Status: {response.status_code}")
        if response.status_code == expected_status:
            try:
                data = response.json()
                if isinstance(data, dict) and 'items' in data:
                    print(f"  Items: {len(data['items'])}")
                elif isinstance(data, dict) and 'versions' in data:
                    print(f"  Versions: {len(data['versions'])}")
                else:
                    print(f"  Response: {str(data)[:100]}...")
            except:
                print(f"  Response: {response.text[:100]}...")
        else:
            print(f"  ✗ Expected {expected_status}, got {response.status_code}")
        print()
        return response.status_code == expected_status
    except Exception as e:
        print(f"✗ {description or url}")
        print(f"  Error: {e}")
        print()
        return False

def main():
    """Test all endpoints"""
    base_url = "http://localhost:8080"
    
    print("Testing SOVD Enhanced Server Endpoints")
    print("=" * 50)
    
    # Test basic endpoints
    print("1. Basic Endpoints")
    print("-" * 20)
    test_endpoint(f"{base_url}/health", description="Health Check")
    test_endpoint(f"{base_url}/version-info", description="Version Info")
    
    # Test collection endpoints
    print("2. Collection Endpoints")
    print("-" * 20)
    test_endpoint(f"{base_url}/areas", description="Areas Collection")
    test_endpoint(f"{base_url}/components", description="Components Collection")
    test_endpoint(f"{base_url}/apps", description="Apps Collection")
    
    # Test entity capabilities
    print("3. Entity Capabilities")
    print("-" * 20)
    test_endpoint(f"{base_url}/engine", description="Engine Capabilities")
    test_endpoint(f"{base_url}/engine/ecu", description="ECU Capabilities")
    test_endpoint(f"{base_url}/camera/front", description="Camera Capabilities")
    
    # Test data resources
    print("4. Data Resources")
    print("-" * 20)
    test_endpoint(f"{base_url}/engine/data", description="Engine Data Resources")
    test_endpoint(f"{base_url}/engine/data/SoftwarePartNumber", description="Software Part Number")
    test_endpoint(f"{base_url}/engine/ecu/data", description="ECU Data Resources")
    
    # Test operations
    print("5. Operations")
    print("-" * 20)
    test_endpoint(f"{base_url}/camera/front/operations", description="Camera Operations")
    test_endpoint(f"{base_url}/camera/front/operations/calibratecamera", description="Calibrate Camera")
    
    # Test faults
    print("6. Faults")
    print("-" * 20)
    test_endpoint(f"{base_url}/engine/faults", description="Engine Faults")
    
    # Test modes
    print("7. Modes")
    print("-" * 20)
    test_endpoint(f"{base_url}/engine/modes", description="Engine Modes")
    
    print("=" * 50)
    print("Endpoint testing completed!")

if __name__ == '__main__':
    main()
