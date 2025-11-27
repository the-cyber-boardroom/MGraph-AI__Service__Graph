from unittest                                                                               import TestCase
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                       import Type_Safe__Dict
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key            import Safe_Str__Key
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                import Safe_Str__Text
from osbot_utils.utils.Objects                                                              import base_classes
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Node__Response         import Schema__Graph__Find_Node__Response


class test_Schema__Graph__Find_Node__Response(TestCase):

    def test__init__(self):                                                                 # Test auto-initialization
        with Schema__Graph__Find_Node__Response() as _:
            assert type(_)           is Schema__Graph__Find_Node__Response
            assert base_classes(_)   == [Type_Safe, object]
            assert type(_.graph_id)  is Obj_Id
            assert type(_.node_id)   is Obj_Id
            assert type(_.node_type) is Safe_Str__Id
            assert type(_.node_data) is Type_Safe__Dict
            assert _.found           is False

    def test__with_values(self):                                                            # Test with explicit values
        graph_id  = Obj_Id()
        node_id   = Obj_Id()
        node_type = Safe_Str__Id('Person')
        node_data = {Safe_Str__Key('name'): Safe_Str__Text('Alice')}

        with Schema__Graph__Find_Node__Response(graph_id  = graph_id ,
                                                node_id   = node_id  ,
                                                node_type = node_type,
                                                node_data = node_data,
                                                found     = True     ) as _:
            assert _.graph_id  == graph_id
            assert _.node_id   == node_id
            assert _.node_type == node_type
            assert _.found     is True

