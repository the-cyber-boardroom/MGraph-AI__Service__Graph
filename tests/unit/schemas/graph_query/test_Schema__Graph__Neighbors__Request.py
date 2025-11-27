from unittest                                                                               import TestCase
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.utils.Objects                                                              import base_classes
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Neighbors__Request          import Schema__Graph__Neighbors__Request


class test_Schema__Graph__Neighbors__Request(TestCase):

    def test__init__(self):                                                                 # Test auto-initialization
        with Schema__Graph__Neighbors__Request() as _:
            assert type(_)          is Schema__Graph__Neighbors__Request
            assert base_classes(_)  == [Type_Safe, object]
            assert type(_.graph_id) is Obj_Id
            assert type(_.node_id)  is Obj_Id

    def test__with_values(self):                                                            # Test with explicit values
        graph_id = Obj_Id()
        node_id  = Obj_Id()

        with Schema__Graph__Neighbors__Request(graph_id = graph_id,
                                               node_id  = node_id ) as _:
            assert _.graph_id == graph_id
            assert _.node_id  == node_id