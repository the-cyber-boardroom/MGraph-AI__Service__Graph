from unittest                                                                               import TestCase
from osbot_utils.testing.__                                                                 import __
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.utils.Objects                                                              import base_classes
from mgraph_ai_service_cache_client.schemas.cache.Cache_Id                                  import Cache_Id
from mgraph_ai_service_graph.schemas.graph_ref.Graph_Id                                     import Graph_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref, GRAPH_REF__DEFAULT_NAMESPACE
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Request                 import Schema__Graph__Get__Request


class test_Schema__Graph__Get__Request(TestCase):

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization
        with Schema__Graph__Get__Request() as _:
            assert type(_)           is Schema__Graph__Get__Request
            assert base_classes(_)   == [Type_Safe, object]
            assert type(_.graph_ref) is Schema__Graph__Ref                                                  # Optional until set

    def test__init__field_types(self):                                                      # Test field types at initialization
        with Schema__Graph__Get__Request() as _:
            assert type(_.graph_ref) is Schema__Graph__Ref

    def test__init__obj_comparison(self):                                                   # Test .obj() with default values
        with Schema__Graph__Get__Request() as _:
            assert _.obj() == __(graph_ref=__(cache_id='', graph_id=Graph_Id(''), namespace='graph-service'))

    # ═══════════════════════════════════════════════════════════════════════════════
    # Value Assignment Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__with_graph_ref__graph_id(self):                                               # Test get by graph_id
        graph_id  = Graph_Id()
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id       ,
                                       namespace = 'test-namespace')

        with Schema__Graph__Get__Request(graph_ref = graph_ref) as _:
            assert _.graph_ref.graph_id  == graph_id
            assert _.graph_ref.cache_id  == ''                                              # Empty when using graph_id
            assert _.graph_ref.namespace == 'test-namespace'

    def test__with_graph_ref__cache_id(self):                                               # Test get by cache_id
        cache_id  = Cache_Id()
        graph_ref = Schema__Graph__Ref(cache_id  = cache_id  ,
                                       namespace = 'cache-ns')

        with Schema__Graph__Get__Request(graph_ref = graph_ref) as _:
            assert _.graph_ref.cache_id  == cache_id
            assert _.graph_ref.graph_id  == ''                                              # Empty when using cache_id
            assert _.graph_ref.namespace == 'cache-ns'

    def test__with_graph_ref__both_ids(self):                                               # Test with both IDs (should be avoided but valid)
        graph_id  = Graph_Id()
        cache_id  = Cache_Id()
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id ,
                                       cache_id  = cache_id ,
                                       namespace = 'both-ns')

        with Schema__Graph__Get__Request(graph_ref = graph_ref) as _:
            assert _.graph_ref.graph_id  == graph_id
            assert _.graph_ref.cache_id  == cache_id
            assert _.graph_ref.namespace == 'both-ns'

    def test__with_default_namespace(self):                                                 # Test default namespace
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id())                               # Uses default namespace

        with Schema__Graph__Get__Request(graph_ref = graph_ref) as _:
            assert _.graph_ref.namespace == GRAPH_REF__DEFAULT_NAMESPACE

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Validation Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__graph_ref_field_types(self):                                                  # Test types within graph_ref
        graph_id  = Graph_Id()
        cache_id  = Cache_Id()
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id ,
                                       cache_id  = cache_id ,
                                       namespace = 'type-ns')

        with Schema__Graph__Get__Request(graph_ref = graph_ref) as _:
            assert type(_.graph_ref)           is Schema__Graph__Ref
            assert type(_.graph_ref.graph_id)  is Graph_Id
            assert type(_.graph_ref.cache_id)  is Cache_Id
            assert type(_.graph_ref.namespace) is Safe_Str__Id

    # ═══════════════════════════════════════════════════════════════════════════════
    # Serialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__serialization_round_trip__minimal(self):                                      # Test JSON round-trip with minimal data
        with Schema__Graph__Get__Request() as original:
            json_data = original.json()

            with Schema__Graph__Get__Request.from_json(json_data) as restored:
                assert restored.graph_ref.obj() == original.graph_ref.obj()

    def test__serialization_round_trip__with_graph_id(self):                                # Test JSON round-trip with graph_id
        graph_ref = Schema__Graph__Ref(graph_id  = Graph_Id()  ,
                                       namespace = 'serial-ns' )

        with Schema__Graph__Get__Request(graph_ref = graph_ref) as original:
            json_data = original.json()

            with Schema__Graph__Get__Request.from_json(json_data) as restored:
                assert restored.graph_ref.graph_id  == original.graph_ref.graph_id
                assert restored.graph_ref.namespace == original.graph_ref.namespace

    def test__serialization_round_trip__with_cache_id(self):                                # Test JSON round-trip with cache_id
        graph_ref = Schema__Graph__Ref(cache_id  = Cache_Id()  ,
                                       namespace = 'cache-serial')

        with Schema__Graph__Get__Request(graph_ref = graph_ref) as original:
            json_data = original.json()

            with Schema__Graph__Get__Request.from_json(json_data) as restored:
                assert restored.graph_ref.cache_id  == original.graph_ref.cache_id
                assert restored.graph_ref.namespace == original.graph_ref.namespace

    def test__serialization_preserves_types(self):                                          # Test that types are preserved after serialization
        graph_ref = Schema__Graph__Ref(graph_id  = Graph_Id() ,
                                       cache_id  = Cache_Id() ,
                                       namespace = 'type-test')

        with Schema__Graph__Get__Request(graph_ref = graph_ref) as original:
            json_data = original.json()

            with Schema__Graph__Get__Request.from_json(json_data) as restored:
                assert type(restored.graph_ref)           is Schema__Graph__Ref
                assert type(restored.graph_ref.graph_id)  is Graph_Id
                assert type(restored.graph_ref.cache_id)  is Cache_Id
                assert type(restored.graph_ref.namespace) is Safe_Str__Id

    # ═══════════════════════════════════════════════════════════════════════════════
    # Edge Cases
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__empty_graph_ref_ids(self):                                                    # Test graph_ref with empty IDs
        graph_ref = Schema__Graph__Ref(graph_id  = ''                        ,
                                       cache_id  = ''                        ,
                                       namespace = GRAPH_REF__DEFAULT_NAMESPACE)

        with Schema__Graph__Get__Request(graph_ref = graph_ref) as _:
            assert _.graph_ref.graph_id == ''
            assert _.graph_ref.cache_id == ''

    def test__graph_ref_with_only_namespace(self):                                          # Test graph_ref with only namespace (would create new)
        graph_ref = Schema__Graph__Ref(namespace = 'namespace-only')

        with Schema__Graph__Get__Request(graph_ref = graph_ref) as _:
            assert _.graph_ref.graph_id  == ''
            assert _.graph_ref.cache_id  == ''
            assert _.graph_ref.namespace == 'namespace-only'

    def test__multiple_requests_same_graph_ref(self):                                       # Test reusing graph_ref
        graph_id  = Graph_Id()
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id ,
                                       namespace = 'reuse-ns')

        with Schema__Graph__Get__Request(graph_ref = graph_ref) as request1:
            with Schema__Graph__Get__Request(graph_ref = graph_ref) as request2:
                assert request1.graph_ref.graph_id == request2.graph_ref.graph_id
                assert request1.graph_ref.graph_id == graph_id