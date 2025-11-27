from unittest                                                                               import TestCase
from osbot_utils.testing.__                                                                 import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.utils.Objects                                                              import base_classes
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Delete__Response             import Schema__Graph__Delete__Response


class test_Schema__Graph__Delete__Response(TestCase):

    def test__init__(self):                                                                 # Test auto-initialization
        with Schema__Graph__Delete__Response() as _:
            assert type(_)         is Schema__Graph__Delete__Response
            assert base_classes(_) == [Type_Safe, object]
            assert _.graph_id      is None
            assert _.cache_id      is None
            assert _.namespace     is None
            assert _.deleted       is False

            assert _.obj() == __(graph_id  = None  ,
                                 cache_id  = None  ,
                                 namespace = None  ,
                                 deleted   = False )

    def test__with_values(self):                                                            # Test with explicit values
        graph_id  = Obj_Id()
        cache_id  = Random_Guid()
        namespace = Safe_Str__Id('test-namespace')

        with Schema__Graph__Delete__Response(graph_id  = graph_id  ,
                                             cache_id  = cache_id  ,
                                             namespace = namespace ,
                                             deleted   = True      ) as _:
            assert _.graph_id  == graph_id
            assert _.cache_id  == cache_id
            assert _.namespace == namespace
            assert _.deleted   is True

    def test__serialization_round_trip(self):                                               # Test JSON round-trip
        graph_id = Obj_Id()
        with Schema__Graph__Delete__Response(graph_id = graph_id,
                                             deleted  = True    ) as original:
            json_data = original.json()

            with Schema__Graph__Delete__Response.from_json(json_data) as restored:
                assert restored.obj() == original.obj()
