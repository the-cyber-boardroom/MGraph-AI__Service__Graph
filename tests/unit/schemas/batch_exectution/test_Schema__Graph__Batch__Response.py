from unittest                                                                                   import TestCase
from osbot_utils.testing.__                                                                     import __
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                           import Type_Safe__List
from osbot_utils.type_safe.primitives.core.Safe_UInt                                            import Safe_UInt
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                    import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key                import Safe_Str__Key
from osbot_utils.utils.Objects                                                                  import base_classes
from mgraph_ai_service_graph.schemas.batch_execution.Schema__Graph__Batch__Response             import Schema__Graph__Batch__Response

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

            assert _.obj() == __(results        = []   ,
                                 total_commands = 0    ,
                                 stop_on_error  = False,
                                 success        = False,
                                 successful     = 0    ,
                                 failed         = 0    ,
                                 errors         = []   )

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