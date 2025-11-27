from unittest                                                                               import TestCase
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                       import Type_Safe__List
from osbot_utils.type_safe.primitives.core.Safe_UInt                                        import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.utils.Objects                                                              import base_classes
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Neighbors__Response         import Schema__Graph__Neighbors__Response


class test_Schema__Graph__Neighbors__Response(TestCase):

    def test__init__(self):                                                                 # Test auto-initialization
        with Schema__Graph__Neighbors__Response() as _:
            assert type(_)              is Schema__Graph__Neighbors__Response
            assert base_classes(_)      == [Type_Safe, object]
            assert type(_.graph_id)     is Obj_Id
            assert type(_.node_id)      is Obj_Id
            assert type(_.neighbor_ids) is Type_Safe__List
            assert type(_.total_found)  is Safe_UInt

    def test__with_values(self):                                                            # Test with explicit values
        graph_id     = Obj_Id()
        node_id      = Obj_Id()
        neighbor_ids = [Obj_Id(), Obj_Id()]

        with Schema__Graph__Neighbors__Response(graph_id     = graph_id    ,
                                                node_id      = node_id     ,
                                                neighbor_ids = neighbor_ids,
                                                total_found  = 2           ) as _:
            assert _.graph_id         == graph_id
            assert _.node_id          == node_id
            assert len(_.neighbor_ids) == 2
            assert _.total_found      == 2