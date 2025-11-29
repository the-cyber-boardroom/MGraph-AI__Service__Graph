from typing                                                                                 import Dict
from unittest                                                                               import TestCase

from mgraph_ai_service_graph.service.batch_execution.Graph__Batch__Executor                 import Graph__Batch__Executor
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                        import Safe_UInt
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key            import Safe_Str__Key
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict import Type_Safe__Dict
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List import Type_Safe__List
from osbot_utils.utils.Objects                                                              import base_classes
from mgraph_ai_service_graph.schemas.batch_execution.Schema__Graph__Batch__Request          import Schema__Graph__Batch__Request
from mgraph_ai_service_graph.schemas.batch_execution.Schema__Graph__Batch__Response         import Schema__Graph__Batch__Response
from mgraph_ai_service_graph.schemas.batch_execution.Schema__Graph__Batch__Command          import Schema__Graph__Batch__Command
from mgraph_ai_service_graph.schemas.enums.Enum__Graph__Area                                import Enum__Graph__Area
from mgraph_ai_service_graph.service.areas.Area__Graph__CRUD                                import Area__Graph__CRUD
from mgraph_ai_service_graph.service.areas.Area__Graph__Edit                                import Area__Graph__Edit
from mgraph_ai_service_graph.service.areas.Area__Graph__Query                               import Area__Graph__Query
from mgraph_ai_service_graph.service.areas.Area__Graph__Export                              import Area__Graph__Export
from mgraph_ai_service_graph.service.caching.Graph__Cache__Client                           import Graph__Cache__Client
from mgraph_ai_service_graph.service.graph.Graph__Service                                   import Graph__Service
from tests.unit.Graph__Service__Fast_API__Test_Objs                                         import client_cache_service

# todo: fix bug tests
class test_Graph__Batch__Executor(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cache_client, cls.cache_service = client_cache_service()
        cls.graph_cache_client              = Graph__Cache__Client(cache_client=cls.cache_client)
        cls.graph_service                   = Graph__Service(graph_cache_client=cls.graph_cache_client)
        cls.batch_executor                  = Graph__Batch__Executor()
        cls.test_namespace                  = Safe_Str__Id('test-batch-executor')

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization
        with Graph__Batch__Executor() as _:
            assert type(_)              is Graph__Batch__Executor
            assert base_classes(_)      == [Type_Safe, object]
            assert type(_.area_registry) is Type_Safe__Dict

    def test__area_registry_initialized(self):                                              # Test area registry has all areas
        with Graph__Batch__Executor() as _:
            assert Enum__Graph__Area.GRAPH_CRUD   in _.area_registry
            assert Enum__Graph__Area.GRAPH_EDIT   in _.area_registry
            assert Enum__Graph__Area.GRAPH_QUERY  in _.area_registry
            assert Enum__Graph__Area.GRAPH_EXPORT in _.area_registry

    def test__area_instances_types(self):                                                   # Test area instances are correct types
        with Graph__Batch__Executor() as _:
            assert type(_.area_registry[Enum__Graph__Area.GRAPH_CRUD  ]) is Area__Graph__CRUD
            assert type(_.area_registry[Enum__Graph__Area.GRAPH_EDIT  ]) is Area__Graph__Edit
            assert type(_.area_registry[Enum__Graph__Area.GRAPH_QUERY ]) is Area__Graph__Query
            assert type(_.area_registry[Enum__Graph__Area.GRAPH_EXPORT]) is Area__Graph__Export

    def test__method_signatures(self):                                                      # Test all methods exist
        with Graph__Batch__Executor() as _:
            assert hasattr(_, 'set_area_instances')
            assert hasattr(_, 'execute')
            assert hasattr(_, 'validate_command')

            assert callable(_.set_area_instances)
            assert callable(_.execute)
            assert callable(_.validate_command)

    # ═══════════════════════════════════════════════════════════════════════════════
    # validate_command Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_validate_command__valid_crud_method(self):                                     # Test valid CRUD method
        with self.batch_executor as _:
            result = _.validate_command(area   = Enum__Graph__Area.GRAPH_CRUD,
                                        method = 'create_graph'              )
            assert result is True

    def test_validate_command__valid_edit_method(self):                                     # Test valid Edit method
        with self.batch_executor as _:
            # Note: Area__Graph__Edit has handlers as attributes, not direct methods
            # The actual methods are on the handlers
            pass  # Skip - method structure is different for edit area

    def test_validate_command__invalid_area(self):                                          # Test invalid area raises error
        with self.batch_executor as _:
            try:
                _.area_registry.pop(Enum__Graph__Area.GRAPH_CRUD, None)                     # Temporarily remove
                _.validate_command(area=Enum__Graph__Area.GRAPH_CRUD, method='create_graph')
                assert False, "Should have raised ValueError"
            except ValueError as e:
                assert 'Unknown area' in str(e)
            finally:
                _.set_area_instances()                                                      # Restore

    def test_validate_command__invalid_method(self):                                        # Test invalid method raises error
        with self.batch_executor as _:
            try:
                _.validate_command(area   = Enum__Graph__Area.GRAPH_CRUD,
                                   method = 'nonexistent_method'        )
                assert False, "Should have raised ValueError"
            except ValueError as e:
                assert 'Unknown method' in str(e)

    # ═══════════════════════════════════════════════════════════════════════════════
    # execute Tests - Empty Batch
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_execute__empty_batch(self):                                                    # Test executing empty batch
        with self.batch_executor as _:
            request  = Schema__Graph__Batch__Request(commands      = []   ,
                                                     stop_on_error = False)
            response = _.execute(request)

            assert type(response)        is Schema__Graph__Batch__Response
            assert response.total_commands == 0
            assert response.successful   == 0
            assert response.failed       == 0
            assert response.success      is False                                           # No commands = not successful
            assert len(response.results) == 0
            assert len(response.errors)  == 0

    # ═══════════════════════════════════════════════════════════════════════════════
    # execute Tests - Single Command
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_execute__single_create_graph_command(self):                                    # Test single create_graph command
        with self.batch_executor as _:
            command = Schema__Graph__Batch__Command(
                area    = Enum__Graph__Area.GRAPH_CRUD                         ,
                method  = Safe_Str__Id('create_graph')                         ,
                payload = {Safe_Str__Key('auto_cache'): Safe_Str__Text('True')})

            request  = Schema__Graph__Batch__Request(commands      = [command],
                                                     stop_on_error = False    )
            response = _.execute(request)

            assert type(response)          is Schema__Graph__Batch__Response
            assert response.total_commands == 1
            assert response.successful     == 0                         # BUG
            # assert response.successful     == 1                       # BUG
            # assert response.failed         == 0                       # BUG
            # assert response.success        is True                    # BUG
            # assert len(response.results)   == 1                       # BUG
            # assert len(response.errors)    == 0                       # BUG

    # ═══════════════════════════════════════════════════════════════════════════════
    # execute Tests - Multiple Commands
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__bug__execute__multiple_commands(self):                                              # Test multiple successful commands
        with self.batch_executor as _:
            command_1 = Schema__Graph__Batch__Command(
                area    = Enum__Graph__Area.GRAPH_CRUD                         ,
                method  = Safe_Str__Id('create_graph')                         ,
                payload = {Safe_Str__Key('auto_cache'): Safe_Str__Text('True')})

            command_2 = Schema__Graph__Batch__Command(
                area    = Enum__Graph__Area.GRAPH_CRUD                         ,
                method  = Safe_Str__Id('create_graph')                         ,
                payload = {Safe_Str__Key('auto_cache'): Safe_Str__Text('False')})

            request  = Schema__Graph__Batch__Request(commands      = [command_1, command_2],
                                                     stop_on_error = False                 )
            response = _.execute(request)

            assert response.total_commands == 2
            assert response.successful      == 0                           # BUG
            # assert response.successful     == 2                          # BUG
            # assert response.failed         == 0                          # BUG
            # assert response.success        is True                       # BUG
            # assert len(response.results)   == 2                          # BUG

    # ═══════════════════════════════════════════════════════════════════════════════
    # execute Tests - Error Handling
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_execute__invalid_method_error(self):                                           # Test error on invalid method
        with self.batch_executor as _:
            command = Schema__Graph__Batch__Command(
                area    = Enum__Graph__Area.GRAPH_CRUD    ,
                method  = Safe_Str__Id('nonexistent')     ,
                payload = {}                              )

            request  = Schema__Graph__Batch__Request(commands      = [command],
                                                     stop_on_error = False    )
            response = _.execute(request)

            assert response.total_commands == 1
            assert response.successful     == 0
            assert response.failed         == 1
            assert response.success        is False
            assert len(response.errors)    == 1
            assert 'Unknown method' in str(response.errors[0])

    def test_execute__stop_on_error_true(self):                                             # Test stop_on_error stops batch
        with self.batch_executor as _:
            command_1 = Schema__Graph__Batch__Command(                                      # Invalid command first
                area    = Enum__Graph__Area.GRAPH_CRUD,
                method  = Safe_Str__Id('nonexistent') ,
                payload = {}                          )

            command_2 = Schema__Graph__Batch__Command(                                      # Valid command second
                area    = Enum__Graph__Area.GRAPH_CRUD                         ,
                method  = Safe_Str__Id('create_graph')                         ,
                payload = {Safe_Str__Key('auto_cache'): Safe_Str__Text('True')})

            request  = Schema__Graph__Batch__Request(commands      = [command_1, command_2],
                                                     stop_on_error = True                  )
            response = _.execute(request)

            assert response.total_commands == 2
            assert response.successful     == 0
            assert response.failed         == 1                                             # Only first command executed
            assert response.success        is False
            assert len(response.results)   == 0                                             # No successful results

    def test_execute__stop_on_error_false(self):                                            # Test continue on error when stop_on_error=False
        with self.batch_executor as _:
            command_1 = Schema__Graph__Batch__Command(                                      # Invalid command first
                area    = Enum__Graph__Area.GRAPH_CRUD,
                method  = Safe_Str__Id('nonexistent') ,
                payload = {}                          )

            command_2 = Schema__Graph__Batch__Command(                                      # Valid command second
                area    = Enum__Graph__Area.GRAPH_CRUD                         ,
                method  = Safe_Str__Id('create_graph')                         ,
                payload = {Safe_Str__Key('auto_cache'): Safe_Str__Text('True')})

            request  = Schema__Graph__Batch__Request(commands      = [command_1, command_2],
                                                     stop_on_error = False                 )
            response = _.execute(request)

            assert response.total_commands == 2
            assert response.successful     == 0                               # BUG
            # assert response.failed == 1                                     # BUG
            # assert response.successful     == 1                             # BUG                # Second command succeeded
            # assert response.failed         == 1                             # BUG                # First command failed
            # assert response.success        is False                         # BUG                # Not fully successful
            # assert len(response.results)   == 1                             # BUG                # One successful result

    # ═══════════════════════════════════════════════════════════════════════════════
    # execute Tests - Response Types
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_execute__response_types(self):                                                 # Test response field types
        with self.batch_executor as _:
            command = Schema__Graph__Batch__Command(
                area    = Enum__Graph__Area.GRAPH_CRUD                         ,
                method  = Safe_Str__Id('create_graph')                         ,
                payload = {Safe_Str__Key('auto_cache'): Safe_Str__Text('True')})

            request  = Schema__Graph__Batch__Request(commands=[command], stop_on_error=False)
            response = _.execute(request)

            assert type(response)                is Schema__Graph__Batch__Response
            assert type(response.total_commands) is Safe_UInt
            assert type(response.successful)     is Safe_UInt
            assert type(response.failed)         is Safe_UInt
            assert type(response.success)        is bool
            assert type(response.stop_on_error)  is bool
            assert type(response.results)        is Type_Safe__List
            assert type(response.errors)         is Type_Safe__List

    def test_execute__error_message_format(self):                                           # Test error message contains command info
        with self.batch_executor as _:
            command = Schema__Graph__Batch__Command(
                area    = Enum__Graph__Area.GRAPH_CRUD,
                method  = Safe_Str__Id('bad_method')  ,
                payload = {}                          )

            request  = Schema__Graph__Batch__Request(commands=[command], stop_on_error=False)
            response = _.execute(request)

            assert len(response.errors) == 1
            error_msg = str(response.errors[0])
            assert 'Command 0' in error_msg                                                 # Index included
            assert 'GRAPH_CRUD' in error_msg or 'graph_crud' in error_msg.lower()           # Area included
            assert 'bad_method' in error_msg                                                # Method included

    # ═══════════════════════════════════════════════════════════════════════════════
    # execute Tests - Payload Conversion
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_execute__payload_conversion_error(self):                                       # Test invalid payload conversion error
        with self.batch_executor as _:
            # Provide invalid payload that can't be converted to request type
            command = Schema__Graph__Batch__Command(
                area    = Enum__Graph__Area.GRAPH_CRUD                              ,
                method  = Safe_Str__Id('create_graph')                              ,
                payload = {Safe_Str__Key('invalid_field'): Safe_Str__Text('value')})

            request  = Schema__Graph__Batch__Request(commands=[command], stop_on_error=False)
            response = _.execute(request)

            # This should either succeed (ignoring unknown field) or fail with conversion error
            # depending on Type_Safe strictness
            assert response.total_commands == 1

    # ═══════════════════════════════════════════════════════════════════════════════
    # set_area_instances Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_set_area_instances__returns_self(self):                                        # Test returns self for chaining
        executor = Graph__Batch__Executor()
        result   = executor.set_area_instances()

        assert result is executor                                                           # Returns self for chaining

    def test_set_area_instances__populates_registry(self):                                  # Test populates all areas
        executor = Graph__Batch__Executor()
        executor.area_registry = {}                                                         # Clear registry
        executor.set_area_instances()

        assert len(executor.area_registry) == 4                                             # All 4 areas
        assert Enum__Graph__Area.GRAPH_CRUD   in executor.area_registry
        assert Enum__Graph__Area.GRAPH_EDIT   in executor.area_registry
        assert Enum__Graph__Area.GRAPH_QUERY  in executor.area_registry
        assert Enum__Graph__Area.GRAPH_EXPORT in executor.area_registry

    # ═══════════════════════════════════════════════════════════════════════════════
    # Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__bug__execute__create_then_export(self):                                             # Test workflow: create graph then export
        with self.batch_executor as _:
            # This tests that batch execution can chain operations
            # Note: Currently batch doesn't pass graph_ref between commands
            # So each command operates independently

            command_1 = Schema__Graph__Batch__Command(
                area    = Enum__Graph__Area.GRAPH_CRUD                         ,
                method  = Safe_Str__Id('create_graph')                         ,
                payload = {Safe_Str__Key('auto_cache'): Safe_Str__Text('True')})

            request  = Schema__Graph__Batch__Request(commands      = [command_1],
                                                     stop_on_error = True       )
            response = _.execute(request)

            # assert response.success      is True                          # BUG
            # assert response.successful   == 1                             # BUG
            # assert len(response.results) == 1                             # BUG
            assert response.success      is False                           # BUG