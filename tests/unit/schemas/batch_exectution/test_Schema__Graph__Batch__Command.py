from unittest                                                                            import TestCase
from osbot_utils.testing.__                                                              import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                    import Type_Safe__Dict
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                    import Type_Safe__List
from osbot_utils.type_safe.primitives.core.Safe_UInt                                     import Safe_UInt
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text             import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key         import Safe_Str__Key
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Python__Identifier import Safe_Str__Python__Identifier
from osbot_utils.utils.Objects                                                           import base_classes
from mgraph_ai_service_graph.schemas.batch_execution.Schema__Graph__Batch__Command       import Schema__Graph__Batch__Command
from mgraph_ai_service_graph.schemas.batch_execution.Schema__Graph__Batch__Request       import Schema__Graph__Batch__Request
from mgraph_ai_service_graph.schemas.batch_execution.Schema__Graph__Batch__Response      import Schema__Graph__Batch__Response
from mgraph_ai_service_graph.schemas.enums.Enum__Graph__Area                             import Enum__Graph__Area


class test_Schema__Graph__Batch__Command(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Schema__Graph__Batch__Command() as _:
            assert type(_)         is Schema__Graph__Batch__Command
            assert base_classes(_) == [Type_Safe, object]
            assert type(_.area)    is Enum__Graph__Area
            assert type(_.method)  is Safe_Str__Python__Identifier
            assert type(_.payload) is Type_Safe__Dict                                    # Type_Safe__Dict not raw dict

    def test__with_values(self):                                                         # Test with explicit values
        area    = Enum__Graph__Area.GRAPH_CRUD
        method  = Safe_Str__Python__Identifier("create_graph")
        payload = {Safe_Str__Key("auto_cache"): Safe_Str__Text("true")}

        with Schema__Graph__Batch__Command(area    = area    ,
                                           method  = method  ,
                                           payload = payload ) as _:
            assert _.area    == area
            assert _.method  == method
            assert _.payload == payload

            assert _.obj() == __(area    = "graph_crud"                 ,
                                 method  = "create_graph"               ,
                                 payload = {"auto_cache": "true"}       )

    def test__enum_auto_conversion(self):                                                # Test string to enum conversion
        with Schema__Graph__Batch__Command() as _:
            _.area = "graph_crud"                                                        # String should convert to enum
            assert _.area        == Enum__Graph__Area.GRAPH_CRUD
            assert type(_.area)  is Enum__Graph__Area

            _.area = "graph_edit"
            assert _.area        == Enum__Graph__Area.GRAPH_EDIT

    def test__all_enum_areas(self):                                                      # Test all area enum values
        areas = [Enum__Graph__Area.GRAPH_CRUD  ,
                 Enum__Graph__Area.GRAPH_EDIT  ,
                 Enum__Graph__Area.GRAPH_QUERY ,
                 Enum__Graph__Area.GRAPH_CACHE ,
                 Enum__Graph__Area.GRAPH_EXPORT]

        for area in areas:
            with Schema__Graph__Batch__Command(area=area) as _:
                assert _.area == area

    def test__python_identifier_validation(self):                                        # Test method name validation
        with Schema__Graph__Batch__Command() as _:
            _.method = "create_graph"                                                    # Valid Python identifier
            assert _.method == "create_graph"

            _.method = "get_graph_by_id"
            assert _.method == "get_graph_by_id"

    def test__serialization_round_trip(self):                                            # Test JSON round-trip
        payload = {Safe_Str__Key("namespace"): Safe_Str__Text("default")}
        with Schema__Graph__Batch__Command(area    = Enum__Graph__Area.GRAPH_CRUD ,
                                           method  = "create_graph"               ,
                                           payload = payload                      ) as original:
            json_data = original.json()

            with Schema__Graph__Batch__Command.from_json(json_data) as restored:
                assert restored.area   == original.area
                assert restored.method == original.method
                assert type(restored.area)   is Enum__Graph__Area                        # Enum preserved
                assert type(restored.method) is Safe_Str__Python__Identifier


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


class test_Schema__Graph__Batch__Response(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Schema__Graph__Batch__Response() as _:
            assert type(_)               is Schema__Graph__Batch__Response
            assert base_classes(_)       == [Type_Safe, object]
            assert type(_.results)       is Type_Safe__List
            assert type(_.total_commands) is Safe_UInt
            assert type(_.successful)    is Safe_UInt
            assert type(_.failed)        is Safe_UInt
            assert type(_.errors)        is Type_Safe__List

            assert _.obj() == __(results        = []  ,
                                 total_commands = 0   ,
                                 successful     = 0   ,
                                 failed         = 0   ,
                                 errors         = []  )

    def test__with_values(self):                                                         # Test with explicit values
        results = [{Safe_Str__Key("graph_id"): Safe_Str__Text("abc-123")}]
        errors  = [Safe_Str__Text("Error in command 1")]

        with Schema__Graph__Batch__Response(results        = results ,
                                            total_commands = 3       ,
                                            successful     = 2       ,
                                            failed         = 1       ,
                                            errors         = errors  ) as _:
            assert len(_.results)    == 1
            assert _.total_commands  == 3
            assert _.successful      == 2
            assert _.failed          == 1
            assert len(_.errors)     == 1

    def test__success_scenario(self):                                                    # Test all commands successful
        results = [{Safe_Str__Key("id"): Safe_Str__Text("1")} ,
                   {Safe_Str__Key("id"): Safe_Str__Text("2")} ]

        with Schema__Graph__Batch__Response(results        = results ,
                                            total_commands = 2       ,
                                            successful     = 2       ,
                                            failed         = 0       ,
                                            errors         = []      ) as _:
            assert _.total_commands == 2
            assert _.successful     == 2
            assert _.failed         == 0
            assert len(_.errors)    == 0

    def test__partial_failure_scenario(self):                                            # Test some commands failed
        results = [{Safe_Str__Key("id"): Safe_Str__Text("1")}]
        errors  = [Safe_Str__Text("Command 1: Unknown area: invalid_area")]

        with Schema__Graph__Batch__Response(results        = results ,
                                            total_commands = 2       ,
                                            successful     = 1       ,
                                            failed         = 1       ,
                                            errors         = errors  ) as _:
            assert _.total_commands == 2
            assert _.successful     == 1
            assert _.failed         == 1
            assert len(_.errors)    == 1

    def test__serialization_round_trip(self):                                            # Test JSON round-trip
        results = [{Safe_Str__Key("graph_id"): Safe_Str__Text("test-id")}]
        errors  = [Safe_Str__Text("Test error")]

        with Schema__Graph__Batch__Response(results        = results ,
                                            total_commands = 5       ,
                                            successful     = 4       ,
                                            failed         = 1       ,
                                            errors         = errors  ) as original:
            json_data = original.json()

            with Schema__Graph__Batch__Response.from_json(json_data) as restored:
                assert restored.total_commands == 5
                assert restored.successful     == 4
                assert restored.failed         == 1
                assert type(restored.total_commands) is Safe_UInt
                assert type(restored.successful)     is Safe_UInt