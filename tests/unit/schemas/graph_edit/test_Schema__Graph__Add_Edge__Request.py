from types import NoneType
from unittest                                                                            import TestCase
from osbot_utils.testing.__                                                              import __
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                    import Type_Safe__Dict
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                         import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id          import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key         import Safe_Str__Key
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text             import Safe_Str__Text
from osbot_utils.utils.Objects                                                           import base_classes
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Add_Edge__Request   import Schema__Graph__Add_Edge__Request


class test_Schema__Graph__Add_Edge__Request(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Schema__Graph__Add_Edge__Request() as _:
            assert type(_)              is Schema__Graph__Add_Edge__Request
            assert base_classes(_)      == [Type_Safe, object]
            assert type(_.graph_id)     is NoneType
            assert type(_.from_node_id) is NoneType
            assert type(_.to_node_id)   is NoneType
            assert _.auto_cache         is True

            assert _.obj() == __(graph_id     = _.graph_id     ,
                                 from_node_id = _.from_node_id ,
                                 to_node_id   = _.to_node_id   ,
                                 auto_cache   = True           )

    def test__with_values(self):                                                         # Test with explicit values
        graph_id     = Obj_Id()
        from_node_id = Obj_Id()
        to_node_id   = Obj_Id()
        with Schema__Graph__Add_Edge__Request(graph_id     = graph_id     ,
                                              from_node_id = from_node_id ,
                                              to_node_id   = to_node_id   ,
                                              auto_cache   = False        ) as _:
            assert _.graph_id     == graph_id
            assert _.from_node_id == from_node_id
            assert _.to_node_id   == to_node_id
            assert _.auto_cache   is False

    def test__serialization_round_trip(self):                                            # Test JSON round-trip
        edge_data = {Safe_Str__Key("weight"): Safe_Str__Text("1.5")}
        with Schema__Graph__Add_Edge__Request(auto_cache = True       ) as original:
            json_data = original.json()

            with Schema__Graph__Add_Edge__Request.from_json(json_data) as restored:
                assert type(restored.graph_id)     is NoneType
                assert type(restored.from_node_id) is NoneType
                assert type(restored.to_node_id)   is NoneType

                assert restored.obj () == original.obj ()
                assert restored.json() == original.json()


