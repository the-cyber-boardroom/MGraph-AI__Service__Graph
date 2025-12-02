from unittest                                                                               import TestCase
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid
from osbot_utils.testing.__                                                                 import __
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.utils.Objects                                                              import base_classes
from osbot_utils.type_safe.primitives.domains.identifiers.Cache_Id                          import Cache_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                          import Graph_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref, GRAPH_REF__DEFAULT_NAMESPACE
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Response             import Schema__Graph__Create__Response


class test_Schema__Graph__Create__Response(TestCase):

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization
        with Schema__Graph__Create__Response() as _:
            assert type(_)              is Schema__Graph__Create__Response
            assert base_classes(_)      == [Type_Safe, object]
            assert type(_.graph_ref)    is Schema__Graph__Ref                                    # Will allways exit
            assert _.cached             is False                                                 # Default value

    def test__init__field_types(self):                                                      # Test field types at initialization
        with Schema__Graph__Create__Response() as _:
            assert type(_.graph_ref) is Schema__Graph__Ref
            assert type(_.cached)    is bool

    # ═══════════════════════════════════════════════════════════════════════════════
    # Value Assignment Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__with_graph_ref(self):                                                         # Test with graph_ref containing IDs
        graph_id  = Graph_Id(Obj_Id())                                                              # Generate new graph_id
        cache_id  = Cache_Id(Random_Guid())                                                              # Generate new cache_id
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id                  ,
                                       cache_id  = cache_id                  ,
                                       namespace = GRAPH_REF__DEFAULT_NAMESPACE)

        with Schema__Graph__Create__Response(graph_ref = graph_ref,
                                             cached    = True     ) as _:
            assert _.graph_ref.graph_id  == graph_id
            assert _.graph_ref.cache_id  == cache_id
            assert _.graph_ref.namespace == GRAPH_REF__DEFAULT_NAMESPACE
            assert _.cached              is True

    def test__with_cached_true(self):                                                       # Test cached flag
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))

        with Schema__Graph__Create__Response(graph_ref = graph_ref,
                                             cached    = True     ) as _:
            assert _.cached is True

    def test__with_cached_false(self):                                                      # Test cached=False (graph not stored)
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id())

        with Schema__Graph__Create__Response(graph_ref = graph_ref,
                                             cached    = False    ) as _:
            assert _.cached                is False
            assert _.graph_ref.graph_id    == ''                                            # default Graph_id is an empty string
            assert _.graph_ref.cache_id    == ''                                            # No cache_id when not cached

    def test__with_custom_namespace(self):                                                  # Test with custom namespace
        graph_ref = Schema__Graph__Ref(graph_id  = Graph_Id(Obj_Id())        ,
                                       cache_id  = Cache_Id(Random_Guid())        ,
                                       namespace = 'custom-namespace')

        with Schema__Graph__Create__Response(graph_ref = graph_ref,
                                             cached    = True     ) as _:
            assert _.graph_ref.namespace == 'custom-namespace'

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Validation Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__graph_ref_field_types(self):                                                  # Test types within graph_ref
        graph_id  = Graph_Id(Obj_Id())
        cache_id  = Cache_Id(Random_Guid())
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id ,
                                       cache_id  = cache_id ,
                                       namespace = 'test-ns')

        with Schema__Graph__Create__Response(graph_ref = graph_ref,
                                             cached    = True     ) as _:
            assert type(_.graph_ref)           is Schema__Graph__Ref
            assert type(_.graph_ref.graph_id)  is Graph_Id
            assert type(_.graph_ref.cache_id)  is Cache_Id
            assert type(_.graph_ref.namespace) is Safe_Str__Id
            assert type(_.cached)              is bool

    # ═══════════════════════════════════════════════════════════════════════════════
    # Serialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__serialization_round_trip__minimal(self):                                      # Test JSON round-trip with minimal data
        with Schema__Graph__Create__Response(cached = False) as original:
            json_data = original.json()

            with Schema__Graph__Create__Response.from_json(json_data) as restored:
                assert restored.graph_ref.obj() == original.graph_ref.obj()
                assert restored.cached          == original.cached

    def test__serialization_round_trip__complete(self):                                     # Test JSON round-trip with all fields
        graph_ref = Schema__Graph__Ref(graph_id  = Graph_Id(Obj_Id())  ,
                                       cache_id  = Cache_Id(Random_Guid())  ,
                                       namespace = 'serial-ns' )

        with Schema__Graph__Create__Response(graph_ref = graph_ref,
                                             cached    = True     ) as original:
            json_data = original.json()

            with Schema__Graph__Create__Response.from_json(json_data) as restored:
                assert restored.graph_ref.graph_id  == original.graph_ref.graph_id
                assert restored.graph_ref.cache_id  == original.graph_ref.cache_id
                assert restored.graph_ref.namespace == original.graph_ref.namespace
                assert restored.cached              == original.cached

    def test__serialization_preserves_types(self):                                          # Test that types are preserved after serialization
        graph_ref = Schema__Graph__Ref(graph_id  = Graph_Id(Obj_Id()) ,
                                       cache_id  = Cache_Id(Random_Guid()) ,
                                       namespace = 'type-test')

        with Schema__Graph__Create__Response(graph_ref = graph_ref,
                                             cached    = True     ) as original:
            json_data = original.json()

            with Schema__Graph__Create__Response.from_json(json_data) as restored:
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

        with Schema__Graph__Create__Response(graph_ref = graph_ref,
                                             cached    = False    ) as _:
            assert _.graph_ref.graph_id == ''
            assert _.graph_ref.cache_id == ''

    def test__obj_comparison(self):                                                         # Test .obj() method for comparison
        graph_ref = Schema__Graph__Ref(graph_id  = Graph_Id() ,
                                       cache_id  = Cache_Id() ,
                                       namespace = 'obj-test' )

        with Schema__Graph__Create__Response(graph_ref = graph_ref,
                                             cached    = True     ) as _:
            assert _.obj() == __(graph_ref = __(cache_id  = '',
                                                graph_id  = '',
                                                namespace = 'obj-test'),
                                 cached   = True                       )
