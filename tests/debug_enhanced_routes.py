#!/usr/bin/env python3
"""
Debug enhanced server routes
"""

import os
import sys

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from sovd_server.enhanced_server import app

if __name__ == "__main__":
    print("Enhanced server routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule} -> {rule.endpoint}")

    print(f"\nTotal routes: {len(list(app.url_map.iter_rules()))}")

    # Test route matching
    with app.test_client() as client:
        print("\nTesting route matching:")
        response = client.get("/engine/ecu")
        print(f"GET /engine/ecu -> Status: {response.status_code}")
        print(f"Response: {response.get_data(as_text=True)[:200]}")

        response = client.get("/components")
        print(f"GET /components -> Status: {response.status_code}")
        print(f"Response: {response.get_data(as_text=True)[:200]}")

        response = client.get("/health")
        print(f"GET /health -> Status: {response.status_code}")
        print(f"Response: {response.get_data(as_text=True)[:200]}")
