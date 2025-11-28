from types                                                                                  import NoneType
from unittest                                                                               import TestCase

from mgraph_ai_service_graph.schemas.graph_ref.Node_Id import Node_Id
from osbot_utils.testing.__                                                                 import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                       import Type_Safe__List
from osbot_utils.type_safe.primitives.core.Safe_UInt                                        import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.utils.Objects                                                              import base_classes
from mgraph_ai_service_cache_client.schemas.cache.Cache_Id                                  import Cache_Id
from mgraph_ai_service_graph.schemas.graph_ref.Graph_Id                                     import Graph_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref, GRAPH_REF__DEFAULT_NAMESPACE
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Neighbors__Response         import Schema__Graph__Neighbors__Response


class test_Schema__Graph__Neighbors__Response(TestCase):

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization
        with Schema__Graph__Neighbors__Response() as _:
            assert type(_)              is Schema__Graph__Neighbors__Response
            assert base_classes(_)      == [Type_Safe, object]
            assert _.graph_ref          is None                                             # Optional graph_ref
            assert _.node_id            is None                                             # Node that was queried
            assert type(_.neighbor_ids) is Type_Safe__List                                  # List of neighbor IDs
            assert type(_.total_found)  is Safe_UInt

    def test__init__field_types(self):                                                      # Test field types at initialization
        with Schema__Graph__Neighbors__Response() as _:
            assert type(_.graph_ref)    is NoneType
            assert type(_.node_id)      is NoneType
            assert type(_.neighbor_ids) is Type_Safe__List
            assert type(_.total_found)  is Safe_UInt

    def test__init__obj_comparison(self):                                                   # Test .obj() with default values
        with Schema__Graph__Neighbors__Response() as _:
            assert _.obj() == __(graph_ref    = None,
                                 node_id      = None,
                                 neighbor_ids = []  ,
                                 total_found  = 0   )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Value Assignment Tests - Success Cases
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__with_graph_ref__neighbors_found(self):                                        # Test with neighbors found
        graph_id     = Graph_Id(Obj_Id())
        cache_id     = Cache_Id(Random_Guid())
        node_id      = Node_Id()
        neighbor_ids = [Obj_Id(), Obj_Id()]
        graph_ref    = Schema__Graph__Ref(graph_id  = graph_id       ,
                                          cache_id  = cache_id       ,
                                          namespace = 'test-namespace')

        with Schema__Graph__Neighbors__Response(graph_ref    = graph_ref   ,
                                                node_id      = node_id     ,
                                                neighbor_ids = neighbor_ids,
                                                total_found  = 2           ) as _:
            assert _.graph_ref.graph_id  == graph_id
            assert _.graph_ref.cache_id  == cache_id
            assert _.graph_ref.namespace == 'test-namespace'
            assert _.node_id             == node_id
            assert len(_.neighbor_ids)   == 2
            assert _.total_found         == 2

    def test__with_cache_id_lookup(self):                                                   # Test response when graph was found by cache_id
        cache_id     = Cache_Id(Random_Guid())
        graph_id     = Graph_Id(Obj_Id())
        node_id      = Obj_Id()
        neighbor_ids = [Obj_Id(), Obj_Id(), Obj_Id()]
        graph_ref    = Schema__Graph__Ref(cache_id  = cache_id ,
                                          graph_id  = graph_id ,                            # Resolved after lookup
                                          namespace = 'cache-ns')

        with Schema__Graph__Neighbors__Response(graph_ref    = graph_ref   ,
                                                node_id      = node_id     ,
                                                neighbor_ids = neighbor_ids,
                                                total_found  = 3           ) as _:
            assert _.graph_ref.cache_id == cache_id
            assert _.graph_ref.graph_id == graph_id
            assert len(_.neighbor_ids)  == 3
            assert _.total_found        == 3

    def test__with_single_neighbor(self):                                                   # Test node with single neighbor
        graph_ref    = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))
        node_id      = Node_Id(Obj_Id())
        neighbor_id  = Node_Id(Obj_Id())

        with Schema__Graph__Neighbors__Response(graph_ref    = graph_ref   ,
                                                node_id      = node_id     ,
                                                neighbor_ids = [neighbor_id],
                                                total_found  = 1           ) as _:
            assert len(_.neighbor_ids) == 1
            assert _.neighbor_ids[0]   == neighbor_id
            assert _.total_found       == 1

    # ═══════════════════════════════════════════════════════════════════════════════
    # Empty Results Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__no_neighbors(self):                                                           # Test isolated node with no neighbors
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))
        node_id   = Obj_Id()

        with Schema__Graph__Neighbors__Response(graph_ref    = graph_ref,
                                                node_id      = node_id  ,
                                                neighbor_ids = []       ,
                                                total_found  = 0        ) as _:
            assert len(_.neighbor_ids) == 0
            assert _.total_found       == 0

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Validation Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__graph_ref_field_types(self):                                                  # Test types within graph_ref
        graph_id     = Graph_Id(Obj_Id())
        cache_id     = Cache_Id(Random_Guid())
        node_id      = Obj_Id()
        neighbor_ids = [Obj_Id()]
        graph_ref    = Schema__Graph__Ref(graph_id  = graph_id ,
                                          cache_id  = cache_id ,
                                          namespace = 'type-ns')

        with Schema__Graph__Neighbors__Response(graph_ref    = graph_ref   ,
                                                node_id      = node_id     ,
                                                neighbor_ids = neighbor_ids,
                                                total_found  = 1           ) as _:
            assert type(_.graph_ref)           is Schema__Graph__Ref
            assert type(_.graph_ref.graph_id)  is Graph_Id
            assert type(_.graph_ref.cache_id)  is Cache_Id
            assert type(_.graph_ref.namespace) is Safe_Str__Id
            assert type(_.node_id)             is Node_Id
            assert type(_.neighbor_ids)        is Type_Safe__List
            assert type(_.total_found)         is Safe_UInt

    # ═══════════════════════════════════════════════════════════════════════════════
    # Serialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__serialization_round_trip__minimal(self):                                      # Test JSON round-trip with minimal data
        with Schema__Graph__Neighbors__Response() as original:
            json_data = original.json()

            with Schema__Graph__Neighbors__Response.from_json(json_data) as restored:
                assert restored.graph_ref   == original.graph_ref
                assert restored.node_id     == original.node_id
                assert restored.total_found == original.total_found

    def test__serialization_round_trip__complete(self):                                     # Test JSON round-trip with all fields
        graph_ref    = Schema__Graph__Ref(graph_id  = Graph_Id(Obj_Id())    ,
                                          cache_id  = Cache_Id(Random_Guid()),
                                          namespace = 'serial-ns'           )
        node_id      = Obj_Id()
        neighbor_ids = [Obj_Id(), Obj_Id()]

        with Schema__Graph__Neighbors__Response(graph_ref    = graph_ref   ,
                                                node_id      = node_id     ,
                                                neighbor_ids = neighbor_ids,
                                                total_found  = 2           ) as original:
            json_data = original.json()

            with Schema__Graph__Neighbors__Response.from_json(json_data) as restored:
                assert restored.graph_ref.graph_id  == original.graph_ref.graph_id
                assert restored.graph_ref.cache_id  == original.graph_ref.cache_id
                assert restored.graph_ref.namespace == original.graph_ref.namespace
                assert restored.node_id             == original.node_id
                assert restored.total_found         == original.total_found

    def test__serialization_preserves_types(self):                                          # Test that types are preserved
        graph_ref    = Schema__Graph__Ref(graph_id  = Graph_Id(Obj_Id()),
                                          namespace = 'type-test'       )
        node_id      = Node_Id()
        neighbor_ids = [Obj_Id()]

        with Schema__Graph__Neighbors__Response(graph_ref    = graph_ref   ,
                                                node_id      = node_id     ,
                                                neighbor_ids = neighbor_ids,
                                                total_found  = 1           ) as original:
            json_data = original.json()

            with Schema__Graph__Neighbors__Response.from_json(json_data) as restored:
                assert type(restored.graph_ref)           is Schema__Graph__Ref
                assert type(restored.graph_ref.graph_id)  is Graph_Id
                assert type(restored.graph_ref.namespace) is Safe_Str__Id
                assert type(restored.node_id)             is Node_Id
                assert type(restored.neighbor_ids)        is Type_Safe__List
                assert type(restored.total_found)         is Safe_UInt

    # ═══════════════════════════════════════════════════════════════════════════════
    # Edge Cases
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__default_namespace(self):                                                      # Test default namespace from Schema__Graph__Ref
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))                       # Uses default namespace

        with Schema__Graph__Neighbors__Response(graph_ref = graph_ref) as _:
            assert _.graph_ref.namespace == GRAPH_REF__DEFAULT_NAMESPACE

    def test__highly_connected_node(self):                                                  # Test node with many neighbors
        graph_ref    = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))
        node_id      = Obj_Id()
        neighbor_ids = [Obj_Id() for _ in range(100)]

        with Schema__Graph__Neighbors__Response(graph_ref    = graph_ref   ,
                                                node_id      = node_id     ,
                                                neighbor_ids = neighbor_ids,
                                                total_found  = 100         ) as _:
            assert len(_.neighbor_ids) == 100
            assert _.total_found       == 100

    def test__node_id_validity(self):                                                       # Test that node_id is a valid Obj_Id
        node_id   = Obj_Id()
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))

        with Schema__Graph__Neighbors__Response(graph_ref = graph_ref,
                                                node_id   = node_id  ) as _:
            assert len(_.node_id) == 8                                                     # Obj_Id format