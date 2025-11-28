from types                                                                                  import NoneType
from unittest                                                                               import TestCase
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Display_Name   import Safe_Str__Display_Name
from osbot_utils.utils.Objects                                                              import base_classes
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref, GRAPH_REF__DEFAULT_NAMESPACE
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Request              import Schema__Graph__Create__Request


class test_Schema__Graph__Create__Request(TestCase):

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization
        with Schema__Graph__Create__Request() as _:
            assert type(_)            is Schema__Graph__Create__Request
            assert base_classes(_)    == [Type_Safe, object]
            assert _.graph_ref        is None                                               # Optional graph_ref
            assert _.graph_name       is None                                               # Optional name
            assert _.auto_cache       is True                                               # Default value

    def test__init__field_types(self):                                                      # Test field types
        with Schema__Graph__Create__Request() as _:
            assert type(_.graph_ref)  is NoneType
            assert type(_.graph_name) is NoneType
            assert type(_.auto_cache) is bool

    # ═══════════════════════════════════════════════════════════════════════════════
    # Value Assignment Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__with_graph_ref(self):                                                         # Test with graph_ref
        graph_ref = Schema__Graph__Ref(namespace = 'custom-namespace')

        with Schema__Graph__Create__Request(graph_ref = graph_ref) as _:
            assert _.graph_ref           is not None
            assert _.graph_ref.namespace == 'custom-namespace'
            assert _.graph_ref.graph_id  == ''                                              # Empty Graph_Id
            assert _.graph_ref.cache_id  == ''                                              # Empty Cache_Id
            assert _.auto_cache          is True

    def test__with_graph_name(self):                                                        # Test with graph_name
        with Schema__Graph__Create__Request(graph_name = 'My Test Graph') as _:
            assert _.graph_name == 'My Test Graph'
            assert type(_.graph_name) is Safe_Str__Display_Name

    def test__with_auto_cache_false(self):                                                  # Test disabling auto_cache
        with Schema__Graph__Create__Request(auto_cache = False) as _:
            assert _.auto_cache is False

    def test__with_all_values(self):                                                        # Test with all explicit values
        graph_ref = Schema__Graph__Ref(namespace = 'test-ns')

        with Schema__Graph__Create__Request(graph_ref  = graph_ref       ,
                                            graph_name = 'Complete Graph',
                                            auto_cache = False           ) as _:
            assert _.graph_ref.namespace == 'test-ns'
            assert _.graph_name          == 'Complete Graph'
            assert _.auto_cache          is False

    # ═══════════════════════════════════════════════════════════════════════════════
    # Serialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__serialization_round_trip__minimal(self):                                      # Test JSON round-trip with defaults
        with Schema__Graph__Create__Request() as original:
            json_data = original.json()

            with Schema__Graph__Create__Request.from_json(json_data) as restored:
                assert restored.graph_ref  == original.graph_ref
                assert restored.graph_name == original.graph_name
                assert restored.auto_cache == original.auto_cache

    def test__serialization_round_trip__with_graph_ref(self):                               # Test JSON round-trip with graph_ref
        graph_ref = Schema__Graph__Ref(namespace = 'serialization-test')

        with Schema__Graph__Create__Request(graph_ref  = graph_ref      ,
                                            graph_name = 'Test Graph'   ,
                                            auto_cache = False          ) as original:
            json_data = original.json()

            with Schema__Graph__Create__Request.from_json(json_data) as restored:
                assert restored.graph_ref.namespace == 'serialization-test'
                assert restored.graph_name          == 'Test Graph'
                assert restored.auto_cache          is False

    # ═══════════════════════════════════════════════════════════════════════════════
    # Edge Cases
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__graph_ref_with_empty_ids(self):                                               # Test graph_ref with empty IDs (valid for create)
        graph_ref = Schema__Graph__Ref(cache_id  = ''                    ,
                                       graph_id  = ''                    ,
                                       namespace = GRAPH_REF__DEFAULT_NAMESPACE)

        with Schema__Graph__Create__Request(graph_ref = graph_ref) as _:
            assert _.graph_ref.cache_id  == ''
            assert _.graph_ref.graph_id  == ''
            assert _.graph_ref.namespace == GRAPH_REF__DEFAULT_NAMESPACE

    def test__default_namespace_propagation(self):                                          # Test default namespace when graph_ref provided
        graph_ref = Schema__Graph__Ref()                                                    # Uses default namespace

        with Schema__Graph__Create__Request(graph_ref = graph_ref) as _:
            assert _.graph_ref.namespace == GRAPH_REF__DEFAULT_NAMESPACE