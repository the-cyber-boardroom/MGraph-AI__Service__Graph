import pytest
from unittest                                                                            import TestCase
from osbot_utils.testing.__                                                              import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                     import Safe_UInt
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text             import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key         import Safe_Str__Key
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                    import Type_Safe__Dict
from osbot_utils.utils.Objects                                                           import base_classes
from mgraph_ai_service_graph.schemas.batch_execution.Schema__Graph__Batch__Command       import Schema__Graph__Batch__Command
from mgraph_ai_service_graph.schemas.batch_execution.Schema__Graph__Batch__Request       import Schema__Graph__Batch__Request
from mgraph_ai_service_graph.schemas.batch_execution.Schema__Graph__Batch__Response      import Schema__Graph__Batch__Response
from mgraph_ai_service_graph.schemas.enums.Enum__Graph__Area                             import Enum__Graph__Area
from mgraph_ai_service_graph.service.batch_execution.Graph__Batch__Executor              import Graph__Batch__Executor
from mgraph_ai_service_graph.service.areas.Area__Graph__CRUD                             import Area__Graph__CRUD
from mgraph_ai_service_graph.service.areas.Area__Graph__Edit                             import Area__Graph__Edit
from mgraph_ai_service_graph.service.areas.Area__Graph__Query                            import Area__Graph__Query


class test_Graph__Batch__Executor(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.executor = Graph__Batch__Executor()

    def test__init__(self):                                                              # Test auto-initialization
        with Graph__Batch__Executor() as _:
            assert type(_)              is Graph__Batch__Executor
            assert base_classes(_)      == [Type_Safe, object]
            assert type(_.area_registry) is Type_Safe__Dict

            # Registry should have entries for all areas
            assert Enum__Graph__Area.GRAPH_CRUD  in _.area_registry
            assert Enum__Graph__Area.GRAPH_EDIT  in _.area_registry
            assert Enum__Graph__Area.GRAPH_QUERY in _.area_registry

    def test__area_registry_initial_state(self):                                         # Test registry is initialized with None values
        with Graph__Batch__Executor() as _:
            # Before set_area_instances, all areas should be None
            assert _.area_registry[Enum__Graph__Area.GRAPH_CRUD]  is None
            assert _.area_registry[Enum__Graph__Area.GRAPH_EDIT]  is None
            assert _.area_registry[Enum__Graph__Area.GRAPH_QUERY] is None

    def test__set_area_instances(self):                                                  # Test dependency injection
        with Graph__Batch__Executor() as _:
            # Create area instances (these need graph_service injected in real use)
            area_crud  = Area__Graph__CRUD()
            area_edit  = Area__Graph__Edit()
            area_query = Area__Graph__Query()
            
            result = _.set_area_instances(crud=area_crud, edit=area_edit, query=area_query)
            
            # Should return self for chaining
            assert result is _
            
            # Registry should now have the instances
            assert _.area_registry[Enum__Graph__Area.GRAPH_CRUD]  is area_crud
            assert _.area_registry[Enum__Graph__Area.GRAPH_EDIT]  is area_edit
            assert _.area_registry[Enum__Graph__Area.GRAPH_QUERY] is area_query

    def test__execute__empty_commands(self):                                             # Test with empty command list
        with Graph__Batch__Executor() as _:
            request = Schema__Graph__Batch__Request(commands=[])
            
            response = _.execute(request)
            
            assert type(response)        is Schema__Graph__Batch__Response
            assert response.total_commands == 0
            assert response.successful     == 0
            assert response.failed         == 0
            assert len(response.errors)    == 0
            assert len(response.results)   == 0

    def test__execute__unknown_area(self):                                               # Test error handling for unknown area
        with Graph__Batch__Executor() as _:
            # Note: We can't easily test invalid enum values, but we can test uninitialized areas
            command = Schema__Graph__Batch__Command(area   = Enum__Graph__Area.GRAPH_CRUD ,
                                                    method = "create_graph"              )
            request = Schema__Graph__Batch__Request(commands=[command])
            
            response = _.execute(request)
            
            # Should fail because area is not initialized
            assert response.total_commands == 1
            assert response.failed         == 1
            assert response.successful     == 0
            assert len(response.errors)    == 1
            assert "Unknown or uninitialized area" in str(response.errors[0])

    def test__execute__stop_on_error_false(self):                                        # Test continues on error when stop_on_error=False
        with Graph__Batch__Executor() as _:
            # Multiple commands, all will fail because areas not initialized
            cmd1 = Schema__Graph__Batch__Command(area   = Enum__Graph__Area.GRAPH_CRUD ,
                                                 method = "create_graph"               )
            cmd2 = Schema__Graph__Batch__Command(area   = Enum__Graph__Area.GRAPH_EDIT ,
                                                 method = "add_node"                   )
            
            request = Schema__Graph__Batch__Request(commands      = [cmd1, cmd2] ,
                                                    stop_on_error = False        )
            
            response = _.execute(request)
            
            # Both commands should be attempted and both should fail
            assert response.total_commands == 2
            assert response.failed         == 2
            assert response.successful     == 0
            assert len(response.errors)    == 2

    def test__execute__stop_on_error_true(self):                                         # Test stops on first error when stop_on_error=True
        with Graph__Batch__Executor() as _:
            # Multiple commands, should stop after first failure
            cmd1 = Schema__Graph__Batch__Command(area   = Enum__Graph__Area.GRAPH_CRUD ,
                                                 method = "create_graph"               )
            cmd2 = Schema__Graph__Batch__Command(area   = Enum__Graph__Area.GRAPH_EDIT ,
                                                 method = "add_node"                   )
            
            request = Schema__Graph__Batch__Request(commands      = [cmd1, cmd2] ,
                                                    stop_on_error = True         )
            
            response = _.execute(request)
            
            # Should stop after first error
            assert response.total_commands == 2
            assert response.failed         == 1                                          # Only first command failed
            assert response.successful     == 0
            assert len(response.errors)    == 1

    def test__validate_command__unknown_area(self):                                      # Test validation with unknown area
        with Graph__Batch__Executor() as _:
            # Area exists in registry but is None
            with pytest.raises(ValueError, match="Unknown area"):
                _.validate_command(area=Enum__Graph__Area.GRAPH_CRUD, method="create_graph")

    def test__validate_command__unknown_method(self):                                    # Test validation with unknown method
        with Graph__Batch__Executor() as _:
            # Set up area instance
            area_crud = Area__Graph__CRUD()
            _.set_area_instances(crud=area_crud, edit=Area__Graph__Edit(), query=Area__Graph__Query())
            
            # Valid area but invalid method
            with pytest.raises(ValueError, match="Unknown method"):
                _.validate_command(area=Enum__Graph__Area.GRAPH_CRUD, method="nonexistent_method")

    def test__validate_command__valid(self):                                             # Test validation with valid command
        with Graph__Batch__Executor() as _:
            # Set up area instance
            area_crud = Area__Graph__CRUD()
            _.set_area_instances(crud=area_crud, edit=Area__Graph__Edit(), query=Area__Graph__Query())
            
            # Valid area and method
            result = _.validate_command(area=Enum__Graph__Area.GRAPH_CRUD, method="create_graph")
            assert result is True

    def test__execute__response_types(self):                                             # Test response has correct types
        with Graph__Batch__Executor() as _:
            request = Schema__Graph__Batch__Request(commands=[])
            
            response = _.execute(request)
            
            assert type(response.total_commands) is Safe_UInt
            assert type(response.successful)     is Safe_UInt
            assert type(response.failed)         is Safe_UInt