from unittest                                                                                   import TestCase
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                           import Type_Safe__List
from osbot_utils.utils.Objects                                                                  import base_classes
from mgraph_ai_service_graph.schemas.batch_execution.Schema__Graph__Batch__Command              import Schema__Graph__Batch__Command
from mgraph_ai_service_graph.schemas.batch_execution.Schema__Graph__Batch__Request              import Schema__Graph__Batch__Request
from mgraph_ai_service_graph.schemas.enums.Enum__Graph__Area                                    import Enum__Graph__Area

class test_Schema__Graph__Batch__Request(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Schema__Graph__Batch__Request() as _:
            assert type(_)              is Schema__Graph__Batch__Request
            assert base_classes(_)      == [Type_Safe, object]
            assert type(_.commands)     is Type_Safe__List                               # Type_Safe__List not raw list
            assert _.stop_on_error      is False                                         # Default value
            assert _.namespace          == "default"                                     # Default value

    def test__with_commands(self):                                                       # Test with command list
        cmd1 = Schema__Graph__Batch__Command(area   = Enum__Graph__Area.GRAPH_CRUD ,
                                             method = "create_graph"               )
        cmd2 = Schema__Graph__Batch__Command(area   = Enum__Graph__Area.GRAPH_EDIT ,
                                             method = "add_node"                   )

        with Schema__Graph__Batch__Request(commands      = [cmd1, cmd2] ,
                                           stop_on_error = True         ,
                                           namespace     = "test-ns"    ) as _:
            assert len(_.commands)   == 2
            assert _.stop_on_error   is True
            assert _.namespace       == "test-ns"

    def test__empty_commands(self):                                                      # Test with empty command list
        with Schema__Graph__Batch__Request(commands=[]) as _:
            assert len(_.commands) == 0
            assert _.commands      == []

    def test__serialization_round_trip(self):                                            # Test JSON round-trip
        cmd = Schema__Graph__Batch__Command(area   = Enum__Graph__Area.GRAPH_QUERY ,
                                            method = "find_nodes_by_type"          )

        with Schema__Graph__Batch__Request(commands      = [cmd]    ,
                                           stop_on_error = True     ,
                                           namespace     = "my-ns"  ) as original:
            json_data = original.json()

            with Schema__Graph__Batch__Request.from_json(json_data) as restored:
                assert len(restored.commands)     == 1
                assert restored.stop_on_error     is True
                assert restored.namespace         == "my-ns"


