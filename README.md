# SOVD Server with YAML Configuration

This project implements a Service-Oriented Vehicle Diagnostics (SOVD) server based on ISO/DIS 17978-3:2025 with YAML-based configuration support.

## Features

- **Hierarchical YAML Configuration**: Multi-level configuration system with gateway, entity, and resource configurations
- **Real Data Endpoints**: Actual data for data resources, operations, faults, and modes
- **No Authentication**: Simplified setup without authorization layer for testing
- **RESTful API**: Full SOVD API implementation with proper JSON responses
- **Configurable Entities**: Support for areas, components, and applications
- **Resource Management**: Data resources, operations, faults, modes, and configurations

## Project Structure

```
sovd_server/
├── src/
│   └── sovd_server/               # Main source code
│       ├── config/                # Configuration files
│       │   ├── sovd_gateway.yaml  # Main gateway configuration
│       │   ├── entities/          # Entity configurations
│       │   │   ├── areas.yaml
│       │   │   ├── components.yaml
│       │   │   └── apps.yaml
│       │   └── resources/         # Resource configurations
│       │       ├── data/          # Data resource configs
│       │       ├── operations/    # Operation configs
│       │       ├── faults/        # Fault configs
│       │       └── modes/         # Mode configs
│       ├── enhanced_server.py     # Enhanced server with YAML support
│       ├── config_loader.py       # YAML configuration loader
│       └── run_enhanced_server.py # Server runner script
├── tests/                         # Test files
│   ├── test_config.py             # Configuration testing
│   ├── test_endpoints.py          # Endpoint testing
│   └── debug_*.py                 # Debug utilities
├── generated/                     # Auto-generated SOVD server
├── docs/                          # Documentation
├── requirements.txt               # Dependencies
├── setup.py                       # Package setup
├── pyproject.toml                 # Modern Python project config
└── Makefile                       # Development commands
```

## Configuration System

### Gateway Configuration (`config/sovd_gateway.yaml`)
- Network settings (host, port)
- Logging configuration
- Security settings (disabled for testing)
- Entity and resource file references

### Entity Configurations
- **Areas**: Vehicle areas (engine, transmission, brakes)
- **Components**: Vehicle components (ECU, sensors, cameras)
- **Apps**: Diagnostic applications

### Resource Configurations
- **Data Resources**: Actual data with schemas (e.g., SoftwarePartNumber, EngineRPM)
- **Operations**: Operation definitions with request/response payloads (e.g., calibratecamera)
- **Faults**: Fault definitions with severity and diagnostic information
- **Modes**: Operation modes with capabilities and limitations

## Installation

1. **Set up virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install in development mode**:
   ```bash
   pip install -e .
   ```

4. **Test configuration**:
   ```bash
   python tests/test_config.py
   ```

## Running the Server

### Enhanced Server (Recommended)
```bash
make run-server
# or
python src/sovd_server/run_enhanced_server.py
```

### Simple Server (Basic)
```bash
python generated/simple_server.py
```

## Development Commands

```bash
make help          # Show all available commands
make install-dev   # Install development dependencies
make test          # Run all tests
make lint          # Run linting checks
make format        # Format code with black
make clean         # Clean up build artifacts
```

## API Endpoints

### Basic Endpoints
- `GET /health` - Health check
- `GET /version-info` - Server version information

### Collection Endpoints
- `GET /areas` - List vehicle areas
- `GET /components` - List vehicle components  
- `GET /apps` - List diagnostic applications

### Entity Endpoints
- `GET /{entity-path}` - Get entity capabilities
- `GET /{entity-path}/data` - Get data resources
- `GET /{entity-path}/data/{data-id}` - Get specific data resource
- `GET /{entity-path}/operations` - Get operations
- `GET /{entity-path}/operations/{operation-id}` - Get specific operation
- `POST /{entity-path}/operations/{operation-id}` - Start operation execution
- `GET /{entity-path}/faults` - Get faults
- `GET /{entity-path}/modes` - Get modes

## Example Usage

### Get Engine Data
```bash
curl http://localhost:8080/engine/data
```

### Get Software Part Number
```bash
curl http://localhost:8080/engine/data/SoftwarePartNumber
```

### Start Camera Calibration
```bash
curl -X POST http://localhost:8080/camera/front/operations/calibratecamera \
  -H "Content-Type: application/json" \
  -d '{"calibration_type": "automatic", "target_distance": 10.0}'
```

## Configuration Examples

### Data Resource Example
```yaml
data_resources:
  - id: "SoftwarePartNumber"
    name: "Software Part Number"
    description: "Current software part number installed on the engine ECU"
    category: "software"
    data:
      value: "SW-ENG-2024.1.0-REV-A"
      version: "2024.1.0"
      revision: "A"
```

### Operation Example
```yaml
operations:
  - id: "calibratecamera"
    name: "Calibrate Camera"
    description: "Calibrate the front camera system for optimal performance"
    execution:
      type: "asynchronous"
      timeout: 300
    request_payload:
      calibration_type:
        type: "string"
        enum: ["automatic", "manual", "advanced"]
        default: "automatic"
```

## Testing

### Run All Tests
```bash
make test
```

### Configuration Test
```bash
python tests/test_config.py
```

### Endpoint Test
```bash
python tests/test_endpoints.py
```

## Development

The system is designed to be easily extensible:

1. **Add new entities**: Create new YAML files in `src/sovd_server/config/entities/`
2. **Add new resources**: Create new YAML files in `src/sovd_server/config/resources/`
3. **Modify data**: Update the YAML files with new data
4. **Add endpoints**: Extend the enhanced server with new routes

## Documentation

Full documentation is in the [docs/](docs/INDEX.md) directory: configuration, contributing, testing, deployment, security, and changelog.

## Notes

- The server runs without authentication for testing purposes
- All configuration is loaded from YAML files
- The system uses the auto-generated SOVD models for proper API compliance
- CORS is enabled for web client testing
- Logging is configured through the gateway configuration

## Troubleshooting

1. **Configuration not loading**: Check file paths in YAML files
2. **Endpoints returning 404**: Verify entity paths match configuration
3. **Data not found**: Check resource file references in entity configs
4. **Server not starting**: Check port availability and dependencies
