from unittest                                                                            import TestCase
from osbot_utils.testing.__                                                              import __
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                     import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                         import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id          import Safe_Str__Id
from osbot_utils.utils.Objects                                                           import base_classes
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Request      import Schema__Graph__Find_Nodes__Request


class test_Schema__Graph__Find_Nodes__Request(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Schema__Graph__Find_Nodes__Request() as _:
            assert type(_)            is Schema__Graph__Find_Nodes__Request
            assert base_classes(_)    == [Type_Safe, object]
            assert type(_.graph_id)   is Obj_Id
            assert type(_.node_type)  is Safe_Str__Id
            assert type(_.limit)      is Safe_UInt
            assert type(_.offset)     is Safe_UInt
            assert _.limit            == 100                                             # Default value
            assert _.offset           == 0                                               # Default value

            assert _.obj() == __(graph_id  = _.graph_id  ,
                                 node_type = _.node_type ,
                                 limit     = 100         ,
                                 offset    = 0           )

    def test__with_values(self):                                                         # Test with explicit values
        graph_id  = Obj_Id()
        node_type = Safe_Str__Id("Person")

        with Schema__Graph__Find_Nodes__Request(graph_id  = graph_id  ,
                                                node_type = node_type ,
                                                limit     = 50        ,
                                                offset    = 10        ) as _:
            assert _.graph_id  == graph_id
            assert _.node_type == node_type
            assert _.limit     == 50
            assert _.offset    == 10

    def test__pagination_defaults(self):                                                 # Test default pagination values
        with Schema__Graph__Find_Nodes__Request() as _:
            assert _.limit  == 100                                                       # Default limit
            assert _.offset == 0                                                         # Default offset

    def test__serialization_round_trip(self):                                            # Test JSON round-trip
        with Schema__Graph__Find_Nodes__Request(node_type = "Entity" ,
                                                limit     = 25       ,
                                                offset    = 5        ) as original:
            json_data = original.json()

            with Schema__Graph__Find_Nodes__Request.from_json(json_data) as restored:
                assert type(restored.graph_id)  is Obj_Id
                assert type(restored.node_type) is Safe_Str__Id
                assert type(restored.limit)     is Safe_UInt
                assert type(restored.offset)    is Safe_UInt
                assert restored.limit           == 25
                assert restored.offset          == 5