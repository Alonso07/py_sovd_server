#!/usr/bin/env python3
"""
Run Enhanced SOVD Server
Starts the enhanced SOVD server with YAML configuration support
"""

import os
import sys
import subprocess

def main():
    """Main entry point for running the enhanced server"""
    
    # Check if we're in the right directory
    if not os.path.exists('enhanced_server.py'):
        print("Error: enhanced_server.py not found. Please run from the correct directory.")
        sys.exit(1)
    
    # Check if config directory exists
    if not os.path.exists('config'):
        print("Error: config directory not found. Please ensure configuration files are present.")
        sys.exit(1)
    
    # Check if generated server exists
    if not os.path.exists('generated_server'):
        print("Error: generated_server directory not found. Please ensure the generated server is present.")
        sys.exit(1)
    
    print("Starting Enhanced SOVD Server...")
    print("Configuration-based SOVD server with YAML support")
    print("=" * 50)
    
    try:
        # Run the enhanced server
        subprocess.run([sys.executable, 'enhanced_server.py'], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"Error running server: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
