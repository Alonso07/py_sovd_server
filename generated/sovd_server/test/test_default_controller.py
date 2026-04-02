import unittest

from flask import json

from sovd_server.models.configuration import Configuration  # noqa: E501
from sovd_server.models.configuration_write import ConfigurationWrite  # noqa: E501
from sovd_server.models.configuration_write_multipart import ConfigurationWriteMultipart  # noqa: E501
from sovd_server.models.cyclic_subscription import CyclicSubscription  # noqa: E501
from sovd_server.models.cyclic_subscription_collection import CyclicSubscriptionCollection  # noqa: E501
from sovd_server.models.cyclic_subscription_create import CyclicSubscriptionCreate  # noqa: E501
from sovd_server.models.cyclic_subscription_update import CyclicSubscriptionUpdate  # noqa: E501
from sovd_server.models.data_error import DataError  # noqa: E501
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
from sovd_server.models.generic_error import GenericError  # noqa: E501
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
from sovd_server.models.update_package import UpdatePackage  # noqa: E501
from sovd_server.models.update_package_id_list import UpdatePackageIdList  # noqa: E501
from sovd_server.models.update_register_response import UpdateRegisterResponse  # noqa: E501
from sovd_server.models.update_status import UpdateStatus  # noqa: E501
from sovd_server.models.version_info import VersionInfo  # noqa: E501
from sovd_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_create_cyclic_subscription(self):
        """Test case for create_cyclic_subscription

        Issue a new cyclic-subscription
        """
        cyclic_subscription_create = {"duration":0,"protocol":"sse","resource":"https://openapi-generator.tech","interval":"medium"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/cyclic-subscriptions'.format(entity_path='entity_path_example'),
            method='POST',
            headers=headers,
            data=json.dumps(cyclic_subscription_create),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_data_list(self):
        """Test case for create_data_list

        Creating a data-list for reading multiple data values at once from an Entity
        """
        data_list_create = {"ids":["ids","ids"]}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/data-lists'.format(entity_path='entity_path_example'),
            method='POST',
            headers=headers,
            data=json.dumps(data_list_create),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_trigger(self):
        """Test case for create_trigger

        Issue a new trigger
        """
        trigger_create = {"protocol":"sse","condition":{"values":["TriggerCondition_values_inner","TriggerCondition_values_inner"],"match":"equals","source":"source"},"resource":"https://openapi-generator.tech","lifetime":0}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/triggers'.format(entity_path='entity_path_example'),
            method='POST',
            headers=headers,
            data=json.dumps(trigger_create),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_all_faults(self):
        """Test case for delete_all_faults

        Delete all faults of an Entity
        """
        headers = { 
        }
        response = self.client.open(
            '/{entity_path}/faults'.format(entity_path='entity_path_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_cyclic_subscription(self):
        """Test case for delete_cyclic_subscription

        Delete a cyclic-subscription
        """
        headers = { 
        }
        response = self.client.open(
            '/{entity_path}/cyclic-subscriptions/{subscription_id}'.format(entity_path='entity_path_example', subscription_id='subscription_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_data_list(self):
        """Test case for delete_data_list

        Delete an existing data-list
        """
        headers = { 
        }
        response = self.client.open(
            '/{entity_path}/data-lists/{data_list_id}'.format(entity_path='entity_path_example', data_list_id='data_list_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_fault(self):
        """Test case for delete_fault

        Delete single fault of an Entity
        """
        headers = { 
        }
        response = self.client.open(
            '/{entity_path}/faults/{fault_code}'.format(entity_path='entity_path_example', fault_code='fault_code_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_trigger(self):
        """Test case for delete_trigger

        Delete a trigger
        """
        headers = { 
        }
        response = self.client.open(
            '/{entity_path}/triggers/{trigger_id}'.format(entity_path='entity_path_example', trigger_id='trigger_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_update_package(self):
        """Test case for delete_update_package

        Delete update package
        """
        headers = { 
        }
        response = self.client.open(
            '/updates/{update_package_id}'.format(update_package_id='update_package_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_configuration(self):
        """Test case for get_configuration

        Read a configuration resource
        """
        query_string = [('include-schema', False)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/configurations/{configuration_id}'.format(entity_path='entity_path_example', configuration_id='configuration_id_example'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_cyclic_subscription(self):
        """Test case for get_cyclic_subscription

        Retrieve details of a cyclic-subscription
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/cyclic-subscriptions/{subscription_id}'.format(entity_path='entity_path_example', subscription_id='subscription_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_cyclic_subscription_events(self):
        """Test case for get_cyclic_subscription_events

        Retrieve cyclic subscription events
        """
        headers = { 
            'Accept': 'text/event-stream',
        }
        response = self.client.open(
            '/{entity_path}/cyclic-subscriptions/{subscription_id}/events'.format(entity_path='entity_path_example', subscription_id='subscription_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_cyclic_subscriptions(self):
        """Test case for get_cyclic_subscriptions

        Query for cyclic-subscriptions from an Entity
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/cyclic-subscriptions'.format(entity_path='entity_path_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_data_list(self):
        """Test case for get_data_list

        Read a data-list resource
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/data-lists/{data_list_id}'.format(entity_path='entity_path_example', data_list_id='data_list_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_data_lists(self):
        """Test case for get_data_lists

        Query for data-lists from an Entity
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/data-lists'.format(entity_path='entity_path_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_data_resource(self):
        """Test case for get_data_resource

        Read a data resource
        """
        query_string = [('include-schema', False)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/data/{data_id}'.format(entity_path='entity_path_example', data_id='data_id_example'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_data_resources(self):
        """Test case for get_data_resources

        Query for data from an Entity
        """
        query_string = [('category', 'category_example'),
                        ('groups', ['groups_example']),
                        ('tags', ['tags_example']),
                        ('include-schema', False)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/data'.format(entity_path='entity_path_example'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_entities(self):
        """Test case for get_entities

        Query for Entities from an SOVD server
        """
        query_string = [('tags', ['tags_example'])]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{entity_collection}'.format(entity_collection='entity_collection_example'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_entity_capabilities(self):
        """Test case for get_entity_capabilities

        Query for capabilities of an Entity
        """
        query_string = [('include-schema', False)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}'.format(entity_path='entity_path_example'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_fault(self):
        """Test case for get_fault

        Read a fault resource
        """
        query_string = [('include-schema', False)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/faults/{fault_code}'.format(entity_path='entity_path_example', fault_code='fault_code_example'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_faults(self):
        """Test case for get_faults

        Query for faults from an Entity
        """
        query_string = [('severity', 56),
                        ('scope', 'scope_example'),
                        ('status', 'status_example'),
                        ('include-schema', False)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/faults'.format(entity_path='entity_path_example'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_mode(self):
        """Test case for get_mode

        Retrieve details of a mode
        """
        query_string = [('include-schema', False)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/modes/{mode_id}'.format(entity_path='entity_path_example', mode_id='mode_id_example'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_modes(self):
        """Test case for get_modes

        Query for modes of an Entity
        """
        query_string = [('include-schema', False)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/modes'.format(entity_path='entity_path_example'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_operation(self):
        """Test case for get_operation

        Retrieve details of an operation
        """
        query_string = [('include-schema', False)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/operations/{operation_id}'.format(entity_path='entity_path_example', operation_id='operation_id_example'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_operation_execution_status(self):
        """Test case for get_operation_execution_status

        Read the status of an operation execution
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/operations/{operation_id}/executions/{execution_id}'.format(entity_path='entity_path_example', operation_id='operation_id_example', execution_id='execution_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_operation_executions(self):
        """Test case for get_operation_executions

        Query for executions of an operation
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/operations/{operation_id}/executions'.format(entity_path='entity_path_example', operation_id='operation_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_operations(self):
        """Test case for get_operations

        Query for operations from an Entity
        """
        query_string = [('include-schema', False)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/operations'.format(entity_path='entity_path_example'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_script(self):
        """Test case for get_script

        Retrieve details of a script
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/scripts/{script_id}'.format(entity_path='entity_path_example', script_id='script_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_script_execution_status(self):
        """Test case for get_script_execution_status

        Read the status of a script execution
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/scripts/{script_id}/executions/{execution_id}'.format(entity_path='entity_path_example', script_id='script_id_example', execution_id='execution_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_script_executions(self):
        """Test case for get_script_executions

        Query for executions of a Script
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/scripts/{script_id}/executions'.format(entity_path='entity_path_example', script_id='script_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_scripts(self):
        """Test case for get_scripts

        Query for scripts from an Entity
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/scripts'.format(entity_path='entity_path_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_trigger(self):
        """Test case for get_trigger

        Retrieve details of a trigger
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/triggers/{trigger_id}'.format(entity_path='entity_path_example', trigger_id='trigger_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_trigger_events(self):
        """Test case for get_trigger_events

        Retrieve trigger events
        """
        headers = { 
            'Accept': 'text/event-stream',
        }
        response = self.client.open(
            '/{entity_path}/triggers/{trigger_id}/events'.format(entity_path='entity_path_example', trigger_id='trigger_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_triggers(self):
        """Test case for get_triggers

        Query for triggers from an Entity
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/triggers'.format(entity_path='entity_path_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_update_package(self):
        """Test case for get_update_package

        Retrieve details of an update package
        """
        query_string = [('include-schema', False)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/updates/{update_package_id}'.format(update_package_id='update_package_id_example'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_update_status(self):
        """Test case for get_update_status

        Read status of an update
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/updates/{update_package_id}/status'.format(update_package_id='update_package_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_updates(self):
        """Test case for get_updates

        Query for software updates
        """
        query_string = [('target-version', 'target_version_example'),
                        ('origin', 'remote')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/updates',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_version_info(self):
        """Test case for get_version_info

        Read all supported versions of the SOVD server
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/version-info',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_modify_operation_execution(self):
        """Test case for modify_operation_execution

        Support for execute / freeze / reset and custom capabilities
        """
        operation_execution_modify = {"capability":"freeze","timeout":0}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/operations/{operation_id}/executions/{execution_id}'.format(entity_path='entity_path_example', operation_id='operation_id_example', execution_id='execution_id_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(operation_execution_modify),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_put_update_automated(self):
        """Test case for put_update_automated

        Automated installation of an update
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/updates/{update_package_id}/automated'.format(update_package_id='update_package_id_example'),
            method='PUT',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_put_update_execute(self):
        """Test case for put_update_execute

        Execute installation of an update
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/updates/{update_package_id}/execute'.format(update_package_id='update_package_id_example'),
            method='PUT',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_put_update_prepare(self):
        """Test case for put_update_prepare

        Prepare installation of an update
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/updates/{update_package_id}/prepare'.format(update_package_id='update_package_id_example'),
            method='PUT',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_register_update(self):
        """Test case for register_update

        Register an update package
        """
        request_body = None
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/updates',
            method='POST',
            headers=headers,
            data=json.dumps(request_body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_remove_script(self):
        """Test case for remove_script

        Remove a script
        """
        headers = { 
        }
        response = self.client.open(
            '/{entity_path}/scripts/{script_id}'.format(entity_path='entity_path_example', script_id='script_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_reset_all_configurations(self):
        """Test case for reset_all_configurations

        Reset all configurations to default value
        """
        headers = { 
        }
        response = self.client.open(
            '/{entity_path}/configurations'.format(entity_path='entity_path_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_reset_configuration(self):
        """Test case for reset_configuration

        Reset configuration to default value
        """
        headers = { 
        }
        response = self.client.open(
            '/{entity_path}/configurations/{configuration_id}'.format(entity_path='entity_path_example', configuration_id='configuration_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_mode(self):
        """Test case for set_mode

        Set mode of an Entity
        """
        mode_set = {"mode_expiration":0,"value":"value"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/modes/{mode_id}'.format(entity_path='entity_path_example', mode_id='mode_id_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(mode_set),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_start_operation_execution(self):
        """Test case for start_operation_execution

        Start execution of an operation
        """
        operation_execution_request = {"parameters":"{}","timeout":0}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/operations/{operation_id}/executions'.format(entity_path='entity_path_example', operation_id='operation_id_example'),
            method='POST',
            headers=headers,
            data=json.dumps(operation_execution_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_start_script_execution(self):
        """Test case for start_script_execution

        Start execution of a script
        """
        script_execution_request = {"parameters":"{}","timeout":0}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/scripts/{script_id}/executions'.format(entity_path='entity_path_example', script_id='script_id_example'),
            method='POST',
            headers=headers,
            data=json.dumps(script_execution_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_terminate_operation_execution(self):
        """Test case for terminate_operation_execution

        Terminate the execution of an operation
        """
        headers = { 
        }
        response = self.client.open(
            '/{entity_path}/operations/{operation_id}/executions/{execution_id}'.format(entity_path='entity_path_example', operation_id='operation_id_example', execution_id='execution_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_terminate_script_execution(self):
        """Test case for terminate_script_execution

        Terminate the script execution
        """
        headers = { 
        }
        response = self.client.open(
            '/{entity_path}/scripts/{script_id}/executions/{execution_id}'.format(entity_path='entity_path_example', script_id='script_id_example', execution_id='execution_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("Connexion does not support multiple consumes. See https://github.com/zalando/connexion/pull/760")
    def test_update_configuration(self):
        """Test case for update_configuration

        Write a configuration resource
        """
        configuration_write = {"data":"{}","signature":"signature"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/configurations/{configuration_id}'.format(entity_path='entity_path_example', configuration_id='configuration_id_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(configuration_write),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_cyclic_subscription(self):
        """Test case for update_cyclic_subscription

        Update a cyclic-subscription
        """
        cyclic_subscription_update = {"duration":0,"interval":"slow"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/cyclic-subscriptions/{subscription_id}'.format(entity_path='entity_path_example', subscription_id='subscription_id_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(cyclic_subscription_update),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_data_resource(self):
        """Test case for update_data_resource

        Write a data resource
        """
        data_resource_write = {"data":"{}"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/data/{data_id}'.format(entity_path='entity_path_example', data_id='data_id_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(data_resource_write),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_trigger(self):
        """Test case for update_trigger

        Update a trigger
        """
        trigger_update = {"condition":{"values":["TriggerCondition_values_inner","TriggerCondition_values_inner"],"match":"equals","source":"source"},"lifetime":0}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/{entity_path}/triggers/{trigger_id}'.format(entity_path='entity_path_example', trigger_id='trigger_id_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(trigger_update),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("multipart/form-data not supported by Connexion")
    def test_upload_script(self):
        """Test case for upload_script

        Upload a script
        """
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'multipart/form-data',
        }
        data = dict(script='/path/to/file',
                    name='name_example',
                    description='description_example')
        response = self.client.open(
            '/{entity_path}/scripts'.format(entity_path='entity_path_example'),
            method='POST',
            headers=headers,
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
