from types                                                                                      import NoneType
from unittest                                                                                   import TestCase
from osbot_utils.testing.__                                                                     import __
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                           import Type_Safe__Dict
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                    import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key                import Safe_Str__Key
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Python__Identifier import Safe_Str__Python__Identifier
from osbot_utils.utils.Objects                                                                  import base_classes
from mgraph_ai_service_graph.schemas.batch_execution.Schema__Graph__Batch__Command              import Schema__Graph__Batch__Command
from mgraph_ai_service_graph.schemas.enums.Enum__Graph__Area                                    import Enum__Graph__Area


class test_Schema__Graph__Batch__Command(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Schema__Graph__Batch__Command() as _:
            assert type(_)         is Schema__Graph__Batch__Command
            assert base_classes(_) == [Type_Safe, object]
            assert type(_.area)    is NoneType
            assert type(_.method)  is NoneType
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

            assert _.obj() == __(area    = "graph_crud"         ,
                                 method  = "create_graph"       ,
                                 payload = __(auto_cache='true'))

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

                assert restored.obj () == original.obj ()
                assert restored.json() == original.json()