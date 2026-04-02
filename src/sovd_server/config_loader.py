#!/usr/bin/env python3
"""
SOVD Configuration Loader
Loads and manages YAML configuration files for the SOVD server
"""

import yaml
import os
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path


class SOVDConfigLoader:
    """Loads and manages SOVD configuration from YAML files"""

    def __init__(self, config_dir: str = None):
        if config_dir is None:
            # Default to the config directory relative to this file
            self.config_dir = Path(__file__).parent / "config"
        else:
            self.config_dir = Path(config_dir)
        self.gateway_config = None
        self.entity_configs = {}
        self.resource_configs = {}
        self.logger = logging.getLogger(__name__)

    def load_gateway_config(self) -> Dict[str, Any]:
        """Load the main gateway configuration"""
        config_file = self.config_dir / "sovd_gateway.yaml"

        try:
            with open(config_file, "r") as f:
                self.gateway_config = yaml.safe_load(f)
            self.logger.info(f"Loaded gateway configuration from {config_file}")
            return self.gateway_config
        except FileNotFoundError:
            self.logger.error(f"Gateway configuration file not found: {config_file}")
            raise
        except yaml.YAMLError as e:
            self.logger.error(f"Error parsing gateway configuration: {e}")
            raise

    def load_entity_config(self, entity_type: str) -> Dict[str, Any]:
        """Load entity configuration for a specific type"""
        config_file = self.config_dir / "entities" / f"{entity_type}.yaml"

        try:
            with open(config_file, "r") as f:
                config = yaml.safe_load(f)
            self.entity_configs[entity_type] = config
            self.logger.info(
                f"Loaded {entity_type} entity configuration from {config_file}"
            )
            return config
        except FileNotFoundError:
            self.logger.error(f"Entity configuration file not found: {config_file}")
            raise
        except yaml.YAMLError as e:
            self.logger.error(f"Error parsing {entity_type} entity configuration: {e}")
            raise

    def load_resource_config(
        self, resource_type: str, resource_file: str
    ) -> Dict[str, Any]:
        """Load a specific resource configuration file"""
        # Handle both full paths and just filenames
        if resource_file.startswith("config/"):
            # Strip the 'config/' prefix and resolve relative to config_dir
            relative_path = resource_file.replace("config/", "")
            config_file = self.config_dir / relative_path
        else:
            config_file = self.config_dir / "resources" / resource_type / resource_file

        try:
            with open(config_file, "r") as f:
                config = yaml.safe_load(f)

            # Store in nested structure: resource_configs[resource_type][resource_file]
            if resource_type not in self.resource_configs:
                self.resource_configs[resource_type] = {}
            self.resource_configs[resource_type][resource_file] = config

            self.logger.info(
                f"Loaded {resource_type} resource configuration from {config_file}"
            )
            return config
        except FileNotFoundError:
            self.logger.error(f"Resource configuration file not found: {config_file}")
            raise
        except yaml.YAMLError as e:
            self.logger.error(
                f"Error parsing {resource_type} resource configuration: {e}"
            )
            raise

    def get_entity_by_id(
        self, entity_type: str, entity_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get a specific entity by ID from the loaded configuration"""
        if entity_type not in self.entity_configs:
            self.load_entity_config(entity_type)

        entities = self.entity_configs[entity_type].get("entities", [])
        for entity in entities:
            if entity.get("id") == entity_id:
                return entity
        return None

    def get_data_resource(
        self, entity_path: str, resource_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get a specific data resource by ID for an entity"""
        # Find the entity configuration
        entity = None
        for entity_type in ["areas", "components", "apps"]:
            if entity_type in self.entity_configs:
                entities = self.entity_configs[entity_type].get("entities", [])
                for e in entities:
                    if e.get("id") == entity_path:
                        entity = e
                        break
                if entity:
                    break

        if not entity:
            return None

        # Load data resource configurations
        data_resources = entity.get("resources", {}).get("data_resources", [])
        for resource_file in data_resources:
            if resource_file not in self.resource_configs.get("data", {}):
                self.load_resource_config("data", resource_file)

            resource_config = self.resource_configs["data"][resource_file]
            resources = resource_config.get("data_resources", [])

            for resource in resources:
                if resource.get("id") == resource_id:
                    return resource
        return None

    def get_operation(
        self, entity_path: str, operation_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get a specific operation by ID for an entity"""
        # Find the entity configuration
        entity = None
        for entity_type in ["areas", "components", "apps"]:
            if entity_type in self.entity_configs:
                entities = self.entity_configs[entity_type].get("entities", [])
                for e in entities:
                    if e.get("id") == entity_path:
                        entity = e
                        break
                if entity:
                    break

        if not entity:
            return None

        # Load operation configurations
        operations = entity.get("resources", {}).get("operations", [])
        for operation_file in operations:
            if operation_file not in self.resource_configs.get("operations", {}):
                self.load_resource_config("operations", operation_file)

            operation_config = self.resource_configs["operations"][operation_file]
            ops = operation_config.get("operations", [])

            for operation in ops:
                if operation.get("id") == operation_id:
                    return operation
        return None

    def get_faults(self, entity_path: str) -> List[Dict[str, Any]]:
        """Get all faults for an entity"""
        # Find the entity configuration
        entity = None
        for entity_type in ["areas", "components", "apps"]:
            if entity_type in self.entity_configs:
                entities = self.entity_configs[entity_type].get("entities", [])
                for e in entities:
                    if e.get("id") == entity_path:
                        entity = e
                        break
                if entity:
                    break

        if not entity:
            return []

        # Load fault configurations
        faults = []
        fault_files = entity.get("resources", {}).get("faults", [])
        for fault_file in fault_files:
            if fault_file not in self.resource_configs.get("faults", {}):
                self.load_resource_config("faults", fault_file)

            fault_config = self.resource_configs["faults"][fault_file]
            entity_faults = fault_config.get("faults", [])
            faults.extend(entity_faults)

        return faults

    def get_fault(self, entity_path: str, fault_id: str) -> Optional[Dict[str, Any]]:
        """Get a single fault definition by id for an entity."""
        entity = self._entity_for_path(entity_path)
        if not entity:
            return None
        fault_files = entity.get("resources", {}).get("faults", [])
        for fault_file in fault_files:
            if fault_file not in self.resource_configs.get("faults", {}):
                self.load_resource_config("faults", fault_file)
            fault_config = self.resource_configs["faults"][fault_file]
            for fault in fault_config.get("faults", []):
                if fault.get("id") == fault_id:
                    return fault
        return None

    def get_modes(self, entity_path: str) -> List[Dict[str, Any]]:
        """Get all modes for an entity"""
        # Find the entity configuration
        entity = None
        for entity_type in ["areas", "components", "apps"]:
            if entity_type in self.entity_configs:
                entities = self.entity_configs[entity_type].get("entities", [])
                for e in entities:
                    if e.get("id") == entity_path:
                        entity = e
                        break
                if entity:
                    break

        if not entity:
            return []

        # Load mode configurations
        modes = []
        mode_files = entity.get("resources", {}).get("modes", [])
        for mode_file in mode_files:
            if mode_file not in self.resource_configs.get("modes", {}):
                self.load_resource_config("modes", mode_file)

            mode_config = self.resource_configs["modes"][mode_file]
            entity_modes = mode_config.get("modes", [])
            modes.extend(entity_modes)

        return modes

    def get_mode(self, entity_path: str, mode_id: str) -> Optional[Dict[str, Any]]:
        """Get a single mode definition by id for an entity."""
        entity = self._entity_for_path(entity_path)
        if not entity:
            return None
        mode_files = entity.get("resources", {}).get("modes", [])
        for mode_file in mode_files:
            if mode_file not in self.resource_configs.get("modes", {}):
                self.load_resource_config("modes", mode_file)
            mode_config = self.resource_configs["modes"][mode_file]
            for mode in mode_config.get("modes", []):
                if mode.get("id") == mode_id:
                    return mode
        return None

    def _entity_for_path(self, entity_path: str) -> Optional[Dict[str, Any]]:
        for entity_type in ["areas", "components", "apps"]:
            if entity_type not in self.entity_configs:
                continue
            for e in self.entity_configs[entity_type].get("entities", []):
                if e.get("id") == entity_path:
                    return e
        return None

    def get_update_packages(self, entity_path: str) -> List[Dict[str, Any]]:
        """All update package definitions from YAML for an entity."""
        entity = self._entity_for_path(entity_path)
        if not entity:
            return []
        packages: List[Dict[str, Any]] = []
        for yaml_file in entity.get("resources", {}).get("updates", []):
            if yaml_file not in self.resource_configs.get("updates", {}):
                self.load_resource_config("updates", yaml_file)
            cfg = self.resource_configs["updates"][yaml_file]
            packages.extend(cfg.get("update_packages", []))
        return packages

    def get_update_package_by_id(
        self, package_id: str
    ) -> Optional[Dict[str, Any]]:
        """Return the first YAML update package with this id (any entity)."""
        for entity_type in ["areas", "components", "apps"]:
            if entity_type not in self.entity_configs:
                continue
            for entity in self.entity_configs[entity_type].get("entities", []):
                for pkg in self.get_update_packages(entity["id"]):
                    if pkg.get("id") == package_id:
                        return pkg
        return None

    def get_all_update_package_ids(self) -> List[str]:
        """Ordered unique ids for GET /updates `items` (ISO §7.18.2)."""
        seen = set()
        ordered: List[str] = []
        for entity_type in ["areas", "components", "apps"]:
            if entity_type not in self.entity_configs:
                continue
            for entity in self.entity_configs[entity_type].get("entities", []):
                for pkg in self.get_update_packages(entity["id"]):
                    pid = pkg.get("id")
                    if pid and pid not in seen:
                        seen.add(pid)
                        ordered.append(pid)
        return ordered

    def load_all_configs(self):
        """Load all configuration files"""
        # Load gateway config
        self.load_gateway_config()

        # Load entity configs
        for entity_type in ["areas", "components", "apps"]:
            try:
                self.load_entity_config(entity_type)
            except FileNotFoundError:
                self.logger.warning(f"Entity configuration for {entity_type} not found")

        # Load resource configs as needed
        self.logger.info("Configuration loading completed")


# Global configuration loader instance
config_loader = SOVDConfigLoader()
