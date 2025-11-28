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


class test_Schema__Graph__Ref(TestCase):

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization with defaults
        with Schema__Graph__Ref() as _:
            assert type(_)         is Schema__Graph__Ref
            assert base_classes(_) == [Type_Safe, object]
            assert _.cache_id      == ''                                                    # Empty string default
            assert _.graph_id      == ''                                                    # Empty string default
            assert _.namespace     == GRAPH_REF__DEFAULT_NAMESPACE                          # Has default namespace

    def test__init__field_types(self):                                                      # Test field types
        with Schema__Graph__Ref() as _:
            assert type(_.cache_id)  is Cache_Id
            assert type(_.graph_id)  is Graph_Id
            assert type(_.namespace) is Safe_Str__Id

    def test__init__obj_comparison(self):                                                   # Test .obj() with default values
        with Schema__Graph__Ref() as _:
            assert _.obj() == __(cache_id  = ''                        ,
                                 graph_id  = ''                        ,
                                 namespace = GRAPH_REF__DEFAULT_NAMESPACE)

    def test__default_namespace_constant(self):                                             # Test default namespace constant
        assert GRAPH_REF__DEFAULT_NAMESPACE == 'graph-service'

    # ═══════════════════════════════════════════════════════════════════════════════
    # Value Assignment Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__with_graph_id_only(self):                                                     # Test with only graph_id set
        graph_id = Graph_Id(Obj_Id())                                                               # Generate new ID

        with Schema__Graph__Ref(graph_id = graph_id) as _:
            assert _.graph_id  == graph_id
            assert _.graph_id  != ''                                                        # Not empty
            assert _.cache_id  == ''                                                        # Empty default
            assert _.namespace == GRAPH_REF__DEFAULT_NAMESPACE

    def test__with_cache_id_only(self):                                                     # Test with only cache_id set
        cache_id = Cache_Id(Random_Guid())                                                               # Generate new ID

        with Schema__Graph__Ref(cache_id = cache_id) as _:
            assert _.cache_id  == cache_id
            assert _.cache_id  != ''                                                        # Not empty
            assert _.graph_id  == ''                                                        # Empty default
            assert _.namespace == GRAPH_REF__DEFAULT_NAMESPACE

    def test__with_both_ids(self):                                                          # Test with both IDs set
        graph_id = Graph_Id()
        cache_id = Cache_Id()

        with Schema__Graph__Ref(graph_id = graph_id,
                                cache_id = cache_id) as _:
            assert _.graph_id == graph_id
            assert _.cache_id == cache_id

    def test__with_custom_namespace(self):                                                  # Test with custom namespace
        with Schema__Graph__Ref(namespace = 'custom-namespace') as _:
            assert _.namespace == 'custom-namespace'
            assert _.graph_id  == ''
            assert _.cache_id  == ''

    def test__with_all_values(self):                                                        # Test with all values set
        graph_id = Graph_Id()
        cache_id = Cache_Id()

        with Schema__Graph__Ref(graph_id  = graph_id          ,
                                cache_id  = cache_id          ,
                                namespace = 'full-test-ns'    ) as _:
            assert _.graph_id  == graph_id
            assert _.cache_id  == cache_id
            assert _.namespace == 'full-test-ns'

    # ═══════════════════════════════════════════════════════════════════════════════
    # Empty Value Handling Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__empty_string_graph_id(self):                                                  # Test explicit empty string for graph_id
        with Schema__Graph__Ref(graph_id = '') as _:
            assert _.graph_id == ''
            assert type(_.graph_id) is Graph_Id

    def test__empty_string_cache_id(self):                                                  # Test explicit empty string for cache_id
        with Schema__Graph__Ref(cache_id = '') as _:
            assert _.cache_id == ''
            assert type(_.cache_id) is Cache_Id

    def test__none_converted_to_empty(self):                                                # Test that None values become empty strings
        # Note: This depends on Graph_Id and Cache_Id implementation
        graph_id = Graph_Id(None)
        cache_id = Cache_Id(None)

        assert graph_id == ''
        assert cache_id == ''

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Validation Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__graph_id_type(self):                                                          # Test Graph_Id type
        graph_id = Graph_Id(Obj_Id())                                                       # creates new graph_id with a valid random_guid

        with Schema__Graph__Ref(graph_id = graph_id) as _:
            assert type(_.graph_id) is Graph_Id
            assert len(_.graph_id)  == 8                                                    # Obj_Id length

    def test__cache_id_type(self):                                                          # Test Cache_Id type
        cache_id = Cache_Id()

        with Schema__Graph__Ref(cache_id = cache_id) as _:
            assert type(_.cache_id) is Cache_Id
            assert len(_.cache_id)  == 0                                                    # empty value

    def test__namespace_type(self):                                                         # Test namespace type
        with Schema__Graph__Ref(namespace = 'test-ns') as _:
            assert type(_.namespace) is Safe_Str__Id

    # ═══════════════════════════════════════════════════════════════════════════════
    # Serialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__serialization_round_trip__defaults(self):                                     # Test JSON round-trip with defaults
        with Schema__Graph__Ref() as original:
            json_data = original.json()

            with Schema__Graph__Ref.from_json(json_data) as restored:
                assert restored.graph_id  == original.graph_id
                assert restored.cache_id  == original.cache_id
                assert restored.namespace == original.namespace

    def test__serialization_round_trip__with_graph_id(self):                                # Test JSON round-trip with graph_id
        graph_id = Graph_Id()

        with Schema__Graph__Ref(graph_id = graph_id) as original:
            json_data = original.json()

            with Schema__Graph__Ref.from_json(json_data) as restored:
                assert restored.graph_id == graph_id

    def test__serialization_round_trip__with_cache_id(self):                                # Test JSON round-trip with cache_id
        cache_id = Cache_Id()

        with Schema__Graph__Ref(cache_id = cache_id) as original:
            json_data = original.json()

            with Schema__Graph__Ref.from_json(json_data) as restored:
                assert restored.cache_id == cache_id

    def test__serialization_round_trip__complete(self):                                     # Test JSON round-trip with all fields
        graph_id = Graph_Id()
        cache_id = Cache_Id()

        with Schema__Graph__Ref(graph_id  = graph_id     ,
                                cache_id  = cache_id     ,
                                namespace = 'serial-test') as original:
            json_data = original.json()

            with Schema__Graph__Ref.from_json(json_data) as restored:
                assert restored.graph_id  == original.graph_id
                assert restored.cache_id  == original.cache_id
                assert restored.namespace == original.namespace

    def test__serialization_preserves_types(self):                                          # Test that types are preserved after serialization
        graph_id = Graph_Id()
        cache_id = Cache_Id()

        with Schema__Graph__Ref(graph_id  = graph_id ,
                                cache_id  = cache_id ,
                                namespace = 'type-ns') as original:
            json_data = original.json()

            with Schema__Graph__Ref.from_json(json_data) as restored:
                assert type(restored.graph_id)  is Graph_Id
                assert type(restored.cache_id)  is Cache_Id
                assert type(restored.namespace) is Safe_Str__Id

    # ═══════════════════════════════════════════════════════════════════════════════
    # Comparison and Equality Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__equality__same_values(self):                                                  # Test equality with same values
        graph_id = Graph_Id()
        cache_id = Cache_Id()

        ref1 = Schema__Graph__Ref(graph_id  = graph_id ,
                                  cache_id  = cache_id ,
                                  namespace = 'test-ns')
        ref2 = Schema__Graph__Ref(graph_id  = graph_id ,
                                  cache_id  = cache_id ,
                                  namespace = 'test-ns')

        assert ref1.obj() == ref2.obj()

    def test__inequality__different_graph_id(self):                                         # Test inequality with different graph_id
        ref1 = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))
        ref2 = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))

        assert ref1.graph_id != ref2.graph_id

    def test__inequality__different_namespace(self):                                        # Test inequality with different namespace
        graph_id = Graph_Id()

        ref1 = Schema__Graph__Ref(graph_id = graph_id, namespace = 'ns-1')
        ref2 = Schema__Graph__Ref(graph_id = graph_id, namespace = 'ns-2')

        assert ref1.namespace != ref2.namespace

    # ═══════════════════════════════════════════════════════════════════════════════
    # Usage Pattern Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__create_pattern__new_graph(self):                                              # Test pattern for creating new graph
        # When creating a new graph, graph_ref may be empty or have only namespace
        with Schema__Graph__Ref(namespace = 'create-ns') as _:
            assert _.graph_id == ''                                                         # No graph_id yet
            assert _.cache_id == ''                                                         # No cache_id yet
            assert _.namespace == 'create-ns'

    def test__lookup_pattern__by_cache_id(self):                                            # Test pattern for lookup by cache_id
        cache_id = Cache_Id(Random_Guid())

        with Schema__Graph__Ref(cache_id = cache_id) as _:
            assert _.cache_id != ''                                                         # Has cache_id
            assert _.graph_id == ''                                                         # No graph_id needed

    def test__lookup_pattern__by_graph_id(self):                                            # Test pattern for lookup by graph_id
        graph_id = Graph_Id(Obj_Id())

        with Schema__Graph__Ref(graph_id = graph_id) as _:
            assert _.graph_id != ''                                                         # Has graph_id
            assert _.cache_id == ''                                                         # No cache_id needed

    def test__resolved_pattern__after_operation(self):                                      # Test pattern after graph operation (fully resolved)
        graph_id = Graph_Id(Obj_Id())
        cache_id = Cache_Id(Random_Guid())

        with Schema__Graph__Ref(graph_id  = graph_id ,
                                cache_id  = cache_id ,
                                namespace = 'resolved-ns') as _:
            assert _.graph_id  != ''                                                        # Has graph_id
            assert _.cache_id  != ''                                                        # Has cache_id
            assert _.namespace != ''                                                        # Has namespace

    # ═══════════════════════════════════════════════════════════════════════════════
    # Edge Cases
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__whitespace_in_namespace(self):                                                # Test namespace handling (Safe_Str__Id sanitizes)
        with Schema__Graph__Ref(namespace = 'test_namespace') as _:
            assert '_' in _.namespace                                                       # Underscore preserved

    def test__special_chars_in_namespace(self):                                             # Test special characters in namespace
        # Safe_Str__Id should sanitize special characters
        with Schema__Graph__Ref(namespace = 'test-namespace-123') as _:
            assert _.namespace == 'test-namespace-123'