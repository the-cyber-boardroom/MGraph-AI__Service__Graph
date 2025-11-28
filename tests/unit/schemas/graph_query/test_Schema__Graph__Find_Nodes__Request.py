from types                                                                                  import NoneType
from unittest                                                                               import TestCase
from osbot_utils.testing.__                                                                 import __
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                        import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.utils.Objects                                                              import base_classes
from mgraph_ai_service_cache_client.schemas.cache.Cache_Id                                  import Cache_Id
from mgraph_ai_service_graph.schemas.graph_ref.Graph_Id                                     import Graph_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref, GRAPH_REF__DEFAULT_NAMESPACE
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Request         import Schema__Graph__Find_Nodes__Request


class test_Schema__Graph__Find_Nodes__Request(TestCase):

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization
        with Schema__Graph__Find_Nodes__Request() as _:
            assert type(_)           is Schema__Graph__Find_Nodes__Request
            assert base_classes(_)   == [Type_Safe, object]
            assert _.graph_ref       is None                                                # Optional graph_ref
            assert _.node_type       is None                                                # Optional filter
            assert type(_.limit)     is Safe_UInt
            assert type(_.offset)    is Safe_UInt
            assert _.limit           == 100                                                 # Default value
            assert _.offset          == 0                                                   # Default value

    def test__init__field_types(self):                                                      # Test field types at initialization
        with Schema__Graph__Find_Nodes__Request() as _:
            assert type(_.graph_ref) is NoneType
            assert type(_.node_type) is NoneType
            assert type(_.limit)     is Safe_UInt
            assert type(_.offset)    is Safe_UInt

    def test__init__obj_comparison(self):                                                   # Test .obj() with default values
        with Schema__Graph__Find_Nodes__Request() as _:
            assert _.obj() == __(graph_ref = None,
                                 node_type = None,
                                 limit     = 100 ,
                                 offset    = 0   )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Value Assignment Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__with_graph_ref__graph_id(self):                                               # Test with graph_ref containing graph_id
        graph_id  = Graph_Id(Obj_Id())
        node_type = Safe_Str__Id('Person')
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id       ,
                                       namespace = 'test-namespace')

        with Schema__Graph__Find_Nodes__Request(graph_ref = graph_ref,
                                                node_type = node_type,
                                                limit     = 50       ,
                                                offset    = 10       ) as _:
            assert _.graph_ref.graph_id  == graph_id
            assert _.graph_ref.graph_id  != ''
            assert _.graph_ref.namespace == 'test-namespace'
            assert _.node_type           == node_type
            assert _.limit               == 50
            assert _.offset              == 10

    def test__with_graph_ref__cache_id(self):                                               # Test with graph_ref containing cache_id
        cache_id  = Cache_Id(Random_Guid())
        graph_ref = Schema__Graph__Ref(cache_id  = cache_id ,
                                       namespace = 'cache-ns')

        with Schema__Graph__Find_Nodes__Request(graph_ref = graph_ref) as _:
            assert _.graph_ref.cache_id  == cache_id
            assert _.graph_ref.cache_id  != ''

    def test__with_graph_ref__both_ids(self):                                               # Test with graph_ref containing both IDs
        graph_id  = Graph_Id(Obj_Id())
        cache_id  = Cache_Id(Random_Guid())
        node_type = Safe_Str__Id('Entity')
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id ,
                                       cache_id  = cache_id ,
                                       namespace = 'both-ns')

        with Schema__Graph__Find_Nodes__Request(graph_ref = graph_ref,
                                                node_type = node_type) as _:
            assert _.graph_ref.graph_id == graph_id
            assert _.graph_ref.cache_id == cache_id
            assert _.node_type          == node_type

    def test__with_custom_pagination(self):                                                 # Test with custom pagination values
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))

        with Schema__Graph__Find_Nodes__Request(graph_ref = graph_ref,
                                                limit     = 25       ,
                                                offset    = 100      ) as _:
            assert _.limit  == 25
            assert _.offset == 100

    def test__without_node_type_filter(self):                                               # Test finding all nodes (no type filter)
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))

        with Schema__Graph__Find_Nodes__Request(graph_ref = graph_ref) as _:
            assert _.node_type is None                                                      # No filter - find all

    # ═══════════════════════════════════════════════════════════════════════════════
    # Pagination Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__pagination_defaults(self):                                                    # Test default pagination values
        with Schema__Graph__Find_Nodes__Request() as _:
            assert _.limit  == 100                                                          # Default limit
            assert _.offset == 0                                                            # Default offset

    def test__pagination_first_page(self):                                                  # Test first page
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))

        with Schema__Graph__Find_Nodes__Request(graph_ref = graph_ref,
                                                limit     = 10       ,
                                                offset    = 0        ) as _:
            assert _.limit  == 10
            assert _.offset == 0

    def test__pagination_subsequent_page(self):                                             # Test subsequent page
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))

        with Schema__Graph__Find_Nodes__Request(graph_ref = graph_ref,
                                                limit     = 10       ,
                                                offset    = 30       ) as _:
            assert _.limit  == 10
            assert _.offset == 30                                                           # Page 4

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Validation Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__graph_ref_field_types(self):                                                  # Test types within graph_ref
        graph_id  = Graph_Id(Obj_Id())
        cache_id  = Cache_Id(Random_Guid())
        node_type = Safe_Str__Id('Item')
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id ,
                                       cache_id  = cache_id ,
                                       namespace = 'type-ns')

        with Schema__Graph__Find_Nodes__Request(graph_ref = graph_ref,
                                                node_type = node_type) as _:
            assert type(_.graph_ref)           is Schema__Graph__Ref
            assert type(_.graph_ref.graph_id)  is Graph_Id
            assert type(_.graph_ref.cache_id)  is Cache_Id
            assert type(_.graph_ref.namespace) is Safe_Str__Id
            assert type(_.node_type)           is Safe_Str__Id
            assert type(_.limit)               is Safe_UInt
            assert type(_.offset)              is Safe_UInt

    # ═══════════════════════════════════════════════════════════════════════════════
    # Serialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__serialization_round_trip__minimal(self):                                      # Test JSON round-trip with minimal data
        with Schema__Graph__Find_Nodes__Request() as original:
            json_data = original.json()

            with Schema__Graph__Find_Nodes__Request.from_json(json_data) as restored:
                assert restored.graph_ref == original.graph_ref
                assert restored.node_type == original.node_type
                assert restored.limit     == original.limit
                assert restored.offset    == original.offset

    def test__serialization_round_trip__complete(self):                                     # Test JSON round-trip with all fields
        graph_ref = Schema__Graph__Ref(graph_id  = Graph_Id(Obj_Id())    ,
                                       cache_id  = Cache_Id(Random_Guid()),
                                       namespace = 'serial-ns'           )
        node_type = Safe_Str__Id('Document')

        with Schema__Graph__Find_Nodes__Request(graph_ref = graph_ref,
                                                node_type = node_type,
                                                limit     = 25       ,
                                                offset    = 5        ) as original:
            json_data = original.json()

            with Schema__Graph__Find_Nodes__Request.from_json(json_data) as restored:
                assert restored.graph_ref.graph_id  == original.graph_ref.graph_id
                assert restored.graph_ref.cache_id  == original.graph_ref.cache_id
                assert restored.graph_ref.namespace == original.graph_ref.namespace
                assert restored.node_type           == original.node_type
                assert restored.limit               == original.limit
                assert restored.offset              == original.offset

    def test__serialization_preserves_types(self):                                          # Test that types are preserved
        graph_ref = Schema__Graph__Ref(graph_id  = Graph_Id(Obj_Id()),
                                       namespace = 'type-test'       )
        node_type = Safe_Str__Id('Entity')

        with Schema__Graph__Find_Nodes__Request(graph_ref = graph_ref,
                                                node_type = node_type) as original:
            json_data = original.json()

            with Schema__Graph__Find_Nodes__Request.from_json(json_data) as restored:
                assert type(restored.graph_ref)           is Schema__Graph__Ref
                assert type(restored.graph_ref.graph_id)  is Graph_Id
                assert type(restored.graph_ref.namespace) is Safe_Str__Id
                assert type(restored.node_type)           is Safe_Str__Id
                assert type(restored.limit)               is Safe_UInt
                assert type(restored.offset)              is Safe_UInt

    # ═══════════════════════════════════════════════════════════════════════════════
    # Edge Cases
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__default_namespace(self):                                                      # Test default namespace from Schema__Graph__Ref
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))                       # Uses default namespace

        with Schema__Graph__Find_Nodes__Request(graph_ref = graph_ref) as _:
            assert _.graph_ref.namespace == GRAPH_REF__DEFAULT_NAMESPACE

    def test__node_type_auto_conversion(self):                                              # Test node_type auto-converts from str
        graph_ref = Schema__Graph__Ref(graph_id = Graph_Id(Obj_Id()))

        with Schema__Graph__Find_Nodes__Request(graph_ref = graph_ref   ,
                                                node_type = 'CustomType') as _:
            assert type(_.node_type) is Safe_Str__Id
            assert _.node_type       == 'CustomType'