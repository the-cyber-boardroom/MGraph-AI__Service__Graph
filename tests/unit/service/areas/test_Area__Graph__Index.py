import pytest
import inspect
from unittest                                                                                   import TestCase
from mgraph_ai_service_graph.utils.testing.Graph_Test_Helpers import Graph_Test_Helpers
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.utils.Objects                                                                  import base_classes
from mgraph_ai_service_graph.service.areas.Area__Graph__Index                                   import Area__Graph__Index
from mgraph_ai_service_graph.service.areas.Area__Graph__Index                                   import INDEX_DATA_FILE_ID__MAIN, INDEX_DATA_FILE_ID__VALUES
from mgraph_ai_service_graph.service.graph.Graph__Service                                       import Graph__Service
from mgraph_ai_service_graph.service.caching.Graph__Cache__Client                               import Graph__Cache__Client
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Full__Request            import Schema__Graph__Index__Request
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Full__Request            import Schema__Graph__Index__Full__Request
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Full__Response           import Schema__Graph__Index__Full__Response
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Full__Response           import Schema__Graph__Index__Main
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Full__Response           import Schema__Graph__Index__Values
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Node_Edges               import Schema__Graph__Index__Node_Edges__Request
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Node_Edges               import Schema__Graph__Index__Node_Edges__Response
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__By_Predicate             import Schema__Graph__Index__By_Predicate__Request
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__By_Predicate             import Schema__Graph__Index__By_Predicate__Response
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Value_Lookup             import Schema__Graph__Index__Value_Lookup__Request
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Value_Lookup             import Schema__Graph__Index__Value_Lookup__Response
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Stats                    import Schema__Graph__Index__Stats__Response
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__ReIndex                  import Schema__Graph__Index__ReIndex__Request
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__ReIndex                  import Schema__Graph__Index__ReIndex__Response
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                               import Schema__Graph__Ref

from tests.unit.Graph__Service__Fast_API__Test_Objs                                             import client_cache_service


class test_Area__Graph__Index(TestCase):

    @classmethod
    def setUpClass(cls):
        pytest.skip("Graph_Test_Helpers needs refactoring with the latest MGraph-DB changes")
        cls.cache_client, cls.cache_service = client_cache_service()
        cls.graph_cache_client              = Graph__Cache__Client(cache_client       = cls.cache_client        )
        cls.graph_service                   = Graph__Service      (graph_cache_client = cls.graph_cache_client  )
        cls.area_index                      = Area__Graph__Index  (graph_service      = cls.graph_service       )
        cls.graph_test_helpers              = Graph_Test_Helpers  (cache_client       = cls.cache_client        )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                     # Test auto-initialization
        with Area__Graph__Index() as _:
            assert type(_)               is Area__Graph__Index
            assert base_classes(_)       == [Type_Safe, object]
            assert type(_.graph_service) is Graph__Service

    def test__graph_service_dependency(self):                                                   # Test graph service is injected
        with Area__Graph__Index() as _:
            assert _.graph_service is not None
            assert type(_.graph_service) is Graph__Service

    def test__constants(self):                                                                  # Test module constants
        assert INDEX_DATA_FILE_ID__MAIN   == 'index__main'
        assert INDEX_DATA_FILE_ID__VALUES == 'index__values'

    # ═══════════════════════════════════════════════════════════════════════════════
    # Method Signature Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__method_signatures(self):                                                          # Test all methods exist
        with Area__Graph__Index() as _:
            assert hasattr(_, 'get_full_index')                                                 # Check all expected methods exist
            assert hasattr(_, 'get_node_edges')
            assert hasattr(_, 'get_by_predicate')
            assert hasattr(_, 'value_lookup')
            assert hasattr(_, 'get_stats')
            assert hasattr(_, 're_index')
            assert hasattr(_, 'cache_index')

            assert callable(_.get_full_index)                                                   # All should be callable
            assert callable(_.get_node_edges)
            assert callable(_.get_by_predicate)
            assert callable(_.value_lookup)
            assert callable(_.get_stats)
            assert callable(_.re_index)
            assert callable(_.cache_index)

    def test__get_full_index__method_signature(self):                                           # Test get_full_index signature
        with Area__Graph__Index() as _:
            sig    = inspect.signature(_.get_full_index)
            params = list(sig.parameters.values())

            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Index__Full__Request
            assert sig.return_annotation == Schema__Graph__Index__Full__Response

    def test__get_node_edges__method_signature(self):                                           # Test get_node_edges signature
        with Area__Graph__Index() as _:
            sig    = inspect.signature(_.get_node_edges)
            params = list(sig.parameters.values())

            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Index__Node_Edges__Request
            assert sig.return_annotation == Schema__Graph__Index__Node_Edges__Response

    def test__get_by_predicate__method_signature(self):                                         # Test get_by_predicate signature
        with Area__Graph__Index() as _:
            sig    = inspect.signature(_.get_by_predicate)
            params = list(sig.parameters.values())

            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Index__By_Predicate__Request
            assert sig.return_annotation == Schema__Graph__Index__By_Predicate__Response

    def test__value_lookup__method_signature(self):                                             # Test value_lookup signature
        with Area__Graph__Index() as _:
            sig    = inspect.signature(_.value_lookup)
            params = list(sig.parameters.values())

            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Index__Value_Lookup__Request
            assert sig.return_annotation == Schema__Graph__Index__Value_Lookup__Response

    def test__get_stats__method_signature(self):                                                # Test get_stats signature
        with Area__Graph__Index() as _:
            sig    = inspect.signature(_.get_stats)
            params = list(sig.parameters.values())

            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Index__Request
            assert sig.return_annotation == Schema__Graph__Index__Stats__Response

    def test__re_index__method_signature(self):                                                 # Test re_index signature
        with Area__Graph__Index() as _:
            sig    = inspect.signature(_.re_index)
            params = list(sig.parameters.values())

            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Index__ReIndex__Request
            assert sig.return_annotation == Schema__Graph__Index__ReIndex__Response

    def test__cache_index__method_signature(self):                                              # Test cache_index signature
        with Area__Graph__Index() as _:
            sig    = inspect.signature(_.cache_index)
            params = list(sig.parameters.values())

            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Index__Request

    # ═══════════════════════════════════════════════════════════════════════════════
    # Full Index Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__get_full_index__empty_graph(self):                                                # Test getting index of empty graph
        with self.area_index as _:
            create_response = self.graph_test_helpers.create_empty_graph()
            graph_ref       = create_response.graph_ref

            request  = Schema__Graph__Index__Full__Request(graph_ref      = graph_ref,
                                                           include_values = True     ,
                                                           from_cache     = False    )
            response = _.get_full_index(request)

            assert type(response)            is Schema__Graph__Index__Full__Response
            assert type(response.main_index) is Schema__Graph__Index__Main
            assert response.success          is True
            assert response.from_cache       is False

            assert response.main_index.nodes_by_type   == {}                                    # Empty graph has empty indexes
            assert response.main_index.nodes_types     == []
            assert response.main_index.edges_by_type   == {}
            assert response.main_index.edges_types     == []

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id=graph_ref.cache_id)

    def test__get_full_index__with_nodes(self):                                                 # Test getting index of graph with nodes
        with self.area_index as _:
            create_response, node_responses = self.graph_test_helpers.create_graph_with_nodes(node_count=3)
            graph_ref = node_responses[-1].graph_ref

            request  = Schema__Graph__Index__Full__Request(graph_ref      = graph_ref,
                                                           include_values = False    ,
                                                           from_cache     = False    )
            response = _.get_full_index(request)

            assert type(response)       is Schema__Graph__Index__Full__Response
            assert response.success     is True
            assert response.from_cache  is False

            assert len(response.main_index.nodes_types) >= 1                                    # Should have at least one node type
            assert response.values_index                is None                                 # Not requested

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id=graph_ref.cache_id)

    def test__get_full_index__with_values(self):                                                # Test getting index including values
        with self.area_index as _:
            create_response, node_responses = self.graph_test_helpers.create_graph_with_nodes(node_count=2)
            graph_ref = node_responses[-1].graph_ref

            request  = Schema__Graph__Index__Full__Request(graph_ref      = graph_ref,
                                                           include_values = True     ,
                                                           from_cache     = False    )
            response = _.get_full_index(request)

            assert type(response)             is Schema__Graph__Index__Full__Response
            assert response.success           is True
            assert response.values_index      is not None                                       # Values requested
            assert type(response.values_index) is Schema__Graph__Index__Values

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id=graph_ref.cache_id)

    def test__get_full_index__with_edges(self):                                                 # Test getting index of graph with edges
        with self.area_index as _:
            create_response, node_responses, edge_responses = self.graph_test_helpers.create_graph_with_edges(node_count=3)
            graph_ref = edge_responses[-1].graph_ref if edge_responses else node_responses[-1].graph_ref

            request  = Schema__Graph__Index__Full__Request(graph_ref      = graph_ref,
                                                           include_values = True     ,
                                                           from_cache     = False    )
            response = _.get_full_index(request)

            assert type(response)   is Schema__Graph__Index__Full__Response
            assert response.success is True

            assert len(response.main_index.edges_types) >= 1                                    # Should have edge types
            assert len(response.main_index.edges_to_nodes) >= 1                                 # Should have edge mappings

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id=graph_ref.cache_id)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Node Edges Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__get_node_edges__outgoing(self):                                                   # Test getting outgoing edges for a node
        with self.area_index as _:
            create_response, node_responses, edge_responses = self.graph_test_helpers.create_graph_with_edges(node_count=3)
            graph_ref = edge_responses[-1].graph_ref if edge_responses else node_responses[-1].graph_ref
            node_id   = node_responses[0].node_id                                               # First node should have outgoing edge

            request  = Schema__Graph__Index__Node_Edges__Request(graph_ref = graph_ref  ,
                                                                  node_id   = node_id   ,
                                                                  direction = 'outgoing')
            response = _.get_node_edges(request)

            assert type(response)         is Schema__Graph__Index__Node_Edges__Response
            assert response.outgoing_count >= 1                                                 # First node has outgoing edge
            assert len(response.outgoing_edges) >= 1

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id=graph_ref.cache_id)

    def test__get_node_edges__incoming(self):                                                   # Test getting incoming edges for a node
        with self.area_index as _:
            create_response, node_responses, edge_responses = self.graph_test_helpers.create_graph_with_edges(node_count=3)
            graph_ref = edge_responses[-1].graph_ref if edge_responses else node_responses[-1].graph_ref
            node_id   = node_responses[1].node_id                                               # Second node should have incoming edge

            request  = Schema__Graph__Index__Node_Edges__Request(graph_ref = graph_ref  ,
                                                                  node_id   = node_id   ,
                                                                  direction = 'incoming')
            response = _.get_node_edges(request)

            assert type(response)        is Schema__Graph__Index__Node_Edges__Response
            assert response.incoming_count >= 1                                                 # Second node has incoming edge
            assert len(response.incoming_edges) >= 1

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id=graph_ref.cache_id)

    def test__get_node_edges__both(self):                                                       # Test getting both directions
        with self.area_index as _:
            create_response, node_responses, edge_responses = self.graph_test_helpers.create_graph_with_edges(node_count=3)
            graph_ref = edge_responses[-1].graph_ref if edge_responses else node_responses[-1].graph_ref
            node_id   = node_responses[1].node_id                                               # Middle node has both

            request  = Schema__Graph__Index__Node_Edges__Request(graph_ref = graph_ref,
                                                                  node_id   = node_id ,
                                                                  direction = 'both'  )
            response = _.get_node_edges(request)

            assert type(response) is Schema__Graph__Index__Node_Edges__Response
            assert response.incoming_count >= 1                                                 # Has incoming
            assert response.outgoing_count >= 1                                                 # Has outgoing

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id=graph_ref.cache_id)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Stats Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__get_stats__empty_graph(self):                                                     # Test stats on empty graph
        with self.area_index as _:
            create_response = self.graph_test_helpers.create_empty_graph()
            graph_ref       = create_response.graph_ref

            request  = Schema__Graph__Index__Request(graph_ref=graph_ref)
            response = _.get_stats(request)

            assert type(response)       is Schema__Graph__Index__Stats__Response
            assert response.total_nodes == 0
            assert response.total_edges == 0

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id=graph_ref.cache_id)

    def test__get_stats__with_nodes_and_edges(self):                                            # Test stats with data
        with self.area_index as _:
            create_response, node_responses, edge_responses = self.graph_test_helpers.create_graph_with_edges(node_count=3)
            graph_ref = edge_responses[-1].graph_ref if edge_responses else node_responses[-1].graph_ref

            request  = Schema__Graph__Index__Request(graph_ref=graph_ref)
            response = _.get_stats(request)

            assert type(response)        is Schema__Graph__Index__Stats__Response
            assert response.total_nodes  >= 3                                                   # At least 3 nodes
            assert response.total_edges  >= 2                                                   # Chain of edges
            assert response.node_types_count >= 1
            assert response.edge_types_count >= 1

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id=graph_ref.cache_id)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Re-Index Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__re_index__basic(self):                                                            # Test basic re-indexing
        with self.area_index as _:
            create_response, node_responses = self.graph_test_helpers.create_graph_with_nodes(node_count=2)
            graph_ref = node_responses[-1].graph_ref

            request  = Schema__Graph__Index__ReIndex__Request(graph_ref   = graph_ref,
                                                               cache_index = False   )
            response = _.re_index(request)

            assert type(response)          is Schema__Graph__Index__ReIndex__Response
            assert response.nodes_indexed  >= 2
            assert response.index_cached   is False                                             # Not requested

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id=graph_ref.cache_id)

    def test__re_index__with_caching(self):                                                     # Test re-index with cache
        with self.area_index as _:
            create_response, node_responses = self.graph_test_helpers.create_graph_with_nodes(node_count=2)
            graph_ref = node_responses[-1].graph_ref

            request  = Schema__Graph__Index__ReIndex__Request(graph_ref   = graph_ref,
                                                               cache_index = True    )
            response = _.re_index(request)

            assert type(response)          is Schema__Graph__Index__ReIndex__Response
            assert response.nodes_indexed  >= 2
            assert response.index_cached   is True                                              # Should be cached

            # Verify cache by fetching with from_cache=True
            fetch_request = Schema__Graph__Index__Full__Request(graph_ref      = graph_ref,
                                                                 include_values = False    ,
                                                                 from_cache     = True     )
            fetch_response = _.get_full_index(fetch_request)
            assert fetch_response.from_cache is True                                            # Should come from cache

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id=graph_ref.cache_id)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Cache Index Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__cache_index(self):                                                                # Test manual cache index
        with self.area_index as _:
            create_response, node_responses = self.graph_test_helpers.create_graph_with_nodes(node_count=2)
            graph_ref = node_responses[-1].graph_ref

            # First verify not cached
            fetch_request = Schema__Graph__Index__Full__Request(graph_ref      = graph_ref,
                                                                 include_values = False    ,
                                                                 from_cache     = True     )
            fetch_response = _.get_full_index(fetch_request)
            assert fetch_response.from_cache is False                                           # Not yet cached

            # Cache the index
            cache_request = Schema__Graph__Index__Request(graph_ref=graph_ref)
            _.cache_index(cache_request)

            # Now verify cached
            fetch_response_2 = _.get_full_index(fetch_request)
            assert fetch_response_2.from_cache is True                                          # Now cached

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id=graph_ref.cache_id)
