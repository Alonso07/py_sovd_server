#!/usr/bin/env python3
"""
Debug Flask routes
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, request

app = Flask(__name__)


@app.route("/<path:entity_path>", methods=["GET"])
def test_route(entity_path):
    return f"Route matched: {entity_path}"


@app.route("/health", methods=["GET"])
def health():
    return "Health check"


if __name__ == "__main__":
    print("Testing Flask routes...")
    print("Available routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule} -> {rule.endpoint}")

    app.run(host="0.0.0.0", port=8085, debug=True)
