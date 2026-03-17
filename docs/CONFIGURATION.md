# Configuration Guide

This guide explains how to configure the SOVD server using YAML configuration files based on ISO/DIS 17978-3:2025.

## Overview

The SOVD server uses a hierarchical configuration system that allows you to:
- Configure gateway settings (network, logging)
- Define entities (areas, components, applications)
- Set up resources (data, operations, faults, modes)
- Load configuration from multiple YAML files

## Configuration Structure

### Gateway Configuration (`config/sovd_gateway.yaml`)

The main gateway file references entity and resource configuration files:

```yaml
gateway:
  name: "SOVD Gateway"
  network:
    host: "0.0.0.0"
    port: 8080
  logging:
    level: "INFO"
  entities:
    areas: "entities/areas.yaml"
    components: "entities/components.yaml"
    apps: "entities/apps.yaml"
  resources:
    data: "resources/data/"
    operations: "resources/operations/"
    faults: "resources/faults/"
    modes: "resources/modes/"
```

### Entity Configurations

#### Areas (`config/entities/areas.yaml`)
Define vehicle areas (e.g., engine, transmission, brakes).

#### Components (`config/entities/components.yaml`)
Define vehicle components (ECUs, sensors, cameras) and link them to areas and resource files.

#### Applications (`config/entities/apps.yaml`)
Define diagnostic applications.

### Resource Configurations

#### Data Resources
YAML files defining data resources with schemas and actual values (e.g., SoftwarePartNumber, EngineRPM).

#### Operations
Operation definitions with request/response payloads, execution type, and timeout (e.g., calibratecamera).

#### Faults
Fault definitions with severity and diagnostic information.

#### Modes
Operation modes with capabilities and limitations.

## Configuration Examples

### Data Resource Example
```yaml
data_resources:
  - id: "SoftwarePartNumber"
    name: "Software Part Number"
    description: "Current software part number"
    category: "software"
    data:
      value: "SW-ENG-2024.1.0-REV-A"
      version: "2024.1.0"
```

### Operation Example
```yaml
operations:
  - id: "calibratecamera"
    name: "Calibrate Camera"
    execution:
      type: "asynchronous"
      timeout: 300
    request_payload:
      calibration_type:
        type: "string"
        enum: ["automatic", "manual", "advanced"]
```

## Troubleshooting

1. **Configuration not loading**: Check file paths in `sovd_gateway.yaml` and ensure YAML files exist under `config/`.
2. **Endpoints returning 404**: Verify entity paths in areas/components match the URL paths you request.
3. **Data not found**: Check resource file references in entity configs (e.g., components.yaml) point to existing files.
4. **Server not starting**: Check port availability and that all required config files are present.

### Debug Configuration
Set logging level to DEBUG in `sovd_gateway.yaml`:
```yaml
logging:
  level: "DEBUG"
```

## Best Practices

1. Keep entity and resource files organized by domain.
2. Use meaningful IDs for data resources and operations.
3. Version control all configuration files.
4. Validate paths when adding new entity or resource files.
