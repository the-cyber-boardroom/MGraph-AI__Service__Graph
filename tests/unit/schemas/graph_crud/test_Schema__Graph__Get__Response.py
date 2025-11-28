from types                                                                                  import NoneType
from unittest                                                                               import TestCase
from osbot_utils.testing.__                                                                 import __
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.utils.Objects                                                              import base_classes
from mgraph_ai_service_cache_client.schemas.cache.Cache_Id                                  import Cache_Id
from mgraph_db.mgraph.MGraph                                                                import MGraph
from mgraph_ai_service_graph.schemas.graph_ref.Graph_Id                                     import Graph_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref, GRAPH_REF__DEFAULT_NAMESPACE
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Response                import Schema__Graph__Get__Response


class test_Schema__Graph__Get__Response(TestCase):

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization
        with Schema__Graph__Get__Response() as _:
            assert type(_)         is Schema__Graph__Get__Response
            assert base_classes(_) == [Type_Safe, object]
            assert _.graph_ref     is None                                                  # Optional until set
            assert _.mgraph        is None                                                  # No graph data initially
            assert _.success       is False                                                 # Default to failure

    def test__init__field_types(self):                                                      # Test field types at initialization
        with Schema__Graph__Get__Response() as _:
            assert type(_.graph_ref) is NoneType
            assert type(_.mgraph)    is NoneType
            assert type(_.success)   is bool

    def test__init__obj_comparison(self):                                                   # Test .obj() with default values
        with Schema__Graph__Get__Response() as _:
            assert _.obj() == __(graph_ref = None ,
                                 mgraph    = None ,
                                 success   = False)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Value Assignment Tests - Success Cases
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__with_graph_ref__success_true(self):                                           # Test successful graph retrieval
        graph_id  = Graph_Id()
        cache_id  = Cache_Id()
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id       ,
                                       cache_id  = cache_id       ,
                                       namespace = 'test-namespace')
        mgraph    = MGraph()

        with Schema__Graph__Get__Response(graph_ref = graph_ref,
                                          mgraph    = mgraph   ,
                                          success   = True     ) as _:
            assert _.graph_ref.graph_id  == graph_id
            assert _.graph_ref.cache_id  == cache_id
            assert _.graph_ref.namespace == 'test-namespace'
            assert _.mgraph              is not None
            assert type(_.mgraph)        is MGraph
            assert _.success             is True

    def test__with_graph_ref__success_false(self):                                          # Test failed graph retrieval (not found)
        graph_id  = Graph_Id()
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id ,
                                       namespace = 'test-ns')

        with Schema__Graph__Get__Response(graph_ref = graph_ref,
                                          mgraph    = None     ,
                                          success   = False    ) as _:
            assert _.graph_ref.graph_id == graph_id
            assert _.mgraph             is None
            assert _.success            is False

    def test__with_cache_id_lookup(self):                                                   # Test retrieval by cache_id
        cache_id  = Cache_Id()
        graph_ref = Schema__Graph__Ref(cache_id  = cache_id ,
                                       namespace = 'cache-ns')
        mgraph    = MGraph()

        with Schema__Graph__Get__Response(graph_ref = graph_ref,
                                          mgraph    = mgraph   ,
                                          success   = True     ) as _:
            assert _.graph_ref.cache_id  == cache_id
            assert _.mgraph              is not None
            assert _.success             is True

    def test__with_graph_id_lookup(self):                                                   # Test retrieval by graph_id
        graph_id  = Graph_Id()
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id  ,
                                       namespace = 'graph-ns')
        mgraph    = MGraph()

        with Schema__Graph__Get__Response(graph_ref = graph_ref,
                                          mgraph    = mgraph   ,
                                          success   = True     ) as _:
            assert _.graph_ref.graph_id  == graph_id
            assert _.mgraph              is not None
            assert _.success             is True

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Validation Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__graph_ref_field_types(self):                                                  # Test types within graph_ref
        graph_id  = Graph_Id()
        cache_id  = Cache_Id()
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id ,
                                       cache_id  = cache_id ,
                                       namespace = 'type-ns')
        mgraph    = MGraph()

        with Schema__Graph__Get__Response(graph_ref = graph_ref,
                                          mgraph    = mgraph   ,
                                          success   = True     ) as _:
            assert type(_.graph_ref)           is Schema__Graph__Ref
            assert type(_.graph_ref.graph_id)  is Graph_Id
            assert type(_.graph_ref.cache_id)  is Cache_Id
            assert type(_.graph_ref.namespace) is Safe_Str__Id
            assert type(_.mgraph)              is MGraph
            assert type(_.success)             is bool

    def test__mgraph_type(self):                                                            # Test MGraph type specifically
        mgraph = MGraph()

        with Schema__Graph__Get__Response(mgraph  = mgraph,
                                          success = True  ) as _:
            assert type(_.mgraph) is MGraph
            assert _.mgraph       is mgraph                                                 # Same instance

    # ═══════════════════════════════════════════════════════════════════════════════
    # Serialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__serialization_round_trip__minimal(self):                                      # Test JSON round-trip with minimal data
        with Schema__Graph__Get__Response(success = False) as original:
            json_data = original.json()

            with Schema__Graph__Get__Response.from_json(json_data) as restored:
                assert restored.graph_ref == original.graph_ref
                assert restored.success   == original.success

    def test__serialization_round_trip__with_graph_ref(self):                               # Test JSON round-trip with graph_ref (no mgraph)
        graph_ref = Schema__Graph__Ref(graph_id  = Graph_Id()  ,
                                       cache_id  = Cache_Id()  ,
                                       namespace = 'serial-ns' )

        with Schema__Graph__Get__Response(graph_ref = graph_ref,
                                          success   = True     ) as original:
            json_data = original.json()

            with Schema__Graph__Get__Response.from_json(json_data) as restored:
                assert restored.graph_ref.graph_id  == original.graph_ref.graph_id
                assert restored.graph_ref.cache_id  == original.graph_ref.cache_id
                assert restored.graph_ref.namespace == original.graph_ref.namespace
                assert restored.success             == original.success

    def test__serialization_preserves_types(self):                                          # Test that types are preserved after serialization
        graph_ref = Schema__Graph__Ref(graph_id  = Graph_Id() ,
                                       cache_id  = Cache_Id() ,
                                       namespace = 'type-test')

        with Schema__Graph__Get__Response(graph_ref = graph_ref,
                                          success   = True     ) as original:
            json_data = original.json()

            with Schema__Graph__Get__Response.from_json(json_data) as restored:
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

        with Schema__Graph__Get__Response(graph_ref = graph_ref,
                                          success   = False    ) as _:
            assert _.graph_ref.graph_id == ''
            assert _.graph_ref.cache_id == ''
            assert _.success            is False

    def test__default_namespace(self):                                                      # Test default namespace value
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id())                               # Uses default namespace

        with Schema__Graph__Get__Response(graph_ref = graph_ref,
                                          success   = True     ) as _:
            assert _.graph_ref.namespace == GRAPH_REF__DEFAULT_NAMESPACE

    def test__success_with_none_mgraph(self):                                               # Edge case: success=True but mgraph=None (shouldn't happen in practice)
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id())

        with Schema__Graph__Get__Response(graph_ref = graph_ref,
                                          mgraph    = None     ,
                                          success   = True     ) as _:
            assert _.success is True
            assert _.mgraph  is None                                                        # Inconsistent state but allowed by schema

    def test__success_false_with_mgraph(self):                                              # Edge case: success=False but mgraph set (shouldn't happen in practice)
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id())
        mgraph    = MGraph()

        with Schema__Graph__Get__Response(graph_ref = graph_ref,
                                          mgraph    = mgraph   ,
                                          success   = False    ) as _:
            assert _.success is False
            assert _.mgraph  is not None                                                    # Inconsistent state but allowed by schema

    # ═══════════════════════════════════════════════════════════════════════════════
    # MGraph Content Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__mgraph_is_usable(self):                                                       # Test that returned MGraph is functional
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id())
        mgraph    = MGraph()

        with Schema__Graph__Get__Response(graph_ref = graph_ref,
                                          mgraph    = mgraph   ,
                                          success   = True     ) as _:
            assert _.mgraph is not None
            assert hasattr(_.mgraph, 'edit')                                                # MGraph should have edit method
            assert hasattr(_.mgraph, 'query')                                               # MGraph should have query method