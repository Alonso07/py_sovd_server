#!/usr/bin/env python3
"""
Enhanced SOVD Server with YAML Configuration Support
Uses YAML configuration files to provide real data for endpoints
"""

import os
import sys
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import json

# Add the current directory to the path first to ensure we get the local config_loader
current_dir = os.path.dirname(__file__)
sys.path.insert(0, current_dir)

try:
    from .config_loader import config_loader
except ImportError:
    from config_loader import config_loader

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
from sovd_server.models.fault import Fault
from sovd_server.models.fault_collection import FaultCollection
from sovd_server.models.fault_reference import FaultReference
from sovd_server.models.fault_status import FaultStatus
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

        # Create capabilities response
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

        logger.info(f"Entity capabilities requested for: {entity_path}")
        return jsonify(capabilities.to_dict())
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
                data_resource = DataResource(
                    id=resource_data["id"],
                    name=resource_data["name"],
                    data=resource_data["data"],
                    _schema=resource_data.get("schema"),
                    tags=resource_data.get("tags", []),
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

        data_resource = DataResource(
            id=resource_data["id"],
            name=resource_data["name"],
            data=resource_data["data"],
            _schema=resource_data.get("schema"),
            tags=resource_data.get("tags", []),
        )

        logger.info(f"Data resource requested: {entity_path}/{data_id}")
        return jsonify(data_resource.to_dict())
    except Exception as e:
        logger.error(f"Error getting data resource {data_id} for {entity_path}: {e}")
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

        # Return appropriate response based on operation type
        if operation_data.get("execution", {}).get("type") == "asynchronous":
            response = operation_data.get("response_success", {}).copy()
            response["execution_id"] = execution_id
            response["timestamp"] = datetime.now().isoformat() + "Z"
        else:
            response = operation_data.get("response_success", {}).copy()
            response["execution_id"] = execution_id
            response["timestamp"] = datetime.now().isoformat() + "Z"

        logger.info(
            f"Operation execution started: {entity_path}/{operation_id} (ID: {execution_id})"
        )
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error starting operation {operation_id} for {entity_path}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/<path:entity_path>/faults", methods=["GET"])
def faults(entity_path):
    """Get faults for an entity"""
    try:
        # Ensure entity_path starts with /
        if not entity_path.startswith("/"):
            entity_path = "/" + entity_path

        faults_data = config_loader.get_faults(entity_path)

        if not faults_data:
            return jsonify({"error": "Entity not found"}), 404

        faults = []
        for fault_data in faults_data:
            # Create FaultStatus object with default values
            fault_status = FaultStatus(
                test_failed="false",
                confirmed_dtc="false",
                aggregated_status=fault_data.get("status", "inactive"),
            )

            # Create FaultReference object
            fault_ref = FaultReference(
                code=fault_data["id"],
                scope=fault_data.get("scope", "system"),
                display_code=fault_data["id"],
                fault_name=fault_data["name"],
                severity=fault_data.get("severity", "warning"),
                status=fault_status,
            )

            # Create Fault object with the reference
            fault = Fault(item=fault_ref)
            faults.append(fault)

        collection = FaultCollection(items=faults)

        logger.info(f"Faults requested for entity: {entity_path}")
        return jsonify(collection.to_dict())
    except Exception as e:
        logger.error(f"Error getting faults for {entity_path}: {e}")
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
    print("  GET /{entity-path}/operations - Get operations")
    print("  GET /{entity-path}/operations/{operation_id} - Get specific operation")
    print("  POST /{entity-path}/operations/{operation_id} - Start operation execution")
    print("  GET /{entity-path}/faults - Get faults")
    print("  GET /{entity-path}/modes - Get modes")
    print("  GET /health - Health check")
    print(f"\nServer running on http://{host}:{port}")

    app.run(host=host, port=port, debug=debug)
