from types                                                                               import NoneType
from unittest                                                                            import TestCase
from osbot_utils.testing.__                                                              import __
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                         import Obj_Id
from osbot_utils.utils.Objects                                                           import base_classes
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Add_Edge__Response  import Schema__Graph__Add_Edge__Response


class test_Schema__Graph__Add_Edge__Response(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Schema__Graph__Add_Edge__Response() as _:
            assert type(_)           is Schema__Graph__Add_Edge__Response
            assert base_classes(_)   == [Type_Safe, object]
            assert type(_.edge_id)   is NoneType
            assert type(_.graph_id)  is NoneType
            assert type(_.cached)    is bool
            assert _.cached          is False

            assert _.obj() == __(edge_id=None,
                                 graph_id=None,
                                 from_node_id=None,
                                 to_node_id=None,
                                 cache_id=None,
                                 cached=False,
                                 success=False)

    def test__with_values(self):                                                         # Test with explicit values
        edge_id  = Obj_Id()
        graph_id = Obj_Id()

        with Schema__Graph__Add_Edge__Response(edge_id  = edge_id  ,
                                               graph_id = graph_id ,
                                               cached   = True     ) as _:
            assert _.edge_id  == edge_id
            assert _.graph_id == graph_id
            assert _.cached   is True