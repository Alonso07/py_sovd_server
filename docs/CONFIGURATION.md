# Configuration Guide

This guide explains how to configure the SOVD server using YAML configuration files based on ISO/DIS 17978-3:2025.

## Overview

The SOVD server uses a hierarchical configuration system that allows you to:
- Configure gateway settings (network, logging)
- Define entities (areas, components, applications)
- Set up resources (data, operations, faults, modes)
- Load configuration from multiple YAML files

## Configuration Structure

### Gateway Configuration (`src/sovd_server/config/sovd_gateway.yaml`)

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

#### Areas (`src/sovd_server/config/entities/areas.yaml`)
Define vehicle areas (e.g., engine, transmission, brakes).

#### Components (`src/sovd_server/config/entities/components.yaml`)
Define vehicle components (ECUs, sensors, cameras) and link them to areas and resource YAML files.

#### Applications (`src/sovd_server/config/entities/apps.yaml`)
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

#### Software updates (`src/sovd_server/config/resources/updates/*.yaml`)
Defines update packages for **GET /updates**, **GET /updates/{id}**, and related flows (ISO 17978-3 section 7.18). Reference files from an entity under `resources.updates`, and add `endpoints.updates` (for example `"/engine/ecu/updates"`). Each file lists `update_packages` with `id`, `update_name`, `automated`, `origins`, `size`, `duration`, component URIs, and so on. Optional entries: `list_only: true` (for example autonomous stubs), `resolves_to` (concrete id for an autonomous stub).

#### Multiple HTTP responses (round-robin)

For **data resources** (`GET /{entity}/data/{id}`), **operations** (`POST /{entity}/operations/{id}`), **faults** (`GET /{entity}/faults/{fault_code}`), and **modes** (`GET /{entity}/modes/{mode_id}`), you can define a `responses` list instead of relying only on the default single 200 response:

- Each item has `status` (HTTP status code) and `body` (JSON object returned to the client).
- On each request, the server **cycles** through the list in order (round-robin) and wraps to the first item after the last.
- Counters are per **resource kind**, **entity path**, and **resource id** (for example `/engine/ecu` + `ECU-RR` for faults is independent from `/engine/ecu` + `ECU-RR-MODE` for modes).

If `responses` is **omitted**:

- **Data resources** return a single 200 with the usual `id`, `name`, `data`, `schema`, `tags`.
- **Operations** use `response_success` for a single 200 on `POST` (and metadata on `GET` as implemented).
- **Faults** (single GET) return the OpenAPI-style **Fault** JSON (`item`, etc.) built from YAML.
- **Modes** (single GET) return the OpenAPI-style **Mode** JSON built from YAML.

For `GET /{entity}/data` (collection), each item still needs a display payload for the list: keep a top-level `data` field, or the first response’s `body.data` (or `body`) is used when `data` is missing. Fault and mode **collections** still list all entries from YAML fields (`id`, `name`, …); `responses` affect **single-resource GETs** only.

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

**Fault** — each `GET /{entity}/faults/{id}` cycles through the list (body is returned as JSON as-is):

```yaml
faults:
  - id: "DEMO-FAULT"
    name: "Demo"
    description: "Example"
    severity: "warning"
    scope: "system"
    status: "inactive"
    responses:
      - status: 200
        body: { demo: "step-a" }
      - status: 404
        body: { error: "not-found-demo" }
```

**Mode** — each `GET /{entity}/modes/{id}` cycles similarly:

```yaml
modes:
  - id: "DEMO-MODE"
    name: "Demo mode"
    description: "Example"
    responses:
      - status: 200
        body: { demo: "mode-a" }
      - status: 503
        body: { error: "unavailable" }
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
