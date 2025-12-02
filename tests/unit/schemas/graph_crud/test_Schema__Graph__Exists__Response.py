from types                                                                                  import NoneType
from unittest                                                                               import TestCase
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.testing.__                                                                 import __
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.utils.Objects                                                              import base_classes
from osbot_utils.type_safe.primitives.domains.identifiers.Cache_Id                          import Cache_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                          import Graph_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref, GRAPH_REF__DEFAULT_NAMESPACE
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Exists__Response             import Schema__Graph__Exists__Response


class test_Schema__Graph__Exists__Response(TestCase):

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization
        with Schema__Graph__Exists__Response() as _:
            assert type(_)         is Schema__Graph__Exists__Response
            assert base_classes(_) == [Type_Safe, object]
            assert _.graph_ref     is None                                                  # Optional until set
            assert _.exists        is False                                                 # Default value

    def test__init__field_types(self):                                                      # Test field types at initialization
        with Schema__Graph__Exists__Response() as _:
            assert type(_.graph_ref) is NoneType
            assert type(_.exists)    is bool

    def test__init__obj_comparison(self):                                                   # Test .obj() with default values
        with Schema__Graph__Exists__Response() as _:
            assert _.obj() == __(graph_ref = None ,
                                 exists    = False)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Value Assignment Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__with_graph_ref__exists_true(self):                                            # Test graph exists
        graph_id  = Graph_Id(Obj_Id())
        cache_id  = Cache_Id(Random_Guid())
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id       ,
                                       cache_id  = cache_id       ,
                                       namespace = 'test-namespace')

        with Schema__Graph__Exists__Response(graph_ref = graph_ref,
                                             exists    = True     ) as _:
            assert _.graph_ref.graph_id  == graph_id
            assert _.graph_ref.cache_id  == cache_id
            assert _.graph_ref.namespace == 'test-namespace'
            assert _.exists              is True

    def test__with_graph_ref__exists_false(self):                                           # Test graph does not exist
        graph_id  = Graph_Id(Obj_Id())
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id ,
                                       namespace = 'test-ns')

        with Schema__Graph__Exists__Response(graph_ref = graph_ref,
                                             exists    = False    ) as _:
            assert _.graph_ref.graph_id == graph_id
            assert _.exists             is False

    def test__with_cache_id_lookup(self):                                                   # Test exists check by cache_id
        cache_id  = Cache_Id(Random_Guid())
        graph_ref = Schema__Graph__Ref(cache_id  = cache_id ,
                                       namespace = 'cache-ns')

        with Schema__Graph__Exists__Response(graph_ref = graph_ref,
                                             exists    = True     ) as _:
            assert _.graph_ref.cache_id  == cache_id
            assert _.graph_ref.graph_id  == ''                                              # Empty when checked by cache_id
            assert _.exists              is True

    def test__with_graph_id_lookup(self):                                                   # Test exists check by graph_id
        graph_id  = Graph_Id(Obj_Id())
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id  ,
                                       namespace = 'graph-ns')

        with Schema__Graph__Exists__Response(graph_ref = graph_ref,
                                             exists    = True     ) as _:
            assert _.graph_ref.graph_id  == graph_id
            assert _.graph_ref.cache_id  == ''                                              # Empty when checked by graph_id
            assert _.exists              is True

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Validation Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__graph_ref_field_types(self):                                                  # Test types within graph_ref
        graph_id  = Graph_Id(Obj_Id())
        cache_id  = Cache_Id(Random_Guid())
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id ,
                                       cache_id  = cache_id ,
                                       namespace = 'type-ns')

        with Schema__Graph__Exists__Response(graph_ref = graph_ref,
                                             exists    = True     ) as _:
            assert type(_.graph_ref)           is Schema__Graph__Ref
            assert type(_.graph_ref.graph_id)  is Graph_Id
            assert type(_.graph_ref.cache_id)  is Cache_Id
            assert type(_.graph_ref.namespace) is Safe_Str__Id
            assert type(_.exists)              is bool

    # ═══════════════════════════════════════════════════════════════════════════════
    # Serialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__serialization_round_trip__minimal(self):                                      # Test JSON round-trip with minimal data
        with Schema__Graph__Exists__Response(exists = False) as original:
            json_data = original.json()

            with Schema__Graph__Exists__Response.from_json(json_data) as restored:
                assert restored.graph_ref == original.graph_ref
                assert restored.exists    == original.exists

    def test__serialization_round_trip__complete(self):                                     # Test JSON round-trip with all fields
        graph_ref = Schema__Graph__Ref(graph_id  = Graph_Id(Obj_Id())  ,
                                       cache_id  = Cache_Id(Random_Guid())  ,
                                       namespace = 'serial-ns' )

        with Schema__Graph__Exists__Response(graph_ref = graph_ref,
                                             exists    = True     ) as original:
            json_data = original.json()

            with Schema__Graph__Exists__Response.from_json(json_data) as restored:
                assert restored.graph_ref.graph_id  == original.graph_ref.graph_id
                assert restored.graph_ref.cache_id  == original.graph_ref.cache_id
                assert restored.graph_ref.namespace == original.graph_ref.namespace
                assert restored.exists              == original.exists

    def test__serialization_preserves_types(self):                                          # Test that types are preserved after serialization
        graph_ref = Schema__Graph__Ref(graph_id  = Graph_Id(Obj_Id()) ,
                                       cache_id  = Cache_Id(Random_Guid()) ,
                                       namespace = 'type-test')

        with Schema__Graph__Exists__Response(graph_ref = graph_ref,
                                             exists    = True     ) as original:
            json_data = original.json()

            with Schema__Graph__Exists__Response.from_json(json_data) as restored:
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

        with Schema__Graph__Exists__Response(graph_ref = graph_ref,
                                             exists    = False    ) as _:
            assert _.graph_ref.graph_id == ''
            assert _.graph_ref.cache_id == ''
            assert _.exists             is False

    def test__default_namespace(self):                                                      # Test default namespace value
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))                               # Uses default namespace

        with Schema__Graph__Exists__Response(graph_ref = graph_ref,
                                             exists    = True     ) as _:
            assert _.graph_ref.namespace == GRAPH_REF__DEFAULT_NAMESPACE

    def test__exists_state_transitions(self):                                               # Test different exists states
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))

        with Schema__Graph__Exists__Response(graph_ref = graph_ref, exists = True) as exists_true:
            assert exists_true.exists is True

        with Schema__Graph__Exists__Response(graph_ref = graph_ref, exists = False) as exists_false:
            assert exists_false.exists is False