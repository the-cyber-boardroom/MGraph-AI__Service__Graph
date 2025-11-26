from unittest                                                                            import TestCase
from osbot_utils.testing.__                                                              import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                     import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                    import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Namespace   import Safe_Str__Namespace
from osbot_utils.utils.Objects                                                           import base_classes
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Request              import Schema__Graph__Get__Request
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Response             import Schema__Graph__Get__Response
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Request           import Schema__Graph__Create__Request
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Response          import Schema__Graph__Create__Response


class test_Schema__Graph__Get__Request(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Schema__Graph__Get__Request() as _:
            assert type(_)            is Schema__Graph__Get__Request
            assert base_classes(_)    == [Type_Safe, object]
            assert type(_.graph_id)   is Random_Guid
            assert type(_.namespace)  is Safe_Str__Namespace
            assert _.namespace        == "default"                                       # Default value

            assert _.obj() == __(graph_id  = _.graph_id ,                                # Auto-generated
                                 namespace = "default"  )

    def test__with_values(self):                                                         # Test with explicit values
        graph_id  = Random_Guid()
        namespace = Safe_Str__Namespace("test-namespace")

        with Schema__Graph__Get__Request(graph_id=graph_id, namespace=namespace) as _:
            assert _.graph_id  == graph_id
            assert _.namespace == namespace

            assert _.obj() == __(graph_id  = graph_id       ,
                                 namespace = "test-namespace")

    def test__serialization_round_trip(self):                                            # Test JSON round-trip
        with Schema__Graph__Get__Request(namespace="my-namespace") as original:
            json_data = original.json()

            with Schema__Graph__Get__Request.from_json(json_data) as restored:
                assert restored.obj() == original.obj()
                assert type(restored.graph_id)  is Random_Guid
                assert type(restored.namespace) is Safe_Str__Namespace


class test_Schema__Graph__Get__Response(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Schema__Graph__Get__Response() as _:
            assert type(_)             is Schema__Graph__Get__Response
            assert base_classes(_)     == [Type_Safe, object]
            assert type(_.graph_id)    is Random_Guid
            assert type(_.node_count)  is Safe_UInt
            assert type(_.edge_count)  is Safe_UInt
            assert type(_.cached)      is bool
            assert _.cache_id          is None                                           # Optional field

            assert _.obj() == __(graph_id   = _.graph_id ,
                                 node_count = 0          ,
                                 edge_count = 0          ,
                                 cached     = False      ,
                                 cache_id   = None       )

    def test__with_values(self):                                                         # Test with explicit values
        graph_id = Random_Guid()
        cache_id = Random_Guid()

        with Schema__Graph__Get__Response(graph_id   = graph_id ,
                                          node_count = 10       ,
                                          edge_count = 5        ,
                                          cached     = True     ,
                                          cache_id   = cache_id ) as _:
            assert _.graph_id   == graph_id
            assert _.node_count == 10
            assert _.edge_count == 5
            assert _.cached     is True
            assert _.cache_id   == cache_id

            assert _.obj() == __(graph_id   = graph_id ,
                                 node_count = 10       ,
                                 edge_count = 5        ,
                                 cached     = True     ,
                                 cache_id   = cache_id )

    def test__serialization_round_trip(self):                                            # Test JSON round-trip
        cache_id = Random_Guid()
        with Schema__Graph__Get__Response(node_count = 42      ,
                                          edge_count = 7       ,
                                          cached     = True    ,
                                          cache_id   = cache_id) as original:
            json_data = original.json()

            with Schema__Graph__Get__Response.from_json(json_data) as restored:
                assert restored.obj() == original.obj()
                assert type(restored.node_count) is Safe_UInt
                assert type(restored.edge_count) is Safe_UInt


class test_Schema__Graph__Create__Request(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Schema__Graph__Create__Request() as _:
            assert type(_)         is Schema__Graph__Create__Request
            assert base_classes(_) == [Type_Safe, object]
            assert _.graph_name    is None
            assert _.auto_cache    is True                                               # Default value
            assert _.namespace     == "default"                                          # Default value

    def test__with_values(self):                                                         # Test with explicit values
        with Schema__Graph__Create__Request(graph_name = "my-graph"  ,
                                            auto_cache = False       ,
                                            namespace  = "custom-ns" ) as _:
            assert _.graph_name == "my-graph"
            assert _.auto_cache is False
            assert _.namespace  == "custom-ns"


class test_Schema__Graph__Create__Response(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Schema__Graph__Create__Response() as _:
            assert type(_)             is Schema__Graph__Create__Response
            assert base_classes(_)     == [Type_Safe, object]
            assert type(_.graph_id)    is Random_Guid
            assert type(_.node_count)  is Safe_UInt
            assert type(_.edge_count)  is Safe_UInt
            assert _.node_count        == 0
            assert _.edge_count        == 0
            assert _.cached            is False
            assert _.cache_id          is None

    def test__serialization_round_trip(self):                                            # Test JSON round-trip
        with Schema__Graph__Create__Response(node_count = 0    ,
                                             edge_count = 0    ,
                                             cached     = True ) as original:
            json_data = original.json()

            with Schema__Graph__Create__Response.from_json(json_data) as restored:
                assert restored.obj() == original.obj()