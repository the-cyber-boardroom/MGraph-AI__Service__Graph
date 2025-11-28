from unittest                                                                               import TestCase
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.utils.Objects                                                              import base_classes
from mgraph_ai_service_graph.schemas.graph_edit.nodes.Schema__Graph__Delete_Node__Response  import Schema__Graph__Delete_Node__Response


class test_Schema__Graph__Delete_Node__Response(TestCase):

    def test__init__(self):                                                                 # Test auto-initialization
        with Schema__Graph__Delete_Node__Response() as _:
            assert type(_)         is Schema__Graph__Delete_Node__Response
            assert base_classes(_) == [Type_Safe, object]
            assert type(_.graph_id) is Obj_Id
            assert type(_.node_id)  is Obj_Id
            assert _.deleted       is False

    def test__with_values(self):                                                            # Test with explicit values
        graph_id = Obj_Id()
        node_id  = Obj_Id()

        with Schema__Graph__Delete_Node__Response(graph_id = graph_id,
                                                  node_id  = node_id ,
                                                  deleted  = True    ) as _:
            assert _.graph_id == graph_id
            assert _.node_id  == node_id
            assert _.deleted  is True

    def test__serialization_round_trip(self):                                               # Test JSON round-trip
        graph_id = Obj_Id()
        node_id  = Obj_Id()
        with Schema__Graph__Delete_Node__Response(graph_id = graph_id,
                                                  node_id  = node_id ,
                                                  deleted  = True    ) as original:
            json_data = original.json()

            with Schema__Graph__Delete_Node__Response.from_json(json_data) as restored:
                assert restored.deleted == original.deleted


