from types                                                                                  import NoneType
from unittest                                                                               import TestCase
from osbot_utils.testing.__                                                                 import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.utils.Objects                                                              import base_classes
from mgraph_ai_service_cache_client.schemas.cache.Cache_Id                                  import Cache_Id
from mgraph_ai_service_graph.schemas.graph_ref.Graph_Id                                     import Graph_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref, GRAPH_REF__DEFAULT_NAMESPACE
from mgraph_ai_service_graph.schemas.graph_edit.nodes.Schema__Graph__Add_Node__Request      import Schema__Graph__Add_Node__Request


class test_Schema__Graph__Add_Node__Request(TestCase):

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization
        with Schema__Graph__Add_Node__Request() as _:
            assert type(_)            is Schema__Graph__Add_Node__Request
            assert base_classes(_)    == [Type_Safe, object]
            assert _.graph_ref        is None                                               # Optional graph_ref
            assert _.auto_cache       is True                                               # Default value

    def test__init__field_types(self):                                                      # Test field types at initialization
        with Schema__Graph__Add_Node__Request() as _:
            assert type(_.graph_ref)  is NoneType
            assert type(_.auto_cache) is bool

    def test__init__obj_comparison(self):                                                   # Test .obj() with default values
        with Schema__Graph__Add_Node__Request() as _:
            assert _.obj() == __(graph_ref  = None,
                                 auto_cache = True)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Value Assignment Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__with_graph_ref__graph_id(self):                                               # Test with graph_ref containing graph_id
        graph_id  = Graph_Id(Obj_Id())
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id       ,
                                       namespace = 'test-namespace')

        with Schema__Graph__Add_Node__Request(graph_ref  = graph_ref,
                                              auto_cache = True     ) as _:
            assert _.graph_ref.graph_id  == graph_id
            assert _.graph_ref.graph_id  != ''
            assert _.graph_ref.namespace == 'test-namespace'
            assert _.auto_cache          is True

    def test__with_graph_ref__cache_id(self):                                               # Test with graph_ref containing cache_id
        cache_id  = Cache_Id(Random_Guid())
        graph_ref = Schema__Graph__Ref(cache_id  = cache_id ,
                                       namespace = 'cache-ns')

        with Schema__Graph__Add_Node__Request(graph_ref  = graph_ref,
                                              auto_cache = True     ) as _:
            assert _.graph_ref.cache_id  == cache_id
            assert _.graph_ref.cache_id  != ''
            assert _.graph_ref.namespace == 'cache-ns'

    def test__with_graph_ref__both_ids(self):                                               # Test with graph_ref containing both IDs
        graph_id  = Graph_Id(Obj_Id())
        cache_id  = Cache_Id(Random_Guid())
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id ,
                                       cache_id  = cache_id ,
                                       namespace = 'both-ns')

        with Schema__Graph__Add_Node__Request(graph_ref  = graph_ref,
                                              auto_cache = True     ) as _:
            assert _.graph_ref.graph_id  == graph_id
            assert _.graph_ref.cache_id  == cache_id
            assert _.graph_ref.namespace == 'both-ns'

    def test__with_auto_cache_false(self):                                                  # Test disabling auto_cache
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))

        with Schema__Graph__Add_Node__Request(graph_ref  = graph_ref,
                                              auto_cache = False    ) as _:
            assert _.auto_cache is False

    def test__with_empty_graph_ref(self):                                                   # Test with empty graph_ref (creates new graph)
        graph_ref = Schema__Graph__Ref(namespace = 'new-graph-ns')

        with Schema__Graph__Add_Node__Request(graph_ref  = graph_ref,
                                              auto_cache = True     ) as _:
            assert _.graph_ref.graph_id  == ''                                              # Empty - new graph will be created
            assert _.graph_ref.cache_id  == ''                                              # Empty - new graph will be created
            assert _.graph_ref.namespace == 'new-graph-ns'

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Validation Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__graph_ref_field_types(self):                                                  # Test types within graph_ref
        graph_id  = Graph_Id(Obj_Id())
        cache_id  = Cache_Id(Random_Guid())
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id ,
                                       cache_id  = cache_id ,
                                       namespace = 'type-ns')

        with Schema__Graph__Add_Node__Request(graph_ref = graph_ref) as _:
            assert type(_.graph_ref)           is Schema__Graph__Ref
            assert type(_.graph_ref.graph_id)  is Graph_Id
            assert type(_.graph_ref.cache_id)  is Cache_Id
            assert type(_.graph_ref.namespace) is Safe_Str__Id
            assert type(_.auto_cache)          is bool

    # ═══════════════════════════════════════════════════════════════════════════════
    # Serialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__serialization_round_trip__minimal(self):                                      # Test JSON round-trip with minimal data
        with Schema__Graph__Add_Node__Request(auto_cache = False) as original:
            json_data = original.json()

            with Schema__Graph__Add_Node__Request.from_json(json_data) as restored:
                assert restored.graph_ref  == original.graph_ref
                assert restored.auto_cache == original.auto_cache

    def test__serialization_round_trip__with_graph_ref(self):                               # Test JSON round-trip with graph_ref
        graph_ref = Schema__Graph__Ref(graph_id  = Graph_Id(Obj_Id()),
                                       cache_id  = Cache_Id(Random_Guid()),
                                       namespace = 'serial-ns')

        with Schema__Graph__Add_Node__Request(graph_ref  = graph_ref,
                                              auto_cache = True     ) as original:
            json_data = original.json()

            with Schema__Graph__Add_Node__Request.from_json(json_data) as restored:
                assert restored.graph_ref.graph_id  == original.graph_ref.graph_id
                assert restored.graph_ref.cache_id  == original.graph_ref.cache_id
                assert restored.graph_ref.namespace == original.graph_ref.namespace
                assert restored.auto_cache          == original.auto_cache

    def test__serialization_preserves_types(self):                                          # Test that types are preserved after serialization
        graph_ref = Schema__Graph__Ref(graph_id  = Graph_Id(Obj_Id()),
                                       namespace = 'type-test'       )

        with Schema__Graph__Add_Node__Request(graph_ref = graph_ref) as original:
            json_data = original.json()

            with Schema__Graph__Add_Node__Request.from_json(json_data) as restored:
                assert type(restored.graph_ref)           is Schema__Graph__Ref
                assert type(restored.graph_ref.graph_id)  is Graph_Id
                assert type(restored.graph_ref.namespace) is Safe_Str__Id

    # ═══════════════════════════════════════════════════════════════════════════════
    # Edge Cases
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__default_namespace(self):                                                      # Test default namespace from Schema__Graph__Ref
        graph_ref = Schema__Graph__Ref()                                                    # Uses default namespace

        with Schema__Graph__Add_Node__Request(graph_ref = graph_ref) as _:
            assert _.graph_ref.namespace == GRAPH_REF__DEFAULT_NAMESPACE

    def test__none_graph_ref(self):                                                         # Test with None graph_ref (will create new graph)
        with Schema__Graph__Add_Node__Request(graph_ref  = None,
                                              auto_cache = True) as _:
            assert _.graph_ref is None