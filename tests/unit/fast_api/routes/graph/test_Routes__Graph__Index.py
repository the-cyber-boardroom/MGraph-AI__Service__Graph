import pytest
import inspect
from unittest                                                                                   import TestCase
from fastapi                                                                                    import FastAPI
from mgraph_ai_service_graph.fast_api.routes.graph.Routes__Graph__Index                         import Routes__Graph__Index, TAG__ROUTES_GRAPH_INDEX
from mgraph_ai_service_graph.utils.testing.Graph_Test_Helpers                                   import Graph_Test_Helpers
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.utils.Objects                                                                  import base_classes
from osbot_fast_api.api.routes.Fast_API__Routes                                                 import Fast_API__Routes
from mgraph_ai_service_graph.service.areas.Area__Graph__Index                                   import Area__Graph__Index
from mgraph_ai_service_graph.service.graph.Graph__Service                                       import Graph__Service
from mgraph_ai_service_graph.service.caching.Graph__Cache__Client                               import Graph__Cache__Client
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Full__Request            import Schema__Graph__Index__Request
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Full__Request            import Schema__Graph__Index__Full__Request
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Full__Response           import Schema__Graph__Index__Full__Response
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Node_Edges               import Schema__Graph__Index__Node_Edges__Request
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Node_Edges               import Schema__Graph__Index__Node_Edges__Response
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__By_Predicate             import Schema__Graph__Index__By_Predicate__Request
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__By_Predicate             import Schema__Graph__Index__By_Predicate__Response
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Value_Lookup             import Schema__Graph__Index__Value_Lookup__Request
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Value_Lookup             import Schema__Graph__Index__Value_Lookup__Response
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Stats                    import Schema__Graph__Index__Stats__Response
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__ReIndex                  import Schema__Graph__Index__ReIndex__Request
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__ReIndex                  import Schema__Graph__Index__ReIndex__Response
from tests.unit.Graph__Service__Fast_API__Test_Objs                                             import client_cache_service


class test_Routes__Graph__Index(TestCase):

    @classmethod
    def setUpClass(cls):
        pytest.skip("Graph_Test_Helpers needs refactoring with the latest MGraph-DB changes")
        cls.cache_client, cls.cache_service = client_cache_service()                            # Create in-memory cache service
        cls.graph_cache_client              = Graph__Cache__Client(cache_client = cls.cache_client)
        cls.graph_service                   = Graph__Service      (graph_cache_client = cls.graph_cache_client)

        cls.area_index                      = Area__Graph__Index  (graph_service = cls.graph_service,
                                                                   cache_client  = cls.cache_client )
        cls.routes                          = Routes__Graph__Index(area_index    = cls.area_index   )
        cls.graph_test_helpers              = Graph_Test_Helpers  (cache_client  = cls.cache_client )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                     # Test auto-initialization
        with Routes__Graph__Index() as _:
            assert type(_)             is Routes__Graph__Index
            assert base_classes(_)     == [Fast_API__Routes, Type_Safe, object]
            assert _.tag               == TAG__ROUTES_GRAPH_INDEX
            assert _.tag               == 'graph-index'
            assert type(_.area_index)  is Area__Graph__Index

    def test__tag_constant(self):                                                               # Test tag constant
        assert TAG__ROUTES_GRAPH_INDEX == 'graph-index'

    def test__area_dependency(self):                                                            # Test area class is injected
        with self.routes as _:
            assert _.area_index is not None
            assert type(_.area_index) is Area__Graph__Index
            assert _.area_index       is self.area_index                                        # Same instance as setup

    # ═══════════════════════════════════════════════════════════════════════════════
    # Method Signature Tests - Full Index
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__get_full_index__method_signature(self):                                           # Test get_full_index method exists
        with Routes__Graph__Index() as _:
            assert hasattr(_, 'get_full_index')
            assert callable(_.get_full_index)

            sig    = inspect.signature(_.get_full_index)
            params = list(sig.parameters.values())
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Index__Full__Request
            assert sig.return_annotation == Schema__Graph__Index__Full__Response

    # ═══════════════════════════════════════════════════════════════════════════════
    # Method Signature Tests - Node Edges
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__get_node_edges__method_signature(self):                                           # Test get_node_edges method exists
        with Routes__Graph__Index() as _:
            assert hasattr(_, 'get_node_edges')
            assert callable(_.get_node_edges)

            sig    = inspect.signature(_.get_node_edges)
            params = list(sig.parameters.values())
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Index__Node_Edges__Request
            assert sig.return_annotation == Schema__Graph__Index__Node_Edges__Response

    # ═══════════════════════════════════════════════════════════════════════════════
    # Method Signature Tests - By Predicate
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__get_by_predicate__method_signature(self):                                         # Test get_by_predicate method exists
        with Routes__Graph__Index() as _:
            assert hasattr(_, 'get_by_predicate')
            assert callable(_.get_by_predicate)

            sig    = inspect.signature(_.get_by_predicate)
            params = list(sig.parameters.values())
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Index__By_Predicate__Request
            assert sig.return_annotation == Schema__Graph__Index__By_Predicate__Response

    # ═══════════════════════════════════════════════════════════════════════════════
    # Method Signature Tests - Value Lookup
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__value_lookup__method_signature(self):                                             # Test value_lookup method exists
        with Routes__Graph__Index() as _:
            assert hasattr(_, 'value_lookup')
            assert callable(_.value_lookup)

            sig    = inspect.signature(_.value_lookup)
            params = list(sig.parameters.values())
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Index__Value_Lookup__Request
            assert sig.return_annotation == Schema__Graph__Index__Value_Lookup__Response

    # ═══════════════════════════════════════════════════════════════════════════════
    # Method Signature Tests - Stats
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__get_stats__method_signature(self):                                                # Test get_stats method exists
        with Routes__Graph__Index() as _:
            assert hasattr(_, 'get_stats')
            assert callable(_.get_stats)

            sig    = inspect.signature(_.get_stats)
            params = list(sig.parameters.values())
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Index__Request
            assert sig.return_annotation == Schema__Graph__Index__Stats__Response

    # ═══════════════════════════════════════════════════════════════════════════════
    # Method Signature Tests - Re-Index
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__re_index__method_signature(self):                                                 # Test re_index method exists
        with Routes__Graph__Index() as _:
            assert hasattr(_, 're_index')
            assert callable(_.re_index)

            sig    = inspect.signature(_.re_index)
            params = list(sig.parameters.values())
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Index__ReIndex__Request
            assert sig.return_annotation == Schema__Graph__Index__ReIndex__Response

    # ═══════════════════════════════════════════════════════════════════════════════
    # Method Signature Tests - Cache Index
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__cache_index__method_signature(self):                                              # Test cache_index method exists
        with Routes__Graph__Index() as _:
            assert hasattr(_, 'cache_index')
            assert callable(_.cache_index)

            sig    = inspect.signature(_.cache_index)
            params = list(sig.parameters.values())
            assert len(params)          == 1
            assert params[0].name       == 'request'
            assert params[0].annotation == Schema__Graph__Index__Request

    # ═══════════════════════════════════════════════════════════════════════════════
    # Setup Routes Test
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__setup_routes(self):                                                               # Test setup_routes method
        with Routes__Graph__Index(app=FastAPI()) as _:
            assert hasattr(_, 'setup_routes')
            assert callable(_.setup_routes)

            result = _.setup_routes()
            assert result is _                                                                  # Returns self for chaining

    def test__routes_paths(self):                                                               # Test that routes are registered
        with Routes__Graph__Index(app=FastAPI()) as _:
            _.setup_routes()
            paths = _.routes_paths()

            assert '/full'         in paths
            assert '/node-edges'   in paths
            assert '/by-predicate' in paths
            assert '/value-lookup' in paths
            assert '/stats'        in paths
            assert '/re-index'     in paths
            assert '/cache'        in paths

    # ═══════════════════════════════════════════════════════════════════════════════
    # Functional Tests - Full Index
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__get_full_index__via_route(self):                                                  # Test full index via route
        with self.routes as _:
            create_response, node_responses = self.graph_test_helpers.create_graph_with_nodes(node_count=2)
            graph_ref = node_responses[-1].graph_ref

            request  = Schema__Graph__Index__Full__Request(graph_ref      = graph_ref,
                                                           include_values = False    ,
                                                           from_cache     = False    )
            response = _.get_full_index(request)

            assert type(response)   is Schema__Graph__Index__Full__Response
            assert response.success is True

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id=graph_ref.cache_id)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Functional Tests - Node Edges
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__get_node_edges__via_route(self):                                                  # Test node edges via route
        with self.routes as _:
            create_response, node_responses, edge_responses = self.graph_test_helpers.create_graph_with_edges(node_count=3)
            graph_ref = edge_responses[-1].graph_ref if edge_responses else node_responses[-1].graph_ref
            node_id   = node_responses[0].node_id

            request  = Schema__Graph__Index__Node_Edges__Request(graph_ref = graph_ref  ,
                                                                  node_id   = node_id   ,
                                                                  direction = 'outgoing')
            response = _.get_node_edges(request)

            assert type(response) is Schema__Graph__Index__Node_Edges__Response
            assert response.outgoing_count >= 1

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id=graph_ref.cache_id)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Functional Tests - Stats
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__get_stats__via_route(self):                                                       # Test stats via route
        with self.routes as _:
            create_response, node_responses, edge_responses = self.graph_test_helpers.create_graph_with_edges(node_count=3)
            graph_ref = edge_responses[-1].graph_ref if edge_responses else node_responses[-1].graph_ref

            request  = Schema__Graph__Index__Request(graph_ref=graph_ref)
            response = _.get_stats(request)

            assert type(response)       is Schema__Graph__Index__Stats__Response
            assert response.total_nodes >= 3
            assert response.total_edges >= 2

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id=graph_ref.cache_id)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Functional Tests - Re-Index
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__re_index__via_route(self):                                                        # Test re-index via route
        with self.routes as _:
            create_response, node_responses = self.graph_test_helpers.create_graph_with_nodes(node_count=2)
            graph_ref = node_responses[-1].graph_ref

            request  = Schema__Graph__Index__ReIndex__Request(graph_ref   = graph_ref,
                                                               cache_index = False   )
            response = _.re_index(request)

            assert type(response)         is Schema__Graph__Index__ReIndex__Response
            assert response.nodes_indexed >= 2

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id=graph_ref.cache_id)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Functional Tests - Cache Index
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__cache_index__via_route(self):                                                     # Test cache index via route
        with self.routes as _:
            create_response, node_responses = self.graph_test_helpers.create_graph_with_nodes(node_count=2)
            graph_ref = node_responses[-1].graph_ref

            # Cache the index
            cache_request = Schema__Graph__Index__Request(graph_ref=graph_ref)
            _.cache_index(cache_request)

            # Verify it's cached by fetching with from_cache=True
            fetch_request = Schema__Graph__Index__Full__Request(graph_ref      = graph_ref,
                                                                 include_values = False    ,
                                                                 from_cache     = True     )
            fetch_response = _.get_full_index(fetch_request)
            assert fetch_response.from_cache is True

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id=graph_ref.cache_id)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Delegation Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__routes_delegate_to_area(self):                                                    # Test routes properly delegate to area
        with self.routes as _:
            # Verify the area is used
            assert _.area_index is self.area_index

            # The route methods should call area methods
            create_response = self.graph_test_helpers.create_empty_graph()
            graph_ref       = create_response.graph_ref

            # Both should produce same result type
            request       = Schema__Graph__Index__Request(graph_ref=graph_ref)
            route_result  = _.get_stats(request)
            area_result   = self.area_index.get_stats(request)

            assert type(route_result) is type(area_result)
            assert type(route_result) is Schema__Graph__Index__Stats__Response

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id=graph_ref.cache_id)
