from unittest                                                                               import TestCase
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.utils.Objects                                                              import base_classes
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Edges__Request         import Schema__Graph__Find_Edges__Request


class test_Schema__Graph__Find_Edges__Request(TestCase):

    def test__init__(self):                                                                 # Test auto-initialization
        with Schema__Graph__Find_Edges__Request() as _:
            assert type(_)           is Schema__Graph__Find_Edges__Request
            assert base_classes(_)   == [Type_Safe, object]
            assert type(_.graph_id)  is Obj_Id
            assert type(_.edge_type) is Safe_Str__Id

    def test__with_values(self):                                                            # Test with explicit values
        graph_id  = Obj_Id()
        edge_type = Safe_Str__Id('KNOWS')

        with Schema__Graph__Find_Edges__Request(graph_id  = graph_id ,
                                                edge_type = edge_type) as _:
            assert _.graph_id  == graph_id
            assert _.edge_type == edge_type