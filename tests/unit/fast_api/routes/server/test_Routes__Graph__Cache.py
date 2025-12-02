from unittest                                                            import TestCase
from mgraph_ai_service_graph.fast_api.routes.server.Routes__Graph__Cache import Routes__Graph__Cache
from mgraph_ai_service_graph.utils.testing.Graph_Test_Helpers            import Graph_Test_Helpers, NAMESPACE__GRAPH_TEST_HELPERS
from tests.unit.Graph__Service__Fast_API__Test_Objs                      import client_cache_service


class test_Routes__Graph__Cache(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.cache_client, cls.cache_service = client_cache_service()                                    # Create in-memory cache service
        cls.routes_graph_cache              = Routes__Graph__Cache(cache_client = cls.cache_client)
        cls.graph_test_helpers              = Graph_Test_Helpers  (cache_client = cls.cache_client)
        cls.create_response, _              = cls.graph_test_helpers.create_graph_with_nodes()
        cls.cache_utils                     = cls.graph_test_helpers.cache_utils()

    def test_SetUpClass(self):
        with self.routes_graph_cache as _:
            assert type(_) is Routes__Graph__Cache
            assert _.cache_client is self.cache_client

    def test_cache_ids(self):
        with self.routes_graph_cache as _:
            assert _.cache_ids(namespace=NAMESPACE__GRAPH_TEST_HELPERS) == [self.create_response.graph_ref.cache_id]

    def test_cache_hashes(self):
        with self.routes_graph_cache as _:
            cache_hashes = _.cache_hashes(namespace=NAMESPACE__GRAPH_TEST_HELPERS)
            cache_hash   = self.cache_utils.graph_ref__to__cache_hash(graph_ref=self.create_response.graph_ref)

            assert cache_hashes == [cache_hash]

    def test_cache_ids__cache_id__location(self):
        with self.routes_graph_cache as _:
            result = _.cache_ids(namespace=NAMESPACE__GRAPH_TEST_HELPERS)

            # Debug: Check class identity
            from osbot_utils.type_safe.primitives.domains.identifiers.Cache_Id import Cache_Id  as Expected_Cache_Id

            print(f"Expected Cache_Id id: {id(Expected_Cache_Id)}")
            print(f"Expected Cache_Id module: {Expected_Cache_Id.__module__}")

            if result:
                actual_type = type(result[0])
                print(f"Actual type id: {id(actual_type)}")
                print(f"Actual type module: {actual_type.__module__}")
                print(f"Same class? {actual_type is Expected_Cache_Id}")