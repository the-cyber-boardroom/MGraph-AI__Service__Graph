from types                                                                                  import NoneType
from unittest                                                                               import TestCase
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                                      import Node_Id
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                                          import Schema__MGraph__Node
from osbot_utils.testing.__                                                                 import __
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.utils.Objects                                                              import base_classes
from osbot_utils.type_safe.primitives.domains.identifiers.Cache_Id                          import Cache_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                                     import Graph_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref, GRAPH_REF__DEFAULT_NAMESPACE
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Node__Response         import Schema__Graph__Find_Node__Response


class test_Schema__Graph__Find_Node__Response(TestCase):

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization
        with Schema__Graph__Find_Node__Response() as _:
            assert type(_)           is Schema__Graph__Find_Node__Response
            assert base_classes(_)   == [Type_Safe, object]
            assert _.graph_ref       is None                                                # Optional graph_ref
            assert _.node_id         is None                                                # Node that was searched
            assert _.node_data       is None                                                # Node data
            assert _.found           is False                                               # Default not found

    def test__init__field_types(self):                                                      # Test field types at initialization
        with Schema__Graph__Find_Node__Response() as _:
            assert type(_.graph_ref) is NoneType
            assert type(_.node_id)   is NoneType
            assert type(_.node_data) is NoneType
            assert type(_.found)     is bool

    def test__init__obj_comparison(self):                                                   # Test .obj() with default values
        with Schema__Graph__Find_Node__Response() as _:
            assert _.obj() == __(graph_ref = None       ,
                                 node_id   = None       ,
                                 node_data = None       ,
                                 found     = False      )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Value Assignment Tests - Success Cases
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__with_graph_ref__found(self):                                                  # Test successful node find
        graph_id  = Graph_Id(Obj_Id())
        cache_id  = Cache_Id(Random_Guid())
        node_id   = Node_Id(Obj_Id())
        node_data = Schema__MGraph__Node()
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id       ,
                                       cache_id  = cache_id       ,
                                       namespace = 'test-namespace')

        with Schema__Graph__Find_Node__Response(graph_ref = graph_ref,
                                                node_id   = node_id  ,
                                                node_data = node_data,
                                                found     = True     ) as _:
            assert _.graph_ref.graph_id  == graph_id
            assert _.graph_ref.cache_id  == cache_id
            assert _.graph_ref.namespace == 'test-namespace'
            assert _.node_id             == node_id
            assert _.found               is True

    def test__with_graph_ref__not_found(self):                                              # Test node not found
        graph_id  = Graph_Id(Obj_Id())
        node_id   = Node_Id(Obj_Id())
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id   ,
                                       namespace = 'search-ns')

        with Schema__Graph__Find_Node__Response(graph_ref = graph_ref,
                                                node_id   = node_id  ,
                                                found     = False    ) as _:
            assert _.graph_ref.graph_id == graph_id
            assert _.node_id            == node_id
            assert _.found              is False
            assert _.node_data          is None

    def test__with_cache_id_lookup(self):                                                   # Test response when graph was found by cache_id
        cache_id  = Cache_Id(Random_Guid())
        graph_id  = Graph_Id(Obj_Id())
        node_id   = Node_Id(Obj_Id())
        graph_ref = Schema__Graph__Ref(cache_id  = cache_id ,
                                       graph_id  = graph_id ,                               # Resolved after lookup
                                       namespace = 'cache-ns')

        with Schema__Graph__Find_Node__Response(graph_ref = graph_ref,
                                                node_id   = node_id  ,
                                                found     = True     ) as _:
            assert _.graph_ref.cache_id == cache_id
            assert _.graph_ref.graph_id == graph_id
            assert _.node_id            == node_id
            assert _.found              is True

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Validation Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__graph_ref_field_types(self):                                                  # Test types within graph_ref
        graph_id  = Graph_Id(Obj_Id())
        cache_id  = Cache_Id(Random_Guid())
        node_id   = Node_Id(Obj_Id())
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id ,
                                       cache_id  = cache_id ,
                                       namespace = 'type-ns')

        with Schema__Graph__Find_Node__Response(graph_ref = graph_ref,
                                                node_id   = node_id  ,
                                                found     = True     ) as _:
            assert type(_.graph_ref)           is Schema__Graph__Ref
            assert type(_.graph_ref.graph_id)  is Graph_Id
            assert type(_.graph_ref.cache_id)  is Cache_Id
            assert type(_.graph_ref.namespace) is Safe_Str__Id
            assert type(_.node_id)             is Node_Id
            assert type(_.node_data)           is NoneType
            assert type(_.found)               is bool

    # ═══════════════════════════════════════════════════════════════════════════════
    # Serialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__serialization_round_trip__minimal(self):                                      # Test JSON round-trip with minimal data
        with Schema__Graph__Find_Node__Response(found = False) as original:
            json_data = original.json()

            with Schema__Graph__Find_Node__Response.from_json(json_data) as restored:
                assert restored.graph_ref == original.graph_ref
                assert restored.node_id   == original.node_id
                assert restored.found     == original.found

    def test__serialization_round_trip__complete(self):                                     # Test JSON round-trip with all fields
        graph_ref = Schema__Graph__Ref(graph_id  = Graph_Id(Obj_Id())    ,
                                       cache_id  = Cache_Id(Random_Guid()),
                                       namespace = 'serial-ns'           )
        node_id   = Node_Id(Obj_Id())
        node_type = Safe_Str__Id('Document')
        node_data = Schema__MGraph__Node()

        with Schema__Graph__Find_Node__Response(graph_ref = graph_ref,
                                                node_id   = node_id  ,
                                                node_data = node_data,
                                                found     = True     ) as original:
            json_data = original.json()

            with Schema__Graph__Find_Node__Response.from_json(json_data) as restored:
                assert restored.graph_ref.graph_id  == original.graph_ref.graph_id
                assert restored.graph_ref.cache_id  == original.graph_ref.cache_id
                assert restored.graph_ref.namespace == original.graph_ref.namespace
                assert restored.node_id             == original.node_id
                assert restored.node_data.obj()     == original.node_data.obj()
                assert restored.found               == original.found

    # ═══════════════════════════════════════════════════════════════════════════════
    # Edge Cases
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__default_namespace(self):                                                      # Test default namespace from Schema__Graph__Ref
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))                       # Uses default namespace

        with Schema__Graph__Find_Node__Response(graph_ref = graph_ref,
                                                found     = True     ) as _:
            assert _.graph_ref.namespace == GRAPH_REF__DEFAULT_NAMESPACE

    def test__empty_node_data(self):                                                        # Test with empty node_data
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))
        node_id   = Node_Id(Obj_Id())

        with Schema__Graph__Find_Node__Response(graph_ref = graph_ref,
                                                node_id   = node_id  ,
                                                found     = True     ) as _:
            assert type(_.node_data) is NoneType