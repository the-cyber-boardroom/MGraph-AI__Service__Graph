from unittest                                                                               import TestCase
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                       import Type_Safe__List
from osbot_utils.type_safe.primitives.core.Safe_UInt                                        import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.utils.Objects                                                              import base_classes
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Edges__Response        import Schema__Graph__Find_Edges__Response
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Edge__Data                  import Schema__Graph__Edge__Data


class test_Schema__Graph__Find_Edges__Response(TestCase):

    def test__init__(self):                                                                 # Test auto-initialization
        with Schema__Graph__Find_Edges__Response() as _:
            assert type(_)             is Schema__Graph__Find_Edges__Response
            assert base_classes(_)     == [Type_Safe, object]
            assert type(_.graph_id)    is Obj_Id
            assert type(_.edge_type)   is Safe_Str__Id
            assert type(_.edges)       is Type_Safe__List
            assert type(_.total_found) is Safe_UInt

    def test__with_values(self):                                                            # Test with explicit values
        graph_id  = Obj_Id()
        edge_type = Safe_Str__Id('KNOWS')
        edge      = Schema__Graph__Edge__Data(edge_type=edge_type)

        with Schema__Graph__Find_Edges__Response(graph_id    = graph_id  ,
                                                 edge_type   = edge_type ,
                                                 edges       = [edge]    ,
                                                 total_found = 1         ) as _:
            assert _.graph_id    == graph_id
            assert _.edge_type   == edge_type
            assert len(_.edges)  == 1
            assert _.total_found == 1




