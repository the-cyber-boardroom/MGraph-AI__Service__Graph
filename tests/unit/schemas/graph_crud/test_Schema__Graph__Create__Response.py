from unittest                                                                            import TestCase
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                     import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                         import Obj_Id
from osbot_utils.utils.Objects                                                           import base_classes
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Response          import Schema__Graph__Create__Response

class test_Schema__Graph__Create__Response(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Schema__Graph__Create__Response() as _:
            assert type(_)             is Schema__Graph__Create__Response
            assert base_classes(_)     == [Type_Safe, object]
            assert type(_.graph_id)    is Obj_Id
            assert _.cached            is False
            assert _.cache_id          is None

    def test__serialization_round_trip(self):                                            # Test JSON round-trip
        with Schema__Graph__Create__Response(cached     = True ) as original:
            json_data = original.json()

            with Schema__Graph__Create__Response.from_json(json_data) as restored:
                assert restored.obj() == original.obj()