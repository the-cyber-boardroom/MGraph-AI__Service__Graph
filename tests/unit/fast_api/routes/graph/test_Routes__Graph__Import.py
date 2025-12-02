import inspect
import pytest
from unittest                                                                                   import TestCase
from fastapi                                                                                    import FastAPI
from mgraph_ai_service_graph.fast_api.routes.graph.Routes__Graph__Import                        import Routes__Graph__Import, TAG__ROUTES_GRAPH_IMPORT
from mgraph_ai_service_graph.utils.testing.Graph_Test_Helpers                                   import Graph_Test_Helpers
from mgraph_db.mgraph.MGraph                                                                    import MGraph
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.utils.Objects                                                                  import base_classes
from osbot_fast_api.api.routes.Fast_API__Routes                                                 import Fast_API__Routes
from mgraph_ai_service_graph.service.areas.Area__Graph__Import                                  import Area__Graph__Import
from mgraph_ai_service_graph.service.graph.Graph__Service                                       import Graph__Service
from mgraph_ai_service_graph.service.caching.Graph__Cache__Client                               import Graph__Cache__Client
from mgraph_ai_service_graph.schemas.graph_import.Schema__Graph__Import                         import Schema__Graph__Import__Request
from mgraph_ai_service_graph.schemas.graph_import.Schema__Graph__Import                         import Schema__Graph__Import__Compressed__Request
from mgraph_ai_service_graph.schemas.graph_import.Schema__Graph__Import                         import Schema__Graph__Import__Response
from tests.unit.Graph__Service__Fast_API__Test_Objs                                             import client_cache_service


class test_Routes__Graph__Import(TestCase):

    @classmethod
    def setUpClass(cls):
        pytest.skip("Graph_Test_Helpers needs refactoring")
        cls.cache_client, cls.cache_service = client_cache_service()                            # Create in-memory cache service
        cls.graph_cache_client              = Graph__Cache__Client(cache_client = cls.cache_client)
        cls.graph_service                   = Graph__Service      (graph_cache_client = cls.graph_cache_client)

        cls.area_import                     = Area__Graph__Import (graph_service = cls.graph_service)
        cls.routes                          = Routes__Graph__Import(area_import  = cls.area_import  )
        cls.graph_test_helpers              = Graph_Test_Helpers   (cache_client = cls.cache_client )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Helper Methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def _create_sample_graph_json(self) -> dict:                                                # Create a sample graph JSON for testing
        mgraph = MGraph()
        mgraph.edit().new_node()
        mgraph.edit().new_node()
        return mgraph.json()

    def _create_sample_graph_compressed_json(self) -> dict:                                     # Create a sample compressed graph JSON
        mgraph = MGraph()
        mgraph.edit().new_node()
        mgraph.edit().new_node()
        return mgraph.json__compressed()

    def _create_graph_with_edges_json(self) -> dict:                                            # Create graph with nodes and edges
        mgraph    = MGraph()
        node_1    = mgraph.edit().new_node()
        node_2    = mgraph.edit().new_node()
        node_1_id = node_1.node_id
        node_2_id = node_2.node_id
        mgraph.edit().new_edge(from_node_id=node_1_id, to_node_id=node_2_id)
        return mgraph.json()

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                     # Test auto-initialization
        with Routes__Graph__Import() as _:
            assert type(_)             is Routes__Graph__Import
            assert base_classes(_)     == [Fast_API__Routes, Type_Safe, object]
            assert _.tag               == TAG__ROUTES_GRAPH_IMPORT
            assert _.tag               == 'graph-import'
            assert type(_.area_import) is Area__Graph__Import

    def test__tag_constant(self):                                                               # Test tag constant
        assert TAG__ROUTES_GRAPH_IMPORT == 'graph-import'

    def test__area_dependency(self):                                                            # Test area class is injected
        with self.routes as _:
            assert _.area_import is not None
            assert type(_.area_import) is Area__Graph__Import
            assert _.area_import       is self.area_import                                      # Same instance as setup

    # ═══════════════════════════════════════════════════════════════════════════════
    # Method Signature Tests - Import JSON
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__import_graph__method_signature(self):                                             # Test import_graph method exists
        with Routes__Graph__Import() as _:
            assert hasattr(_, 'import_graph')
            assert callable(_.import_graph)

            sig    = inspect.signature(_.import_graph)
            params = list(sig.parameters.values())
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Import__Request
            assert sig.return_annotation == Schema__Graph__Import__Response

    # ═══════════════════════════════════════════════════════════════════════════════
    # Method Signature Tests - Import Compressed
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__import_graph_compressed__method_signature(self):                                  # Test import_graph_compressed method exists
        with Routes__Graph__Import() as _:
            assert hasattr(_, 'import_graph_compressed')
            assert callable(_.import_graph_compressed)

            sig    = inspect.signature(_.import_graph_compressed)
            params = list(sig.parameters.values())
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Import__Compressed__Request
            assert sig.return_annotation == Schema__Graph__Import__Response

    # ═══════════════════════════════════════════════════════════════════════════════
    # Setup Routes Test
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__setup_routes(self):                                                               # Test setup_routes method
        with Routes__Graph__Import(app=FastAPI()) as _:
            assert hasattr(_, 'setup_routes')
            assert callable(_.setup_routes)

            result = _.setup_routes()
            assert result is _                                                                  # Returns self for chaining

    def test__routes_paths(self):                                                               # Test that routes are registered
        with Routes__Graph__Import(app=FastAPI()) as _:
            _.setup_routes()
            paths = _.routes_paths()

            assert '/json'       in paths
            assert '/compressed' in paths

    # ═══════════════════════════════════════════════════════════════════════════════
    # Functional Tests - Import JSON
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__import_graph__via_route(self):                                                    # Test import via route
        with self.routes as _:
            graph_json = self._create_sample_graph_json()
            namespace  = 'test-routes-import'

            request  = Schema__Graph__Import__Request(graph_data  = graph_json,
                                                       namespace   = namespace ,
                                                       auto_cache  = True      ,
                                                       build_index = False     ,
                                                       validate    = True      )
            response = _.import_graph(request)

            assert type(response)       is Schema__Graph__Import__Response
            assert response.nodes_count >= 2
            assert response.cached      is True
            assert len(response.validation_errors) == 0

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id  = response.graph_ref.cache_id,
                                                              namespace = namespace                  )

    def test__import_graph__with_edges_via_route(self):                                         # Test import with edges
        with self.routes as _:
            graph_json = self._create_graph_with_edges_json()
            namespace  = 'test-routes-import-edges'

            request  = Schema__Graph__Import__Request(graph_data  = graph_json,
                                                       namespace   = namespace ,
                                                       auto_cache  = True      ,
                                                       build_index = False     ,
                                                       validate    = True      )
            response = _.import_graph(request)

            assert type(response)       is Schema__Graph__Import__Response
            assert response.nodes_count >= 2
            assert response.edges_count >= 1

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id  = response.graph_ref.cache_id,
                                                              namespace = namespace                  )

    def test__import_graph__with_index_via_route(self):                                         # Test import with index building
        with self.routes as _:
            graph_json = self._create_graph_with_edges_json()
            namespace  = 'test-routes-import-index'

            request  = Schema__Graph__Import__Request(graph_data  = graph_json,
                                                       namespace   = namespace ,
                                                       auto_cache  = True      ,
                                                       build_index = True      ,
                                                       validate    = True      )
            response = _.import_graph(request)

            assert type(response)        is Schema__Graph__Import__Response
            assert response.index_cached is True

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id  = response.graph_ref.cache_id,
                                                              namespace = namespace                  )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Functional Tests - Import Compressed
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__import_graph_compressed__via_route(self):                                         # Test compressed import via route
        with self.routes as _:
            compressed_json = self._create_sample_graph_compressed_json()
            namespace       = 'test-routes-import-compressed'

            request  = Schema__Graph__Import__Compressed__Request(graph_data  = compressed_json,
                                                                   namespace   = namespace      ,
                                                                   auto_cache  = True           ,
                                                                   build_index = False          )
            response = _.import_graph_compressed(request)

            assert type(response)       is Schema__Graph__Import__Response
            assert response.nodes_count >= 2
            assert response.cached      is True

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id  = response.graph_ref.cache_id,
                                                              namespace = namespace                  )

    def test__import_graph_compressed__with_index(self):                                        # Test compressed import with index
        with self.routes as _:
            compressed_json = self._create_sample_graph_compressed_json()
            namespace       = 'test-routes-import-compressed-index'

            request  = Schema__Graph__Import__Compressed__Request(graph_data  = compressed_json,
                                                                   namespace   = namespace      ,
                                                                   auto_cache  = True           ,
                                                                   build_index = True           )
            response = _.import_graph_compressed(request)

            assert type(response)        is Schema__Graph__Import__Response
            assert response.index_cached is True

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id  = response.graph_ref.cache_id,
                                                              namespace = namespace                  )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Validation Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__import_graph__invalid_data(self):                                                 # Test import with invalid data
        with self.routes as _:
            invalid_json = {'not': 'valid'}
            namespace    = 'test-routes-invalid'

            request  = Schema__Graph__Import__Request(graph_data  = invalid_json,
                                                       namespace   = namespace  ,
                                                       auto_cache  = True       ,
                                                       build_index = False      ,
                                                       validate    = True       )
            response = _.import_graph(request)

            assert type(response) is Schema__Graph__Import__Response
            assert len(response.validation_errors) > 0                                          # Has errors

    # ═══════════════════════════════════════════════════════════════════════════════
    # Delegation Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__routes_delegate_to_area(self):                                                    # Test routes properly delegate to area
        with self.routes as _:
            # Verify the area is used
            assert _.area_import is self.area_import

            # Both should handle the same request types
            graph_json = self._create_sample_graph_json()
            namespace  = 'test-delegation'

            request  = Schema__Graph__Import__Request(graph_data  = graph_json,
                                                       namespace   = namespace ,
                                                       auto_cache  = True      ,
                                                       build_index = False     ,
                                                       validate    = False     )

            route_result = _.import_graph(request)
            assert type(route_result) is Schema__Graph__Import__Response

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id  = route_result.graph_ref.cache_id,
                                                              namespace = namespace                      )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__import_and_verify_retrieval(self):                                                # Test full import and retrieval flow
        with self.routes as _:
            # Create a graph with known structure
            mgraph = MGraph()
            node_1 = mgraph.edit().new_node()
            node_2 = mgraph.edit().new_node()
            node_3 = mgraph.edit().new_node()
            mgraph.edit().new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
            mgraph.edit().new_edge(from_node_id=node_2.node_id, to_node_id=node_3.node_id)

            graph_json = mgraph.json()
            namespace  = 'test-full-flow'

            # Import via route
            request  = Schema__Graph__Import__Request(graph_data  = graph_json,
                                                       namespace   = namespace ,
                                                       auto_cache  = True      ,
                                                       build_index = True      ,
                                                       validate    = True      )
            response = _.import_graph(request)

            assert response.nodes_count == 3
            assert response.edges_count == 2
            assert response.cached      is True
            assert response.index_cached is True

            # Retrieve and verify using test helpers
            get_response = self.graph_test_helpers.get_graph_by_cache_id(cache_id  = response.graph_ref.cache_id,
                                                                          namespace = namespace                  )

            assert get_response.success is True
            retrieved = MGraph.from_json(get_response.mgraph)
            assert len(retrieved.graph.model.data.nodes) == 3
            assert len(retrieved.graph.model.data.edges) == 2

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id  = response.graph_ref.cache_id,
                                                              namespace = namespace                  )

    def test__multiple_imports(self):                                                           # Test multiple sequential imports
        with self.routes as _:
            namespace = 'test-multiple-imports'
            cache_ids = []

            # Import multiple graphs
            for i in range(3):
                graph_json = self._create_sample_graph_json()
                request    = Schema__Graph__Import__Request(graph_data  = graph_json,
                                                             namespace   = namespace ,
                                                             auto_cache  = True      ,
                                                             build_index = False     ,
                                                             validate    = False     )
                response = _.import_graph(request)

                assert type(response) is Schema__Graph__Import__Response
                assert response.cached is True
                cache_ids.append(response.graph_ref.cache_id)

            # Verify all are unique
            assert len(set(cache_ids)) == 3                                                     # All unique cache IDs

            # Cleanup all
            for cache_id in cache_ids:
                self.graph_test_helpers.delete_graph_by_cache_id(cache_id  = cache_id ,
                                                                  namespace = namespace)
