from types import NoneType
from unittest                                                                            import TestCase
from osbot_utils.testing.__                                                              import __
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                         import Obj_Id
from osbot_utils.utils.Objects                                                           import base_classes
from mgraph_ai_service_graph.schemas.graph_edit.nodes.Schema__Graph__Add_Node__Response  import Schema__Graph__Add_Node__Response


class test_Schema__Graph__Add_Node__Response(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Schema__Graph__Add_Node__Response() as _:
            assert type(_)           is Schema__Graph__Add_Node__Response
            assert base_classes(_)   == [Type_Safe, object]
            assert type(_.node_id)   is NoneType
            assert type(_.graph_id)  is NoneType
            assert type(_.cached)    is bool
            assert _.cached          is False

            assert _.obj() == __(node_id=None, graph_id=None, cache_id=None, cached=False, success=False)

    def test__with_values(self):                                                         # Test with explicit values
        node_id  = Obj_Id()
        graph_id = Obj_Id()

        with Schema__Graph__Add_Node__Response(node_id  = node_id  ,
                                               graph_id = graph_id ,
                                               cached   = True     ) as _:
            assert _.node_id  == node_id
            assert _.graph_id == graph_id
            assert _.cached   is True
