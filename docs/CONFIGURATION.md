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

#### Software updates (`config/resources/updates/*.yaml`)
Defines update packages for **GET /updates**, **GET /updates/{id}**, and related flows (ISO 17978-3 §7.18). Reference files from an entity under `resources.updates`, and add `endpoints.updates` (e.g. `"/engine/ecu/updates"`). Each file lists `update_packages` with `id`, `update_name`, `automated`, `origins`, `size`, `duration`, component URIs, etc. Optional entries: `list_only: true` (e.g. `autonomous`), `resolves_to` (concrete id for the autonomous stub).

#### Multiple HTTP responses (round-robin)

For **data resources** (`GET /{entity}/data/{id}`) and **operations** (`POST /{entity}/operations/{id}`), you can define a `responses` list instead of relying only on the default single 200 response:

- Each item has `status` (HTTP status code) and `body` (JSON object returned to the client).
- On each request, the server **cycles** through the list in order (round-robin) and wraps to the first item after the last.
- Counters are per **entity path + resource id** (so `/engine/ecu` + `RoundRobinDemo` is independent from other entities).

If `responses` is **omitted**, behavior is unchanged: data resources return a single 200 with the usual `id`, `name`, `data`, `schema`, `tags`; operations use `response_success` for a single 200.

For `GET /{entity}/data` (collection), each item still needs a payload for the list: keep a top-level `data` field, or the first response’s `body.data` (or `body`) is used when `data` is missing.

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

### Round-robin responses example

**Data resource** — each `GET` cycles `200 → 503 → 201 → …`:

```yaml
data_resources:
  - id: "MyResource"
    name: "Example"
    data:
      value: "used-in-collection-list"
    responses:
      - status: 200
        body:
          id: "MyResource"
          name: "Example"
          data: { value: "first" }
      - status: 503
        body: { error: "temporary", code: "BUSY" }
      - status: 201
        body:
          id: "MyResource"
          data: { value: "created" }
```

**Operation** — each `POST` cycles through the list; `execution_id` and `timestamp` are still added by the server:

```yaml
operations:
  - id: "MyOp"
    name: "Example"
    execution: { type: "synchronous", timeout: 30 }
    responses:
      - status: 200
        body: { status: "success", message: "A" }
      - status: 409
        body: { status: "conflict", message: "B" }
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
