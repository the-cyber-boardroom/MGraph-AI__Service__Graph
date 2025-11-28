from types                                                                                  import NoneType
from unittest                                                                               import TestCase
from osbot_utils.testing.__                                                                 import __
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
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Edges__Response        import Schema__Graph__Find_Edges__Response
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Edge__Data                  import Schema__Graph__Edge__Data


class test_Schema__Graph__Find_Edges__Response(TestCase):

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization
        with Schema__Graph__Find_Edges__Response() as _:
            assert type(_)             is Schema__Graph__Find_Edges__Response
            assert base_classes(_)     == [Type_Safe, object]
            assert _.graph_ref         is None                                              # Optional graph_ref
            assert _.edge_type         is None                                              # Filter used
            assert type(_.edges)       is Type_Safe__List                                   # List of edges
            assert type(_.total_found) is Safe_UInt

    def test__init__field_types(self):                                                      # Test field types at initialization
        with Schema__Graph__Find_Edges__Response() as _:
            assert type(_.graph_ref)   is NoneType
            assert type(_.edge_type)   is NoneType
            assert type(_.edges)       is Type_Safe__List
            assert type(_.total_found) is Safe_UInt

    def test__init__obj_comparison(self):                                                   # Test .obj() with default values
        with Schema__Graph__Find_Edges__Response() as _:
            assert _.obj() == __(graph_ref   = None,
                                 edge_type   = None,
                                 edges       = []  ,
                                 total_found = 0   )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Value Assignment Tests - Success Cases
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__with_graph_ref__results(self):                                                # Test with edges found
        graph_id  = Graph_Id(Obj_Id())
        cache_id  = Cache_Id(Random_Guid())
        edge_type = Safe_Str__Id('KNOWS')
        edge      = Schema__Graph__Edge__Data(edge_type = edge_type)
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id       ,
                                       cache_id  = cache_id       ,
                                       namespace = 'test-namespace')

        with Schema__Graph__Find_Edges__Response(graph_ref   = graph_ref,
                                                 edge_type   = edge_type,
                                                 edges       = [edge]   ,
                                                 total_found = 1        ) as _:
            assert _.graph_ref.graph_id  == graph_id
            assert _.graph_ref.cache_id  == cache_id
            assert _.graph_ref.namespace == 'test-namespace'
            assert _.edge_type           == edge_type
            assert len(_.edges)          == 1
            assert _.total_found         == 1

    def test__with_cache_id_lookup(self):                                                   # Test response when graph was found by cache_id
        cache_id  = Cache_Id(Random_Guid())
        graph_id  = Graph_Id(Obj_Id())
        edge_type = Safe_Str__Id('RELATES')
        edges     = [Schema__Graph__Edge__Data(edge_type = edge_type),
                     Schema__Graph__Edge__Data(edge_type = edge_type)]
        graph_ref = Schema__Graph__Ref(cache_id  = cache_id ,
                                       graph_id  = graph_id ,                               # Resolved after lookup
                                       namespace = 'cache-ns')

        with Schema__Graph__Find_Edges__Response(graph_ref   = graph_ref,
                                                 edge_type   = edge_type,
                                                 edges       = edges    ,
                                                 total_found = 2        ) as _:
            assert _.graph_ref.cache_id == cache_id
            assert _.graph_ref.graph_id == graph_id
            assert len(_.edges)         == 2
            assert _.total_found        == 2

    def test__with_multiple_edges(self):                                                    # Test with multiple edges
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))
        edge_type = Safe_Str__Id('CONNECTS')
        edges     = [Schema__Graph__Edge__Data(edge_type = edge_type) for _ in range(5)]

        with Schema__Graph__Find_Edges__Response(graph_ref   = graph_ref,
                                                 edge_type   = edge_type,
                                                 edges       = edges    ,
                                                 total_found = 5        ) as _:
            assert len(_.edges)  == 5
            assert _.total_found == 5

    # ═══════════════════════════════════════════════════════════════════════════════
    # Empty Results Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__empty_results(self):                                                          # Test with no results
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))
        edge_type = Safe_Str__Id('NONEXISTENT')

        with Schema__Graph__Find_Edges__Response(graph_ref   = graph_ref,
                                                 edge_type   = edge_type,
                                                 edges       = []       ,
                                                 total_found = 0        ) as _:
            assert len(_.edges)  == 0
            assert _.total_found == 0

    def test__all_edges_no_filter(self):                                                    # Test finding all edges (no type filter)
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))
        edge1     = Schema__Graph__Edge__Data(edge_type = Safe_Str__Id('KNOWS'))
        edge2     = Schema__Graph__Edge__Data(edge_type = Safe_Str__Id('LIKES'))

        with Schema__Graph__Find_Edges__Response(graph_ref   = graph_ref    ,
                                                 edge_type   = None         ,               # No filter
                                                 edges       = [edge1, edge2],
                                                 total_found = 2            ) as _:
            assert _.edge_type   is None
            assert len(_.edges)  == 2
            assert _.total_found == 2

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Validation Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__graph_ref_field_types(self):                                                  # Test types within graph_ref
        graph_id  = Graph_Id(Obj_Id())
        cache_id  = Cache_Id(Random_Guid())
        edge_type = Safe_Str__Id('HAS')
        edge      = Schema__Graph__Edge__Data(edge_type = edge_type)
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id ,
                                       cache_id  = cache_id ,
                                       namespace = 'type-ns')

        with Schema__Graph__Find_Edges__Response(graph_ref   = graph_ref,
                                                 edge_type   = edge_type,
                                                 edges       = [edge]   ,
                                                 total_found = 1        ) as _:
            assert type(_.graph_ref)           is Schema__Graph__Ref
            assert type(_.graph_ref.graph_id)  is Graph_Id
            assert type(_.graph_ref.cache_id)  is Cache_Id
            assert type(_.graph_ref.namespace) is Safe_Str__Id
            assert type(_.edge_type)           is Safe_Str__Id
            assert type(_.edges)               is Type_Safe__List
            assert type(_.total_found)         is Safe_UInt

    def test__edge_data_types(self):                                                        # Test types within edge data
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))
        edge_type = Safe_Str__Id('OWNS')
        edge      = Schema__Graph__Edge__Data(edge_type = edge_type)

        with Schema__Graph__Find_Edges__Response(graph_ref   = graph_ref,
                                                 edge_type   = edge_type,
                                                 edges       = [edge]   ,
                                                 total_found = 1        ) as _:
            assert type(_.edges[0]) is Schema__Graph__Edge__Data

    # ═══════════════════════════════════════════════════════════════════════════════
    # Serialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__serialization_round_trip__minimal(self):                                      # Test JSON round-trip with minimal data
        with Schema__Graph__Find_Edges__Response() as original:
            json_data = original.json()

            with Schema__Graph__Find_Edges__Response.from_json(json_data) as restored:
                assert restored.graph_ref   == original.graph_ref
                assert restored.edge_type   == original.edge_type
                assert restored.total_found == original.total_found

    def test__serialization_round_trip__complete(self):                                     # Test JSON round-trip with all fields
        graph_ref = Schema__Graph__Ref(graph_id  = Graph_Id(Obj_Id())    ,
                                       cache_id  = Cache_Id(Random_Guid()),
                                       namespace = 'serial-ns'           )
        edge_type = Safe_Str__Id('LINKS')
        edge      = Schema__Graph__Edge__Data(edge_type = edge_type)

        with Schema__Graph__Find_Edges__Response(graph_ref   = graph_ref,
                                                 edge_type   = edge_type,
                                                 edges       = [edge]   ,
                                                 total_found = 1        ) as original:
            json_data = original.json()

            with Schema__Graph__Find_Edges__Response.from_json(json_data) as restored:
                assert restored.graph_ref.graph_id  == original.graph_ref.graph_id
                assert restored.graph_ref.cache_id  == original.graph_ref.cache_id
                assert restored.graph_ref.namespace == original.graph_ref.namespace
                assert restored.edge_type           == original.edge_type
                assert restored.total_found         == original.total_found

    def test__serialization_preserves_types(self):                                          # Test that types are preserved
        graph_ref = Schema__Graph__Ref(graph_id  = Graph_Id(Obj_Id()),
                                       namespace = 'type-test'       )
        edge_type = Safe_Str__Id('USES')
        edge      = Schema__Graph__Edge__Data(edge_type = edge_type)

        with Schema__Graph__Find_Edges__Response(graph_ref   = graph_ref,
                                                 edge_type   = edge_type,
                                                 edges       = [edge]   ,
                                                 total_found = 1        ) as original:
            json_data = original.json()

            with Schema__Graph__Find_Edges__Response.from_json(json_data) as restored:
                assert type(restored.graph_ref)           is Schema__Graph__Ref
                assert type(restored.graph_ref.graph_id)  is Graph_Id
                assert type(restored.graph_ref.namespace) is Safe_Str__Id
                assert type(restored.edge_type)           is Safe_Str__Id
                assert type(restored.edges)               is Type_Safe__List
                assert type(restored.total_found)         is Safe_UInt

    # ═══════════════════════════════════════════════════════════════════════════════
    # Edge Cases
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__default_namespace(self):                                                      # Test default namespace from Schema__Graph__Ref
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))                       # Uses default namespace

        with Schema__Graph__Find_Edges__Response(graph_ref = graph_ref) as _:
            assert _.graph_ref.namespace == GRAPH_REF__DEFAULT_NAMESPACE

    def test__large_result_set(self):                                                       # Test with large number of edges
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))
        edge_type = Safe_Str__Id('BATCH')
        edges     = [Schema__Graph__Edge__Data(edge_type = edge_type) for _ in range(50)]

        with Schema__Graph__Find_Edges__Response(graph_ref   = graph_ref,
                                                 edge_type   = edge_type,
                                                 edges       = edges    ,
                                                 total_found = 50       ) as _:
            assert len(_.edges)  == 50
            assert _.total_found == 50