import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from sovd_server.models.configuration import Configuration  # noqa: E501
from sovd_server.models.configuration_write import ConfigurationWrite  # noqa: E501
# from sovd_server.models.configuration_write_multipart import ConfigurationWriteMultipart  # noqa: E501
from sovd_server.models.cyclic_subscription import CyclicSubscription  # noqa: E501
from sovd_server.models.cyclic_subscription_collection import CyclicSubscriptionCollection  # noqa: E501
from sovd_server.models.cyclic_subscription_create import CyclicSubscriptionCreate  # noqa: E501
from sovd_server.models.cyclic_subscription_update import CyclicSubscriptionUpdate  # noqa: E501
from sovd_server.models.data_list import DataList  # noqa: E501
from sovd_server.models.data_list_collection import DataListCollection  # noqa: E501
from sovd_server.models.data_list_create import DataListCreate  # noqa: E501
from sovd_server.models.data_resource import DataResource  # noqa: E501
from sovd_server.models.data_resource_collection import DataResourceCollection  # noqa: E501
from sovd_server.models.data_resource_write import DataResourceWrite  # noqa: E501
from sovd_server.models.entity_capabilities import EntityCapabilities  # noqa: E501
from sovd_server.models.entity_collection import EntityCollection  # noqa: E501
from sovd_server.models.execution_collection import ExecutionCollection  # noqa: E501
from sovd_server.models.fault import Fault  # noqa: E501
from sovd_server.models.fault_collection import FaultCollection  # noqa: E501
from sovd_server.models.mode import Mode  # noqa: E501
from sovd_server.models.mode_collection import ModeCollection  # noqa: E501
from sovd_server.models.mode_set import ModeSet  # noqa: E501
from sovd_server.models.operation import Operation  # noqa: E501
from sovd_server.models.operation_collection import OperationCollection  # noqa: E501
from sovd_server.models.operation_execution import OperationExecution  # noqa: E501
from sovd_server.models.operation_execution_modify import OperationExecutionModify  # noqa: E501
from sovd_server.models.operation_execution_request import OperationExecutionRequest  # noqa: E501
from sovd_server.models.script import Script  # noqa: E501
from sovd_server.models.script_collection import ScriptCollection  # noqa: E501
from sovd_server.models.script_execution import ScriptExecution  # noqa: E501
from sovd_server.models.script_execution_collection import ScriptExecutionCollection  # noqa: E501
from sovd_server.models.script_execution_request import ScriptExecutionRequest  # noqa: E501
from sovd_server.models.trigger import Trigger  # noqa: E501
from sovd_server.models.trigger_collection import TriggerCollection  # noqa: E501
from sovd_server.models.trigger_create import TriggerCreate  # noqa: E501
from sovd_server.models.trigger_update import TriggerUpdate  # noqa: E501
from sovd_server.models.version_info import VersionInfo  # noqa: E501
from sovd_server import util


def create_cyclic_subscription(entity_path, body):  # noqa: E501
    """Issue a new cyclic-subscription

    Creates a new cyclic subscription for data monitoring # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param cyclic_subscription_create: 
    :type cyclic_subscription_create: dict | bytes

    :rtype: Union[CyclicSubscription, Tuple[CyclicSubscription, int], Tuple[CyclicSubscription, int, Dict[str, str]]
    """
    cyclic_subscription_create = body
    if connexion.request.is_json:
        cyclic_subscription_create = CyclicSubscriptionCreate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def create_data_list(entity_path, body):  # noqa: E501
    """Creating a data-list for reading multiple data values at once from an Entity

    Creates a new data-list resource for reading multiple data values # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param data_list_create: 
    :type data_list_create: dict | bytes

    :rtype: Union[DataList, Tuple[DataList, int], Tuple[DataList, int, Dict[str, str]]
    """
    data_list_create = body
    if connexion.request.is_json:
        data_list_create = DataListCreate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def create_trigger(entity_path, body):  # noqa: E501
    """Issue a new trigger

    Creates a new trigger for event-based data reception # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param trigger_create: 
    :type trigger_create: dict | bytes

    :rtype: Union[Trigger, Tuple[Trigger, int], Tuple[Trigger, int, Dict[str, str]]
    """
    trigger_create = body
    if connexion.request.is_json:
        trigger_create = TriggerCreate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_all_faults(entity_path):  # noqa: E501
    """Delete all faults of an Entity

    Deletes all fault entries for an Entity # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def delete_cyclic_subscription(entity_path, subscription_id):  # noqa: E501
    """Delete a cyclic-subscription

    Deletes an existing cyclic subscription # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param subscription_id: Cyclic subscription identifier
    :type subscription_id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def delete_data_list(entity_path, data_list_id):  # noqa: E501
    """Delete an existing data-list

    Deletes an existing data-list resource # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param data_list_id: Data-list identifier
    :type data_list_id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def delete_fault(entity_path, fault_code):  # noqa: E501
    """Delete single fault of an Entity

    Deletes a specific fault entry # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param fault_code: Fault code identifier
    :type fault_code: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def delete_trigger(entity_path, trigger_id):  # noqa: E501
    """Delete a trigger

    Deletes an existing trigger # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param trigger_id: Trigger identifier
    :type trigger_id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_configuration(entity_path, configuration_id, include_schema=None):  # noqa: E501
    """Read a configuration resource

    Provides the current value of a specific configuration resource # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param configuration_id: Configuration resource identifier
    :type configuration_id: str
    :param include_schema: Include JSON schema in response
    :type include_schema: bool

    :rtype: Union[Configuration, Tuple[Configuration, int], Tuple[Configuration, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_cyclic_subscription(entity_path, subscription_id):  # noqa: E501
    """Retrieve details of a cyclic-subscription

    Provides detailed information about a specific cyclic subscription # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param subscription_id: Cyclic subscription identifier
    :type subscription_id: str

    :rtype: Union[CyclicSubscription, Tuple[CyclicSubscription, int], Tuple[CyclicSubscription, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_cyclic_subscription_events(entity_path, subscription_id):  # noqa: E501
    """Retrieve cyclic subscription events

    Establishes a Server-Sent Event stream for cyclic data reception # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param subscription_id: Cyclic subscription identifier
    :type subscription_id: str

    :rtype: Union[str, Tuple[str, int], Tuple[str, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_cyclic_subscriptions(entity_path):  # noqa: E501
    """Query for cyclic-subscriptions from an Entity

    Provides the list of cyclic subscriptions for an Entity # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str

    :rtype: Union[CyclicSubscriptionCollection, Tuple[CyclicSubscriptionCollection, int], Tuple[CyclicSubscriptionCollection, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_data_list(entity_path, data_list_id):  # noqa: E501
    """Read a data-list resource

    Provides the current values of all data resources in the data-list # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param data_list_id: Data-list identifier
    :type data_list_id: str

    :rtype: Union[DataList, Tuple[DataList, int], Tuple[DataList, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_data_lists(entity_path):  # noqa: E501
    """Query for data-lists from an Entity

    Provides the list of all data-list resources available for an Entity # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str

    :rtype: Union[DataListCollection, Tuple[DataListCollection, int], Tuple[DataListCollection, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_data_resource(entity_path, data_id, include_schema=None):  # noqa: E501
    """Read a data resource

    Provides the current value of a specific data resource # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param data_id: Data resource identifier
    :type data_id: str
    :param include_schema: Include JSON schema in response
    :type include_schema: bool

    :rtype: Union[DataResource, Tuple[DataResource, int], Tuple[DataResource, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_data_resources(entity_path, category=None, groups=None, tags=None, include_schema=None):  # noqa: E501
    """Query for data from an Entity

    Provides the list of data resources for an Entity # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param category: Filter data resources by category
    :type category: str
    :param groups: Filter data resources by groups
    :type groups: List[str]
    :param tags: Filter by tags
    :type tags: List[str]
    :param include_schema: Include JSON schema in response
    :type include_schema: bool

    :rtype: Union[DataResourceCollection, Tuple[DataResourceCollection, int], Tuple[DataResourceCollection, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_entities(entity_collection, tags=None):  # noqa: E501
    """Query for Entities from an SOVD server

    Provides the list of contained Entities for each requested Entity collection # noqa: E501

    :param entity_collection: Entity collection type (areas, components, apps)
    :type entity_collection: str
    :param tags: Filter by tags
    :type tags: List[str]

    :rtype: Union[EntityCollection, Tuple[EntityCollection, int], Tuple[EntityCollection, int, Dict[str, str]]
    """
    from sovd_server.models.entity_collection import EntityCollection
    from sovd_server.models.entity_reference import EntityReference
    
    # Create a simple mock response
    entities = []
    if entity_collection == "areas":
        entities = [
            EntityReference(
                id="/engine",
                name="Engine Area",
                href="/engine",
                tags=["diagnostics", "engine"]
            ),
            EntityReference(
                id="/transmission", 
                name="Transmission Area",
                href="/transmission",
                tags=["diagnostics", "transmission"]
            )
        ]
    elif entity_collection == "components":
        entities = [
            EntityReference(
                id="/engine/ecu",
                name="Engine Control Unit",
                href="/engine/ecu",
                tags=["ecu", "engine", "control"]
            )
        ]
    elif entity_collection == "apps":
        entities = [
            EntityReference(
                id="/diagnostics",
                name="Diagnostics App",
                href="/diagnostics",
                tags=["app", "diagnostics"]
            )
        ]
    
    collection = EntityCollection(
        items=entities
    )
    return collection


def get_entity_capabilities(entity_path, include_schema=None):  # noqa: E501
    """Query for capabilities of an Entity

    Returns the capabilities of an Entity # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param include_schema: Include JSON schema in response
    :type include_schema: bool

    :rtype: Union[EntityCapabilities, Tuple[EntityCapabilities, int], Tuple[EntityCapabilities, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_fault(entity_path, fault_code, include_schema=None):  # noqa: E501
    """Read a fault resource

    Provides detailed information about a specific fault # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param fault_code: Fault code identifier
    :type fault_code: str
    :param include_schema: Include JSON schema in response
    :type include_schema: bool

    :rtype: Union[Fault, Tuple[Fault, int], Tuple[Fault, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_faults(entity_path, severity=None, scope=None, status=None, include_schema=None):  # noqa: E501
    """Query for faults from an Entity

    Provides the list of fault entries for an Entity # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param severity: Filter faults by severity level
    :type severity: int
    :param scope: Filter faults by scope
    :type scope: str
    :param status: Filter faults by status
    :type status: str
    :param include_schema: Include JSON schema in response
    :type include_schema: bool

    :rtype: Union[FaultCollection, Tuple[FaultCollection, int], Tuple[FaultCollection, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_mode(entity_path, mode_id, include_schema=None):  # noqa: E501
    """Retrieve details of a mode

    Provides detailed information about a specific mode # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param mode_id: Mode identifier
    :type mode_id: str
    :param include_schema: Include JSON schema in response
    :type include_schema: bool

    :rtype: Union[Mode, Tuple[Mode, int], Tuple[Mode, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_modes(entity_path, include_schema=None):  # noqa: E501
    """Query for modes of an Entity

    Provides the list of modes available for an Entity # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param include_schema: Include JSON schema in response
    :type include_schema: bool

    :rtype: Union[ModeCollection, Tuple[ModeCollection, int], Tuple[ModeCollection, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_operation(entity_path, operation_id, include_schema=None):  # noqa: E501
    """Retrieve details of an operation

    Provides detailed information about a specific operation # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param operation_id: Operation identifier
    :type operation_id: str
    :param include_schema: Include JSON schema in response
    :type include_schema: bool

    :rtype: Union[Operation, Tuple[Operation, int], Tuple[Operation, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_operation_execution_status(entity_path, operation_id, execution_id):  # noqa: E501
    """Read the status of an operation execution

    Provides the current status of a specific operation execution # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param operation_id: Operation identifier
    :type operation_id: str
    :param execution_id: Operation execution identifier
    :type execution_id: str

    :rtype: Union[OperationExecution, Tuple[OperationExecution, int], Tuple[OperationExecution, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_operation_executions(entity_path, operation_id):  # noqa: E501
    """Query for executions of an operation

    Provides the list of executions for a specific operation # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param operation_id: Operation identifier
    :type operation_id: str

    :rtype: Union[ExecutionCollection, Tuple[ExecutionCollection, int], Tuple[ExecutionCollection, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_operations(entity_path, include_schema=None):  # noqa: E501
    """Query for operations from an Entity

    Provides the list of operations available for an Entity # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param include_schema: Include JSON schema in response
    :type include_schema: bool

    :rtype: Union[OperationCollection, Tuple[OperationCollection, int], Tuple[OperationCollection, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_script(entity_path, script_id):  # noqa: E501
    """Retrieve details of a script

    Provides detailed information about a specific script # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param script_id: Script identifier
    :type script_id: str

    :rtype: Union[Script, Tuple[Script, int], Tuple[Script, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_script_execution_status(entity_path, script_id, execution_id):  # noqa: E501
    """Read the status of a script execution

    Provides the current status of a specific script execution # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param script_id: Script identifier
    :type script_id: str
    :param execution_id: Operation execution identifier
    :type execution_id: str

    :rtype: Union[ScriptExecution, Tuple[ScriptExecution, int], Tuple[ScriptExecution, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_script_executions(entity_path, script_id):  # noqa: E501
    """Query for executions of a Script

    Provides the list of executions for a specific script # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param script_id: Script identifier
    :type script_id: str

    :rtype: Union[ScriptExecutionCollection, Tuple[ScriptExecutionCollection, int], Tuple[ScriptExecutionCollection, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_scripts(entity_path):  # noqa: E501
    """Query for scripts from an Entity

    Provides the list of scripts available for an Entity # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str

    :rtype: Union[ScriptCollection, Tuple[ScriptCollection, int], Tuple[ScriptCollection, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_trigger(entity_path, trigger_id):  # noqa: E501
    """Retrieve details of a trigger

    Provides detailed information about a specific trigger # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param trigger_id: Trigger identifier
    :type trigger_id: str

    :rtype: Union[Trigger, Tuple[Trigger, int], Tuple[Trigger, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_trigger_events(entity_path, trigger_id):  # noqa: E501
    """Retrieve trigger events

    Establishes a Server-Sent Event stream for trigger-based data reception # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param trigger_id: Trigger identifier
    :type trigger_id: str

    :rtype: Union[str, Tuple[str, int], Tuple[str, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_triggers(entity_path):  # noqa: E501
    """Query for triggers from an Entity

    Provides the list of triggers for an Entity # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str

    :rtype: Union[TriggerCollection, Tuple[TriggerCollection, int], Tuple[TriggerCollection, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_version_info():  # noqa: E501
    """Read all supported versions of the SOVD server

    Provides information about all supported versions of the SOVD standard # noqa: E501


    :rtype: Union[VersionInfo, Tuple[VersionInfo, int], Tuple[VersionInfo, int, Dict[str, str]]
    """
    from sovd_server.models.version_info import VersionInfo
    from sovd_server.models.version import Version
    
    # Create a simple version info response
    version = Version(
        version="1.0.0",
        status="stable",
        accessurl="http://localhost:8080"
    )
    
    version_info = VersionInfo(
        versions=[version]
    )
    return version_info


def modify_operation_execution(entity_path, operation_id, execution_id, body):  # noqa: E501
    """Support for execute / freeze / reset and custom capabilities

    Modifies the execution of an operation (freeze, reset, etc.) # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param operation_id: Operation identifier
    :type operation_id: str
    :param execution_id: Operation execution identifier
    :type execution_id: str
    :param operation_execution_modify: 
    :type operation_execution_modify: dict | bytes

    :rtype: Union[OperationExecution, Tuple[OperationExecution, int], Tuple[OperationExecution, int, Dict[str, str]]
    """
    operation_execution_modify = body
    if connexion.request.is_json:
        operation_execution_modify = OperationExecutionModify.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def remove_script(entity_path, script_id):  # noqa: E501
    """Remove a script

    Removes a script from an Entity # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param script_id: Script identifier
    :type script_id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def reset_all_configurations(entity_path):  # noqa: E501
    """Reset all configurations to default value

    Resets all configuration resources to their default values # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def reset_configuration(entity_path, configuration_id):  # noqa: E501
    """Reset configuration to default value

    Resets a specific configuration resource to its default value # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param configuration_id: Configuration resource identifier
    :type configuration_id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def set_mode(entity_path, mode_id, body):  # noqa: E501
    """Set mode of an Entity

    Sets the mode of an Entity to a specific value # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param mode_id: Mode identifier
    :type mode_id: str
    :param mode_set: 
    :type mode_set: dict | bytes

    :rtype: Union[Mode, Tuple[Mode, int], Tuple[Mode, int, Dict[str, str]]
    """
    mode_set = body
    if connexion.request.is_json:
        mode_set = ModeSet.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def start_operation_execution(entity_path, operation_id, body):  # noqa: E501
    """Start execution of an operation

    Starts execution of a specific operation # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param operation_id: Operation identifier
    :type operation_id: str
    :param operation_execution_request: 
    :type operation_execution_request: dict | bytes

    :rtype: Union[OperationExecution, Tuple[OperationExecution, int], Tuple[OperationExecution, int, Dict[str, str]]
    """
    operation_execution_request = body
    if connexion.request.is_json:
        operation_execution_request = OperationExecutionRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def start_script_execution(entity_path, script_id, body):  # noqa: E501
    """Start execution of a script

    Starts execution of a specific script # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param script_id: Script identifier
    :type script_id: str
    :param script_execution_request: 
    :type script_execution_request: dict | bytes

    :rtype: Union[ScriptExecution, Tuple[ScriptExecution, int], Tuple[ScriptExecution, int, Dict[str, str]]
    """
    script_execution_request = body
    if connexion.request.is_json:
        script_execution_request = ScriptExecutionRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def terminate_operation_execution(entity_path, operation_id, execution_id):  # noqa: E501
    """Terminate the execution of an operation

    Terminates a running operation execution # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param operation_id: Operation identifier
    :type operation_id: str
    :param execution_id: Operation execution identifier
    :type execution_id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def terminate_script_execution(entity_path, script_id, execution_id):  # noqa: E501
    """Terminate the script execution

    Terminates a running script execution # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param script_id: Script identifier
    :type script_id: str
    :param execution_id: Operation execution identifier
    :type execution_id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def update_configuration(entity_path, configuration_id, body):  # noqa: E501
    """Write a configuration resource

    Updates the value of a specific configuration resource # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param configuration_id: Configuration resource identifier
    :type configuration_id: str
    :param configuration_write: 
    :type configuration_write: dict | bytes

    :rtype: Union[Configuration, Tuple[Configuration, int], Tuple[Configuration, int, Dict[str, str]]
    """
    configuration_write = body
    if connexion.request.is_json:
        configuration_write = ConfigurationWrite.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def update_cyclic_subscription(entity_path, subscription_id, body):  # noqa: E501
    """Update a cyclic-subscription

    Updates an existing cyclic subscription # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param subscription_id: Cyclic subscription identifier
    :type subscription_id: str
    :param cyclic_subscription_update: 
    :type cyclic_subscription_update: dict | bytes

    :rtype: Union[CyclicSubscription, Tuple[CyclicSubscription, int], Tuple[CyclicSubscription, int, Dict[str, str]]
    """
    cyclic_subscription_update = body
    if connexion.request.is_json:
        cyclic_subscription_update = CyclicSubscriptionUpdate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def update_data_resource(entity_path, data_id, body):  # noqa: E501
    """Write a data resource

    Updates the value of a specific data resource # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param data_id: Data resource identifier
    :type data_id: str
    :param data_resource_write: 
    :type data_resource_write: dict | bytes

    :rtype: Union[DataResource, Tuple[DataResource, int], Tuple[DataResource, int, Dict[str, str]]
    """
    data_resource_write = body
    if connexion.request.is_json:
        data_resource_write = DataResourceWrite.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def update_trigger(entity_path, trigger_id, body):  # noqa: E501
    """Update a trigger

    Updates an existing trigger # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param trigger_id: Trigger identifier
    :type trigger_id: str
    :param trigger_update: 
    :type trigger_update: dict | bytes

    :rtype: Union[Trigger, Tuple[Trigger, int], Tuple[Trigger, int, Dict[str, str]]
    """
    trigger_update = body
    if connexion.request.is_json:
        trigger_update = TriggerUpdate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def upload_script(entity_path, script, name=None, description=None):  # noqa: E501
    """Upload a script

    Uploads a new script to an Entity # noqa: E501

    :param entity_path: Path to the Entity
    :type entity_path: str
    :param script: Script file
    :type script: str
    :param name: Script name
    :type name: str
    :param description: Script description
    :type description: str

    :rtype: Union[Script, Tuple[Script, int], Tuple[Script, int, Dict[str, str]]
    """
    return 'do some magic!'
