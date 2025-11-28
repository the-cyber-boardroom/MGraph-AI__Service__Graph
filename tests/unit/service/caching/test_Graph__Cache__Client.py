from unittest                                                                            import TestCase
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.utils.Objects                                                           import base_classes

from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client import Cache__Service__Fast_API__Client
from mgraph_ai_service_graph.service.caching.Graph__Cache__Client                        import Graph__Cache__Client


class test_Graph__Cache__Client(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cache_client = Graph__Cache__Client()

    def test__init__(self):                                                              # Test auto-initialization
        with Graph__Cache__Client() as _:
            assert type(_)              is Graph__Cache__Client
            assert base_classes(_)      == [Type_Safe, object]
            assert type(_.cache_client) is Cache__Service__Fast_API__Client                                            # No client injected by default

    def test__method_signatures(self):                                                   # Test all methods exist
        with Graph__Cache__Client() as _:
            # Check all expected methods exist
            assert hasattr(_, 'store_graph')
            assert hasattr(_, 'retrieve_graph')
            assert hasattr(_, 'delete_graph')
            assert hasattr(_, 'graph_exists')
            
            # All should be callable
            assert callable(_.store_graph)
            assert callable(_.retrieve_graph)
            assert callable(_.delete_graph)
            assert callable(_.graph_exists)

    # todo: add methods that actually test the methods from Graph__Cache__Client