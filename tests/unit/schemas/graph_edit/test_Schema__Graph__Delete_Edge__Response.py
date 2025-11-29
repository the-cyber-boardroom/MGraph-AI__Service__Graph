from types                                                                                  import NoneType
from unittest                                                                               import TestCase
from mgraph_ai_service_graph.schemas.graph_ref.Edge_Id                                      import Edge_Id
from osbot_utils.testing.__                                                                 import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.utils.Objects                                                              import base_classes
from mgraph_ai_service_cache_client.schemas.cache.Cache_Id                                  import Cache_Id
from mgraph_ai_service_graph.schemas.graph_ref.Graph_Id                                     import Graph_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref, GRAPH_REF__DEFAULT_NAMESPACE
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Delete_Edge__Response  import Schema__Graph__Delete_Edge__Response


class test_Schema__Graph__Delete_Edge__Response(TestCase):

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization
        with Schema__Graph__Delete_Edge__Response() as _:
            assert type(_)         is Schema__Graph__Delete_Edge__Response
            assert base_classes(_) == [Type_Safe, object]
            assert _.graph_ref     is None                                                  # Optional until set
            assert _.edge_id       is None                                                  # No edge_id yet
            assert _.deleted       is False                                                 # Default value

    def test__init__field_types(self):                                                      # Test field types at initialization
        with Schema__Graph__Delete_Edge__Response() as _:
            assert type(_.graph_ref) is NoneType
            assert type(_.edge_id)   is NoneType
            assert type(_.deleted)   is bool

    def test__init__obj_comparison(self):                                                   # Test .obj() with default values
        with Schema__Graph__Delete_Edge__Response() as _:
            assert _.obj() == __(graph_ref = None ,
                                 edge_id   = None ,
                                 deleted   = False)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Value Assignment Tests - Success Cases
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__with_graph_ref__deleted_true(self):                                           # Test successful edge deletion
        graph_id  = Graph_Id(Obj_Id())
        cache_id  = Cache_Id(Random_Guid())
        edge_id   = Edge_Id(Obj_Id())
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id       ,
                                       cache_id  = cache_id       ,
                                       namespace = 'test-namespace')

        with Schema__Graph__Delete_Edge__Response(graph_ref = graph_ref,
                                                  edge_id   = edge_id  ,
                                                  deleted   = True     ) as _:
            assert _.graph_ref.graph_id  == graph_id
            assert _.graph_ref.cache_id  == cache_id
            assert _.graph_ref.namespace == 'test-namespace'
            assert _.edge_id             == edge_id
            assert _.deleted             is True

    def test__with_graph_ref__deleted_false(self):                                          # Test failed edge deletion (not found)
        graph_id  = Graph_Id(Obj_Id())
        edge_id   = Edge_Id(Obj_Id())
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id,
                                       namespace = 'fail-ns')

        with Schema__Graph__Delete_Edge__Response(graph_ref = graph_ref,
                                                  edge_id   = edge_id  ,
                                                  deleted   = False    ) as _:
            assert _.graph_ref.graph_id == graph_id
            assert _.edge_id            == edge_id
            assert _.deleted            is False

    def test__with_cache_id_lookup(self):                                                   # Test deletion when graph was found by cache_id
        cache_id  = Cache_Id(Random_Guid())
        graph_id  = Graph_Id(Obj_Id())
        edge_id   = Edge_Id(Obj_Id())
        graph_ref = Schema__Graph__Ref(cache_id  = cache_id ,
                                       graph_id  = graph_id ,                               # Resolved after lookup
                                       namespace = 'cache-ns')

        with Schema__Graph__Delete_Edge__Response(graph_ref = graph_ref,
                                                  edge_id   = edge_id  ,
                                                  deleted   = True     ) as _:
            assert _.graph_ref.cache_id == cache_id
            assert _.graph_ref.graph_id == graph_id
            assert _.edge_id            == edge_id
            assert _.deleted            is True

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Validation Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__graph_ref_field_types(self):                                                  # Test types within graph_ref
        graph_id  = Graph_Id(Obj_Id())
        cache_id  = Cache_Id(Random_Guid())
        edge_id   = Obj_Id()
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id ,
                                       cache_id  = cache_id ,
                                       namespace = 'type-ns')

        with Schema__Graph__Delete_Edge__Response(graph_ref = graph_ref,
                                                  edge_id   = edge_id  ,
                                                  deleted   = True     ) as _:
            assert type(_.graph_ref)           is Schema__Graph__Ref
            assert type(_.graph_ref.graph_id)  is Graph_Id
            assert type(_.graph_ref.cache_id)  is Cache_Id
            assert type(_.graph_ref.namespace) is Safe_Str__Id
            assert type(_.edge_id)             is Edge_Id
            assert type(_.deleted)             is bool

    # ═══════════════════════════════════════════════════════════════════════════════
    # Serialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__serialization_round_trip__minimal(self):                                      # Test JSON round-trip with minimal data
        with Schema__Graph__Delete_Edge__Response(deleted = False) as original:
            json_data = original.json()

            with Schema__Graph__Delete_Edge__Response.from_json(json_data) as restored:
                assert restored.graph_ref == original.graph_ref
                assert restored.edge_id   == original.edge_id
                assert restored.deleted   == original.deleted

    def test__serialization_round_trip__complete(self):                                     # Test JSON round-trip with all fields
        graph_ref = Schema__Graph__Ref(graph_id  = Graph_Id(Obj_Id())    ,
                                       cache_id  = Cache_Id(Random_Guid()),
                                       namespace = 'serial-ns'           )
        edge_id   = Obj_Id()

        with Schema__Graph__Delete_Edge__Response(graph_ref = graph_ref,
                                                  edge_id   = edge_id  ,
                                                  deleted   = True     ) as original:
            json_data = original.json()

            with Schema__Graph__Delete_Edge__Response.from_json(json_data) as restored:
                assert restored.graph_ref.graph_id  == original.graph_ref.graph_id
                assert restored.graph_ref.cache_id  == original.graph_ref.cache_id
                assert restored.graph_ref.namespace == original.graph_ref.namespace
                assert restored.edge_id             == original.edge_id
                assert restored.deleted             == original.deleted

    def test__serialization_preserves_types(self):                                          # Test that types are preserved after serialization
        graph_ref = Schema__Graph__Ref(graph_id  = Graph_Id(Obj_Id())    ,
                                       cache_id  = Cache_Id(Random_Guid()),
                                       namespace = 'type-test'           )
        edge_id   = Obj_Id()

        with Schema__Graph__Delete_Edge__Response(graph_ref = graph_ref,
                                                  edge_id   = edge_id  ,
                                                  deleted   = True     ) as original:
            json_data = original.json()

            with Schema__Graph__Delete_Edge__Response.from_json(json_data) as restored:
                assert type(restored.graph_ref)           is Schema__Graph__Ref
                assert type(restored.graph_ref.graph_id)  is Graph_Id
                assert type(restored.graph_ref.cache_id)  is Cache_Id
                assert type(restored.graph_ref.namespace) is Safe_Str__Id
                assert type(restored.edge_id)             is Edge_Id

    # ═══════════════════════════════════════════════════════════════════════════════
    # Edge Cases
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__default_namespace(self):                                                      # Test default namespace from Schema__Graph__Ref
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))                       # Uses default namespace

        with Schema__Graph__Delete_Edge__Response(graph_ref = graph_ref,
                                                  deleted   = True     ) as _:
            assert _.graph_ref.namespace == GRAPH_REF__DEFAULT_NAMESPACE

    def test__edge_id_validity(self):                                                       # Test that edge_id is a valid Obj_Id
        edge_id   = Obj_Id()
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))

        with Schema__Graph__Delete_Edge__Response(graph_ref = graph_ref,
                                                  edge_id   = edge_id  ,
                                                  deleted   = True     ) as _:
            assert len(_.edge_id) == 8                                                      # Obj_id format

    def test__delete_nonexistent_edge(self):                                                # Test deleting an edge that doesn't exist
        edge_id   = Edge_Id(Obj_Id())
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))

        with Schema__Graph__Delete_Edge__Response(graph_ref = graph_ref,
                                                  edge_id   = edge_id  ,
                                                  deleted   = False    ) as _:
            assert _.edge_id == edge_id
            assert _.deleted is False                                                       # Edge wasn't found/deleted