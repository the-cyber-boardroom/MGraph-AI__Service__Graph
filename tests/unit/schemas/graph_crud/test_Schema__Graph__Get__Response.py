from types import NoneType
from unittest                                                                            import TestCase
from osbot_utils.testing.__                                                              import __
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                     import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                         import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                    import Random_Guid
from osbot_utils.utils.Objects                                                           import base_classes
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Response             import Schema__Graph__Get__Response

class test_Schema__Graph__Get__Response(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Schema__Graph__Get__Response() as _:
            assert type(_)             is Schema__Graph__Get__Response
            assert base_classes(_)     == [Type_Safe, object]
            assert type(_.graph_id)    is NoneType
            assert _.cache_id          is None                                           # Optional field

            assert _.obj() == __(graph_id=None, cache_id=None, mgraph=None, success=False)

    def test__with_values(self):                                                         # Test with explicit values
        graph_id = Obj_Id()
        cache_id = Random_Guid()

        with Schema__Graph__Get__Response(graph_id   = graph_id ,
                                          cache_id   = cache_id ) as _:
            assert _.graph_id   == graph_id
            #assert _.cached     is True
            assert _.cache_id   == cache_id

            assert _.obj() == __(graph_id   = graph_id ,
                                 cache_id   = cache_id ,
                                 mgraph     = None     ,
                                 success    = False    )

    def test__serialization_round_trip(self):                                            # Test JSON round-trip
        cache_id = Random_Guid()
        with Schema__Graph__Get__Response(cache_id   = cache_id) as original:
            json_data = original.json()

            with Schema__Graph__Get__Response.from_json(json_data) as restored:
                assert restored.obj() == original.obj()


