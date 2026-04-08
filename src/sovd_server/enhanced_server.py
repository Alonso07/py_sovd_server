#!/usr/bin/env python3
"""
Enhanced SOVD Server with YAML Configuration Support
Uses YAML configuration files to provide real data for endpoints
"""

import os
import sys
import logging
from typing import Optional
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from datetime import datetime
import json

# Add the current directory to the path first to ensure we get the local config_loader
current_dir = os.path.dirname(__file__)
sys.path.insert(0, current_dir)

try:
    from .config_loader import config_loader
    from . import data_write_runtime
    from . import execution_runtime
    from .fault_builder import (
        build_fault_reference,
        filter_faults_for_query,
        parse_query_mask,
    )
    from .resource_response import (
        data_for_list_view,
        pick_data_resource_response,
        pick_fault_response,
        pick_mode_response,
        pick_operation_response,
    )
    from . import update_runtime
except ImportError:
    from config_loader import config_loader
    import data_write_runtime
    import execution_runtime
    from fault_builder import (
        build_fault_reference,
        filter_faults_for_query,
        parse_query_mask,
    )
    from resource_response import (
        data_for_list_view,
        pick_data_resource_response,
        pick_fault_response,
        pick_mode_response,
        pick_operation_response,
    )
    import update_runtime

# Add the generated server to the path
generated_path = os.path.join(os.path.dirname(__file__), "..", "..", "generated")
sys.path.insert(0, generated_path)
from sovd_server.models.entity_collection import EntityCollection
from sovd_server.models.entity_reference import EntityReference
from sovd_server.models.entity_capabilities import EntityCapabilities
from sovd_server.models.data_resource import DataResource
from sovd_server.models.data_resource_collection import DataResourceCollection
from sovd_server.models.operation import Operation
from sovd_server.models.operation_collection import OperationCollection
from sovd_server.models.fault_collection import FaultCollection
from sovd_server.models.mode import Mode
from sovd_server.models.mode_collection import ModeCollection
from sovd_server.models.version_info import VersionInfo
from sovd_server.models.version import Version

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)


def _base_url() -> str:
    return request.url_root.rstrip("/")


def _norm_entity_path(entity_path: str) -> str:
    if not entity_path.startswith("/"):
        return "/" + entity_path
    return entity_path


def _with_data_override(entity_path: str, resource_data: dict) -> dict:
    """Copy YAML resource dict; apply in-memory data overlay if present."""
    out = dict(resource_data)
    oid = resource_data.get("id")
    if oid is None:
        return out
    ov = data_write_runtime.get_override(entity_path, oid)
    if ov is not None:
        out = {**out, "data": ov}
    return out


def _public_update_package(pkg: dict) -> dict:
    """Drop YAML-only keys not meant for API clients."""
    if not pkg:
        return {}
    skip = {"list_only", "resolves_to"}
    return {k: v for k, v in pkg.items() if k not in skip}


def _update_detail(package_id: str) -> Optional[dict]:
    """Resolved update package for GET /updates/{id} (autonomous -> resolves_to)."""
    pkg = config_loader.get_update_package_by_id(package_id)
    reg = update_runtime.get_registered(package_id)
    if reg is not None:
        merged = dict(reg)
        if pkg:
            merged = {**_public_update_package(pkg), **merged}
        return merged
    if not pkg:
        return None
    if pkg.get("id") == "autonomous" and pkg.get("resolves_to"):
        resolved = config_loader.get_update_package_by_id(pkg["resolves_to"])
        if resolved:
            return _public_update_package(resolved)
    return _public_update_package(pkg)


# Load configuration
config_loader.load_all_configs()
gateway_config = config_loader.gateway_config


@app.route("/version-info", methods=["GET"])
def version_info():
    """Get server version information"""
    try:
        # Create version info from configuration
        version = Version(
            version=gateway_config["gateway"]["version"],
            status="stable",
            accessurl=f"http://{gateway_config['gateway']['network']['host']}:{gateway_config['gateway']['network']['port']}",
        )

        version_info = VersionInfo(versions=[version])

        logger.info("Version info requested")
        return jsonify(version_info.to_dict())
    except Exception as e:
        logger.error(f"Error getting version info: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/areas", methods=["GET"])
def areas():
    """Get areas entities"""
    return get_entities("areas")


@app.route("/components", methods=["GET"])
def components():
    """Get components entities"""
    return get_entities("components")


@app.route("/apps", methods=["GET"])
def apps():
    """Get apps entities"""
    return get_entities("apps")


def get_entities(entity_collection):
    """Get entities for a collection"""
    try:
        # Load entity configuration
        entity_config = config_loader.load_entity_config(entity_collection)
        entities = []

        for entity_data in entity_config.get("entities", []):
            entity_ref = EntityReference(
                id=entity_data["id"],
                name=entity_data["name"],
                href=entity_data["href"],
                tags=entity_data.get("tags", []),
            )
            entities.append(entity_ref)

        collection = EntityCollection(items=entities)

        logger.info(f"Entities requested for collection: {entity_collection}")
        return jsonify(collection.to_dict())
    except Exception as e:
        logger.error(f"Error getting entities for {entity_collection}: {e}")
        return jsonify({"error": str(e)}), 500


# --- Software updates (ISO/DIS 17978-3 §7.18) — must be registered before generic /{entity_path} ---


@app.route("/updates", methods=["GET"])
def updates_list():
    """GET /updates — aggregate package ids from YAML + runtime registrations."""
    try:
        items = list(config_loader.get_all_update_package_ids())
        for rid in update_runtime.list_registered_ids():
            if rid not in items:
                items.append(rid)
        return jsonify({"items": items})
    except Exception as e:
        logger.error(f"Error listing updates: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/updates", methods=["POST"])
def updates_register():
    """POST /updates — register a package (body must include id)."""
    try:
        body = request.get_json(silent=True) or {}
        uid = body.get("id")
        if not uid:
            return jsonify({"error": "id is required"}), 400
        update_runtime.register_package(uid, body)
        loc = f"{_base_url()}/updates/{uid}"
        resp = make_response(jsonify({"id": uid}), 201)
        resp.headers["Location"] = loc
        return resp
    except Exception as e:
        logger.error(f"Error registering update: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/updates/<update_package_id>", methods=["GET"])
def updates_get_detail(update_package_id):
    detail = _update_detail(update_package_id)
    if detail is None:
        return jsonify({"error": "Update package not found"}), 404
    return jsonify(detail)


@app.route("/updates/<update_package_id>", methods=["DELETE"])
def updates_delete(update_package_id):
    pkg = config_loader.get_update_package_by_id(update_package_id)
    if pkg and pkg.get("list_only"):
        return "", 405
    if update_runtime.delete_registered(update_package_id):
        return "", 204
    if pkg:
        return "", 204
    return jsonify({"error": "Update package not found"}), 404


def _updates_accepted_response(update_package_id: str):
    loc = f"{_base_url()}/updates/{update_package_id}/status"
    resp = make_response("", 202)
    resp.headers["Location"] = loc
    return resp


@app.route("/updates/<update_package_id>/automated", methods=["PUT"])
def updates_put_automated(update_package_id):
    if _update_detail(update_package_id) is None:
        return jsonify({"error": "Update package not found"}), 404
    pkg = config_loader.get_update_package_by_id(update_package_id)
    if pkg and not pkg.get("automated", False):
        return (
            jsonify(
                {
                    "error_code": "update-automated-not-supported",
                    "message": "The package cannot be installed automatically",
                }
            ),
            409,
        )
    update_runtime.set_status(
        update_package_id,
        {"phase": "execute", "status": "inProgress", "progress": 0},
    )
    return _updates_accepted_response(update_package_id)


@app.route("/updates/<update_package_id>/prepare", methods=["PUT"])
def updates_put_prepare(update_package_id):
    if _update_detail(update_package_id) is None:
        return jsonify({"error": "Update package not found"}), 404
    update_runtime.set_status(
        update_package_id,
        {"phase": "prepare", "status": "inProgress", "progress": 0},
    )
    return _updates_accepted_response(update_package_id)


@app.route("/updates/<update_package_id>/execute", methods=["PUT"])
def updates_put_execute(update_package_id):
    if _update_detail(update_package_id) is None:
        return jsonify({"error": "Update package not found"}), 404
    update_runtime.set_status(
        update_package_id,
        {"phase": "execute", "status": "inProgress", "progress": 0},
    )
    return _updates_accepted_response(update_package_id)


@app.route("/updates/<update_package_id>/status", methods=["GET"])
def updates_get_status(update_package_id):
    if _update_detail(update_package_id) is None:
        return jsonify({"error": "Update package not found"}), 404
    defaults = {
        "phase": "execute",
        "status": "completed",
        "progress": 100,
    }
    body = update_runtime.merge_status(update_package_id, defaults)
    return jsonify(body)


@app.route("/<path:entity_path>/updates", methods=["GET"])
def entity_updates_list(entity_path):
    """Entity-scoped update id list (ISO allows /updates under an Entity)."""
    try:
        if not entity_path.startswith("/"):
            entity_path = "/" + entity_path
        items = [
            p.get("id")
            for p in config_loader.get_update_packages(entity_path)
            if p.get("id")
        ]
        return jsonify({"items": items})
    except Exception as e:
        logger.error(f"Error listing entity updates: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/<path:entity_path>", methods=["GET"])
def entity_capabilities(entity_path):
    """Get capabilities of an Entity"""

    try:
        # Ensure entity_path starts with /
        if not entity_path.startswith("/"):
            entity_path = "/" + entity_path

        logger.info(f"Entity capabilities route called with path: {entity_path}")
        logger.info(f"Request URL: {request.url}")
        logger.info(f"Request path: {request.path}")
        # Find entity in any collection
        entity = None
        for entity_type in ["areas", "components", "apps"]:
            logger.info(f"  Checking {entity_type}...")
            entity = config_loader.get_entity_by_id(entity_type, entity_path)
            if entity:
                logger.info(f"  Found in {entity_type}: {entity['name']}")
                break
            else:
                logger.info(f"  Not found in {entity_type}")

        if not entity:
            logger.error(f"Entity not found: {entity_path}")
            return jsonify({"error": "Entity not found"}), 404

        # Create capabilities response (include updates URI when configured)
        capabilities = EntityCapabilities(
            id=entity["id"],
            name=entity["name"],
            tags=entity.get("tags", []),
            data=entity["endpoints"]["data_resources"],
            faults=entity["endpoints"]["faults"],
            operations=entity["endpoints"]["operations"],
            configurations=entity["endpoints"]["configurations"],
            modes=entity["endpoints"]["modes"],
        )
        cap_dict = capabilities.to_dict()
        if entity.get("endpoints", {}).get("updates"):
            cap_dict["updates"] = entity["endpoints"]["updates"]

        logger.info(f"Entity capabilities requested for: {entity_path}")
        return jsonify(cap_dict)
    except Exception as e:
        logger.error(f"Error getting entity capabilities for {entity_path}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/<path:entity_path>/data", methods=["GET"])
def data_resources(entity_path):
    """Get data resources for an entity"""
    try:
        # Ensure entity_path starts with /
        if not entity_path.startswith("/"):
            entity_path = "/" + entity_path

        # Find entity and load its data resources
        entity = None
        for entity_type in ["areas", "components", "apps"]:
            entity = config_loader.get_entity_by_id(entity_type, entity_path)
            if entity:
                break

        if not entity:
            return jsonify({"error": "Entity not found"}), 404

        # Load all data resource files for this entity
        data_resources = []
        resource_files = entity.get("resources", {}).get("data_resources", [])

        for resource_file in resource_files:
            resource_config = config_loader.load_resource_config("data", resource_file)
            resources = resource_config.get("data_resources", [])

            for resource_data in resources:
                effective = _with_data_override(entity_path, resource_data)
                data_resource = DataResource(
                    id=effective["id"],
                    name=effective["name"],
                    data=data_for_list_view(effective),
                    _schema=effective.get("schema"),
                    tags=effective.get("tags", []),
                )
                data_resources.append(data_resource)

        collection = DataResourceCollection(items=data_resources)

        logger.info(f"Data resources requested for entity: {entity_path}")
        return jsonify(collection.to_dict())
    except Exception as e:
        logger.error(f"Error getting data resources for {entity_path}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/<path:entity_path>/data/<data_id>", methods=["GET"])
def data_resource(entity_path, data_id):
    """Get a specific data resource"""
    try:
        # Ensure entity_path starts with /
        if not entity_path.startswith("/"):
            entity_path = "/" + entity_path

        resource_data = config_loader.get_data_resource(entity_path, data_id)

        if not resource_data:
            return jsonify({"error": "Data resource not found"}), 404

        effective = _with_data_override(entity_path, resource_data)
        status, body = pick_data_resource_response(entity_path, effective)
        logger.info(
            f"Data resource requested: {entity_path}/{data_id} -> HTTP {status}"
        )
        return jsonify(body), status
    except Exception as e:
        logger.error(f"Error getting data resource {data_id} for {entity_path}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/<path:entity_path>/data/<data_id>", methods=["PUT"])
def update_data_resource(entity_path, data_id):
    """Write data (ISO-style DataResourceWrite → DataResource). See sovd-api.yaml."""
    try:
        entity_path = _norm_entity_path(entity_path)
        resource_data = config_loader.get_data_resource(entity_path, data_id)
        if not resource_data:
            return jsonify({"error": "Data resource not found"}), 404

        payload = request.get_json(silent=True)
        if not isinstance(payload, dict) or "data" not in payload:
            return (
                jsonify(
                    {
                        "error": "Invalid body",
                        "detail": "Request must be JSON with a required 'data' object (DataResourceWrite).",
                    }
                ),
                400,
            )
        incoming = payload["data"]
        if not isinstance(incoming, dict):
            return (
                jsonify(
                    {"error": "Invalid body", "detail": "'data' must be a JSON object."}
                ),
                400,
            )

        base = dict(resource_data.get("data") or {})
        cur = data_write_runtime.get_override(entity_path, data_id)
        if cur is not None:
            base = dict(cur)
        merged = {**base, **incoming}
        data_write_runtime.set_override(entity_path, data_id, merged)

        effective = _with_data_override(entity_path, resource_data)
        dr = DataResource(
            id=effective["id"],
            name=effective.get("name"),
            data=effective.get("data"),
            _schema=effective.get("schema"),
            tags=effective.get("tags", []),
        )
        return jsonify(dr.to_dict()), 200
    except Exception as e:
        logger.error(f"Error updating data resource {data_id} for {entity_path}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/<path:entity_path>/operations", methods=["GET"])
def operations(entity_path):
    """Get operations for an entity"""
    try:
        # Ensure entity_path starts with /
        if not entity_path.startswith("/"):
            entity_path = "/" + entity_path

        # Find entity and load its operations
        entity = None
        for entity_type in ["areas", "components", "apps"]:
            entity = config_loader.get_entity_by_id(entity_type, entity_path)
            if entity:
                break

        if not entity:
            return jsonify({"error": "Entity not found"}), 404

        # Load all operation files for this entity
        operations = []
        operation_files = entity.get("resources", {}).get("operations", [])

        for operation_file in operation_files:
            operation_config = config_loader.load_resource_config(
                "operations", operation_file
            )
            ops = operation_config.get("operations", [])

            for op_data in ops:
                operation = Operation(
                    id=op_data["id"],
                    name=op_data["name"],
                    description=op_data["description"],
                )
                operations.append(operation)

        collection = OperationCollection(items=operations)

        logger.info(f"Operations requested for entity: {entity_path}")
        return jsonify(collection.to_dict())
    except Exception as e:
        logger.error(f"Error getting operations for {entity_path}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route(
    "/<path:entity_path>/operations/<operation_id>/executions/<execution_id>",
    methods=["GET", "DELETE"],
)
def operation_execution_detail(entity_path, operation_id, execution_id):
    """ISO DIS 17978-3 style execution status (GET) and terminate (DELETE → 204)."""
    try:
        entity_path = _norm_entity_path(entity_path)
        op = config_loader.get_operation(entity_path, operation_id)
        if not op:
            return jsonify({"error": "Operation not found"}), 404

        if request.method == "DELETE":
            if not execution_runtime.terminate(entity_path, operation_id, execution_id):
                return jsonify({"error": "Execution not found"}), 404
            return "", 204

        rec = execution_runtime.get_record(entity_path, operation_id, execution_id)
        if not rec:
            return jsonify({"error": "Execution not found"}), 404
        return jsonify(rec), 200
    except Exception as e:
        logger.error(
            f"Error in operation execution {execution_id} for "
            f"{entity_path}/{operation_id}: {e}"
        )
        return jsonify({"error": str(e)}), 500


@app.route(
    "/<path:entity_path>/operations/<operation_id>/executions", methods=["GET", "POST"]
)
def operation_executions(entity_path, operation_id):
    """List executions (GET) or start one (POST → 202 + Location)."""
    try:
        entity_path = _norm_entity_path(entity_path)
        op = config_loader.get_operation(entity_path, operation_id)
        if not op:
            return jsonify({"error": "Operation not found"}), 404

        if request.method == "GET":
            ids = execution_runtime.list_ids(entity_path, operation_id)
            return jsonify({"items": [{"id": i} for i in ids]}), 200

        body = request.get_json(force=True, silent=True) or {}
        if not isinstance(body, dict):
            return jsonify({"error": "Request body must be a JSON object"}), 400
        params = body.get("parameters")
        if params is not None and not isinstance(params, dict):
            return jsonify({"error": "'parameters' must be a JSON object"}), 400

        exec_id = execution_runtime.create(entity_path, operation_id, params)
        rec = execution_runtime.get_record(entity_path, operation_id, exec_id)
        location = (
            f"{_base_url()}{entity_path}/operations/{operation_id}/executions/{exec_id}"
        )
        rv = make_response(jsonify(rec), 202)
        rv.headers["Location"] = location
        logger.info(
            f"Operation execution (ISO path) started: {entity_path}/"
            f"operations/{operation_id}/executions/{exec_id}"
        )
        return rv
    except Exception as e:
        logger.error(
            f"Error in operation executions for {entity_path}/{operation_id}: {e}"
        )
        return jsonify({"error": str(e)}), 500


@app.route("/<path:entity_path>/operations/<operation_id>", methods=["GET"])
def operation(entity_path, operation_id):
    """Get a specific operation"""
    try:
        # Ensure entity_path starts with /
        if not entity_path.startswith("/"):
            entity_path = "/" + entity_path

        operation_data = config_loader.get_operation(entity_path, operation_id)

        if not operation_data:
            return jsonify({"error": "Operation not found"}), 404

        operation = Operation(
            id=operation_data["id"],
            name=operation_data["name"],
            description=operation_data["description"],
        )

        logger.info(f"Operation requested: {entity_path}/{operation_id}")
        return jsonify(operation.to_dict())
    except Exception as e:
        logger.error(f"Error getting operation {operation_id} for {entity_path}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/<path:entity_path>/operations/<operation_id>", methods=["POST"])
def start_operation_execution(entity_path, operation_id):
    """Start execution of an operation"""
    try:
        # Ensure entity_path starts with /
        if not entity_path.startswith("/"):
            entity_path = "/" + entity_path

        operation_data = config_loader.get_operation(entity_path, operation_id)

        if not operation_data:
            return jsonify({"error": "Operation not found"}), 404

        # Get request payload
        request_data = request.get_json() or {}

        # Generate execution ID
        execution_id = f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{operation_id}"

        status, response = pick_operation_response(entity_path, operation_data)
        response = dict(response)
        response["execution_id"] = execution_id
        response["timestamp"] = datetime.now().isoformat() + "Z"

        logger.info(
            f"Operation execution started: {entity_path}/{operation_id} (ID: {execution_id}) -> HTTP {status}"
        )
        return jsonify(response), status
    except Exception as e:
        logger.error(f"Error starting operation {operation_id} for {entity_path}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/<path:entity_path>/faults/<fault_code>", methods=["GET"])
def fault_by_code(entity_path, fault_code):
    """Get a single fault by code (optional ``responses`` round-robin)."""
    try:
        if not entity_path.startswith("/"):
            entity_path = "/" + entity_path
        fault_data = config_loader.get_fault(entity_path, fault_code)
        if not fault_data:
            return jsonify({"error": "Fault not found"}), 404
        status, body = pick_fault_response(entity_path, fault_data)
        return jsonify(body), status
    except Exception as e:
        logger.error(f"Error getting fault {fault_code} for {entity_path}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/<path:entity_path>/faults", methods=["GET"])
def faults(entity_path):
    """Get faults for an entity (optional query: severity, scope, status, mask)."""
    try:
        # Ensure entity_path starts with /
        if not entity_path.startswith("/"):
            entity_path = "/" + entity_path

        faults_data = config_loader.get_faults(entity_path)

        if not faults_data:
            return jsonify({"error": "Entity not found"}), 404

        severity = request.args.get("severity", type=int)
        scope = request.args.get("scope") or None
        if scope is not None and scope.strip() == "":
            scope = None
        status_q = request.args.get("status") or None
        if status_q is not None and status_q.strip() == "":
            status_q = None
        mask = parse_query_mask(request.args.get("mask"))

        filtered = filter_faults_for_query(
            faults_data,
            severity=severity,
            scope=scope,
            status=status_q,
            mask=mask,
        )
        items = [build_fault_reference(fd) for fd in filtered]
        collection = FaultCollection(items=items)

        logger.info(f"Faults requested for entity: {entity_path}")
        return jsonify(collection.to_dict())
    except Exception as e:
        logger.error(f"Error getting faults for {entity_path}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/<path:entity_path>/modes/<mode_id>", methods=["GET"])
def mode_by_id(entity_path, mode_id):
    """Get a single mode by id (optional ``responses`` round-robin)."""
    try:
        if not entity_path.startswith("/"):
            entity_path = "/" + entity_path
        mode_data = config_loader.get_mode(entity_path, mode_id)
        if not mode_data:
            return jsonify({"error": "Mode not found"}), 404
        status, body = pick_mode_response(entity_path, mode_data)
        return jsonify(body), status
    except Exception as e:
        logger.error(f"Error getting mode {mode_id} for {entity_path}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/<path:entity_path>/modes", methods=["GET"])
def modes(entity_path):
    """Get modes for an entity"""
    try:
        # Ensure entity_path starts with /
        if not entity_path.startswith("/"):
            entity_path = "/" + entity_path

        modes_data = config_loader.get_modes(entity_path)

        if not modes_data:
            return jsonify({"error": "Entity not found"}), 404

        modes = []
        for mode_data in modes_data:
            mode = Mode(
                id=mode_data["id"],
                name=mode_data["name"],
                value=mode_data.get("value", mode_data["id"]),
                description=mode_data["description"],
            )
            modes.append(mode)

        collection = ModeCollection(items=modes)

        logger.info(f"Modes requested for entity: {entity_path}")
        return jsonify(collection.to_dict())
    except Exception as e:
        logger.error(f"Error getting modes for {entity_path}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "healthy",
            "message": "SOVD Server is running",
            "version": gateway_config["gateway"]["version"],
            "timestamp": datetime.now().isoformat() + "Z",
        }
    )


if __name__ == "__main__":
    # Get configuration
    host = gateway_config["gateway"]["network"]["host"]
    port = gateway_config["gateway"]["network"]["port"]
    debug = gateway_config["gateway"]["network"]["debug"]

    print("Starting Enhanced SOVD Server...")
    print(f"Configuration loaded from: {config_loader.config_dir}")
    print(f"Available endpoints:")
    print("  GET /version-info - Get server version information")
    print("  GET /{entity-collection} - Get entities (areas, components, apps)")
    print("  GET /{entity-path} - Get entity capabilities")
    print("  GET /{entity-path}/data - Get data resources")
    print("  GET /{entity-path}/data/{data_id} - Get specific data resource")
    print(
        "  PUT /{entity-path}/data/{data_id} - Write data resource (DataResourceWrite)"
    )
    print("  GET /{entity-path}/operations - Get operations")
    print("  GET /{entity-path}/operations/{operation_id} - Get specific operation")
    print(
        "  POST /{entity-path}/operations/{operation_id} - Start operation (legacy path)"
    )
    print(
        "  GET|POST /{entity-path}/operations/{id}/executions - ISO execution list / start"
    )
    print(
        "  GET|DELETE /{entity-path}/operations/{id}/executions/{eid} - Status / stop"
    )
    print("  GET /{entity-path}/faults - Get faults")
    print("  GET /{entity-path}/faults/{fault_code} - Get fault by code")
    print("  GET /{entity-path}/modes - Get modes")
    print("  GET /{entity-path}/modes/{mode_id} - Get mode by id")
    print("  GET /updates - List software update packages")
    print("  GET /{entity-path}/updates - List updates for an entity")
    print("  GET /health - Health check")
    print(f"\nServer running on http://{host}:{port}")

    app.run(host=host, port=port, debug=debug)
