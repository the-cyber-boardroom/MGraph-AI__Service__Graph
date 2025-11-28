from types                                                                                  import NoneType
from unittest                                                                               import TestCase
from osbot_utils.testing.__                                                                 import __
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.utils.Objects                                                              import base_classes
from mgraph_ai_service_cache_client.schemas.cache.Cache_Id                                  import Cache_Id
from mgraph_ai_service_graph.schemas.graph_ref.Graph_Id                                     import Graph_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref, GRAPH_REF__DEFAULT_NAMESPACE
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Delete__Response             import Schema__Graph__Delete__Response


class test_Schema__Graph__Delete__Response(TestCase):

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization
        with Schema__Graph__Delete__Response() as _:
            assert type(_)         is Schema__Graph__Delete__Response
            assert base_classes(_) == [Type_Safe, object]
            assert _.graph_ref     is None                                                  # Optional until set
            assert _.deleted       is False                                                 # Default value

    def test__init__field_types(self):                                                      # Test field types at initialization
        with Schema__Graph__Delete__Response() as _:
            assert type(_.graph_ref) is NoneType
            assert type(_.deleted)   is bool

    def test__init__obj_comparison(self):                                                   # Test .obj() with default values
        with Schema__Graph__Delete__Response() as _:
            assert _.obj() == __(graph_ref = None ,
                                 deleted   = False)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Value Assignment Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__with_graph_ref__deleted_true(self):                                           # Test successful deletion
        graph_id  = Graph_Id()
        cache_id  = Cache_Id()
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id       ,
                                       cache_id  = cache_id       ,
                                       namespace = 'test-namespace')

        with Schema__Graph__Delete__Response(graph_ref = graph_ref,
                                             deleted   = True     ) as _:
            assert _.graph_ref.graph_id  == graph_id
            assert _.graph_ref.cache_id  == cache_id
            assert _.graph_ref.namespace == 'test-namespace'
            assert _.deleted             is True

    def test__with_graph_ref__deleted_false(self):                                          # Test failed deletion (graph not found)
        graph_id  = Graph_Id()
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id ,
                                       namespace = 'test-ns')

        with Schema__Graph__Delete__Response(graph_ref = graph_ref,
                                             deleted   = False    ) as _:
            assert _.graph_ref.graph_id == graph_id
            assert _.deleted            is False

    def test__with_cache_id_only(self):                                                     # Test deletion by cache_id
        cache_id  = Cache_Id()
        graph_ref = Schema__Graph__Ref(cache_id  = cache_id ,
                                       namespace = 'cache-ns')

        with Schema__Graph__Delete__Response(graph_ref = graph_ref,
                                             deleted   = True     ) as _:
            assert _.graph_ref.cache_id  == cache_id
            assert _.graph_ref.graph_id  == ''                                              # Empty when deleted by cache_id
            assert _.deleted             is True

    def test__with_graph_id_only(self):                                                     # Test deletion by graph_id
        graph_id  = Graph_Id()
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id  ,
                                       namespace = 'graph-ns')

        with Schema__Graph__Delete__Response(graph_ref = graph_ref,
                                             deleted   = True     ) as _:
            assert _.graph_ref.graph_id  == graph_id
            assert _.graph_ref.cache_id  == ''                                              # Empty when deleted by graph_id
            assert _.deleted             is True

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Validation Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__graph_ref_field_types(self):                                                  # Test types within graph_ref
        graph_id  = Graph_Id()
        cache_id  = Cache_Id()
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id ,
                                       cache_id  = cache_id ,
                                       namespace = 'type-ns')

        with Schema__Graph__Delete__Response(graph_ref = graph_ref,
                                             deleted   = True     ) as _:
            assert type(_.graph_ref)           is Schema__Graph__Ref
            assert type(_.graph_ref.graph_id)  is Graph_Id
            assert type(_.graph_ref.cache_id)  is Cache_Id
            assert type(_.graph_ref.namespace) is Safe_Str__Id
            assert type(_.deleted)             is bool

    # ═══════════════════════════════════════════════════════════════════════════════
    # Serialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__serialization_round_trip__minimal(self):                                      # Test JSON round-trip with minimal data
        with Schema__Graph__Delete__Response(deleted = False) as original:
            json_data = original.json()

            with Schema__Graph__Delete__Response.from_json(json_data) as restored:
                assert restored.graph_ref == original.graph_ref
                assert restored.deleted   == original.deleted

    def test__serialization_round_trip__complete(self):                                     # Test JSON round-trip with all fields
        graph_ref = Schema__Graph__Ref(graph_id  = Graph_Id()  ,
                                       cache_id  = Cache_Id()  ,
                                       namespace = 'serial-ns' )

        with Schema__Graph__Delete__Response(graph_ref = graph_ref,
                                             deleted   = True     ) as original:
            json_data = original.json()

            with Schema__Graph__Delete__Response.from_json(json_data) as restored:
                assert restored.graph_ref.graph_id  == original.graph_ref.graph_id
                assert restored.graph_ref.cache_id  == original.graph_ref.cache_id
                assert restored.graph_ref.namespace == original.graph_ref.namespace
                assert restored.deleted             == original.deleted

    def test__serialization_preserves_types(self):                                          # Test that types are preserved after serialization
        graph_ref = Schema__Graph__Ref(graph_id  = Graph_Id() ,
                                       cache_id  = Cache_Id() ,
                                       namespace = 'type-test')

        with Schema__Graph__Delete__Response(graph_ref = graph_ref,
                                             deleted   = True     ) as original:
            json_data = original.json()

            with Schema__Graph__Delete__Response.from_json(json_data) as restored:
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

        with Schema__Graph__Delete__Response(graph_ref = graph_ref,
                                             deleted   = False    ) as _:
            assert _.graph_ref.graph_id == ''
            assert _.graph_ref.cache_id == ''
            assert _.deleted            is False

    def test__default_namespace(self):                                                      # Test default namespace value
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id())                               # Uses default namespace

        with Schema__Graph__Delete__Response(graph_ref = graph_ref,
                                             deleted   = True     ) as _:
            assert _.graph_ref.namespace == GRAPH_REF__DEFAULT_NAMESPACE