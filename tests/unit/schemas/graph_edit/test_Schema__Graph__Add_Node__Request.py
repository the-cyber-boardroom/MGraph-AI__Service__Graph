from unittest                                                                            import TestCase
from osbot_utils.testing.__                                                              import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                         import Obj_Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                    import Type_Safe__Dict
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id          import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key         import Safe_Str__Key
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text             import Safe_Str__Text
from osbot_utils.utils.Objects                                                           import base_classes
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Node__Request         import Schema__Graph__Add_Node__Request


class test_Schema__Graph__Add_Node__Request(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Schema__Graph__Add_Node__Request() as _:
            assert type(_)            is Schema__Graph__Add_Node__Request
            assert base_classes(_)    == [Type_Safe, object]
            assert type(_.graph_id)   is Obj_Id
            assert type(_.node_type)  is Safe_Str__Id
            assert type(_.node_data)  is Type_Safe__Dict                                 # Type_Safe__Dict not raw dict
            assert _.auto_cache       is True                                            # Default value

            assert _.obj() == __(graph_id   = _.graph_id  ,
                                 node_type  = _.node_type ,
                                 node_data  = __()        ,
                                 auto_cache = True        )

    def test__with_values(self):                                                         # Test with explicit values
        graph_id  = Obj_Id()
        node_type = Safe_Str__Id("Person")
        node_data = {Safe_Str__Key("name"): Safe_Str__Text("Alice")}

        with Schema__Graph__Add_Node__Request(graph_id   = graph_id   ,
                                              node_type  = node_type  ,
                                              node_data  = node_data  ,
                                              auto_cache = False      ) as _:
            assert _.graph_id   == graph_id
            assert _.node_type  == node_type
            assert _.node_data  == node_data
            assert _.auto_cache is False

    def test__type_safe_dict_enforcement(self):                                          # Test Dict uses type-safe keys/values
        with Schema__Graph__Add_Node__Request() as _:
            _.node_data = {Safe_Str__Key("key1"): Safe_Str__Text("value1"),
                           "key2": "value2"}                                            # Should accept type-safe dict
            assert len(_.node_data) == 2
            assert _.obj() == __(auto_cache = True,
                                 graph_id   = __SKIP__,
                                 node_type  = '',
                                 node_data  = __(key1='value1', key2='value2'))

    def test__serialization_round_trip(self):                                            # Test JSON round-trip
        node_data = {Safe_Str__Key("name"): Safe_Str__Text("Bob")}
        with Schema__Graph__Add_Node__Request(node_type  = "Entity"   ,
                                              node_data  = node_data  ,
                                              auto_cache = False      ) as original:
            json_data = original.json()

            with Schema__Graph__Add_Node__Request.from_json(json_data) as restored:
                assert type(restored.graph_id)  is Obj_Id
                assert type(restored.node_type) is Safe_Str__Id
