from types                                                                               import NoneType
from unittest                                                                            import TestCase
from osbot_utils.testing.__                                                              import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                         import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id          import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key         import Safe_Str__Key
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text             import Safe_Str__Text
from osbot_utils.utils.Objects                                                           import base_classes
from mgraph_ai_service_graph.schemas.graph_edit.nodes.Schema__Graph__Add_Node__Request   import Schema__Graph__Add_Node__Request


class test_Schema__Graph__Add_Node__Request(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Schema__Graph__Add_Node__Request() as _:
            assert type(_)            is Schema__Graph__Add_Node__Request
            assert base_classes(_)    == [Type_Safe, object]
            assert type(_.graph_id)   is NoneType
            assert _.auto_cache       is True                                            # Default value

            assert _.obj() == __(graph_id   = _.graph_id  ,
                                 auto_cache = True        )

    def test__with_values(self):                                                         # Test with explicit values
        graph_id  = Obj_Id()


        with Schema__Graph__Add_Node__Request(graph_id   = graph_id   ,
                                              auto_cache = False      ) as _:
            assert _.graph_id   == graph_id
            assert _.auto_cache is False

    def test__serialization_round_trip(self):                                            # Test JSON round-trip
        with Schema__Graph__Add_Node__Request(auto_cache = False      ) as original:
            json_data = original.json()

            with Schema__Graph__Add_Node__Request.from_json(json_data) as restored:
                assert type(restored.graph_id)  is NoneType
