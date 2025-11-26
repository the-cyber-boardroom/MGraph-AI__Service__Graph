from unittest                                                                            import TestCase
from osbot_utils.testing.__                                                              import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.utils.Objects                                                           import base_classes
from mgraph_ai_service_graph.service.caching.Graph__Cache__Client                        import Graph__Cache__Client


class test_Graph__Cache__Client(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cache_client = Graph__Cache__Client()

    def test__init__(self):                                                              # Test auto-initialization
        with Graph__Cache__Client() as _:
            assert type(_)            is Graph__Cache__Client
            assert base_classes(_)    == [Type_Safe, object]
            assert _.cache_client     is None                                            # No client injected by default

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

    def test__store_graph__method_signature(self):                                       # Test store_graph signature
        with Graph__Cache__Client() as _:
            import inspect
            sig = inspect.signature(_.store_graph)
            params = list(sig.parameters.values())
            
            # Should have graph_id, graph, and namespace parameters
            assert len(params) == 3
            assert params[0].name == 'graph_id'
            assert params[1].name == 'graph'
            assert params[2].name == 'namespace'
            assert params[2].default == 'graphs'                                         # Default namespace

    def test__retrieve_graph__method_signature(self):                                    # Test retrieve_graph signature
        with Graph__Cache__Client() as _:
            import inspect
            sig = inspect.signature(_.retrieve_graph)
            params = list(sig.parameters.values())
            
            assert len(params) == 2
            assert params[0].name == 'graph_id'
            assert params[1].name == 'namespace'
            assert params[2].default == 'graphs'

    def test__delete_graph__method_signature(self):                                      # Test delete_graph signature
        with Graph__Cache__Client() as _:
            import inspect
            sig = inspect.signature(_.delete_graph)
            params = list(sig.parameters.values())
            
            assert len(params) == 2
            assert params[0].name == 'graph_id'
            assert params[1].name == 'namespace'
            assert params[2].default == 'graphs'

    def test__graph_exists__method_signature(self):                                      # Test graph_exists signature
        with Graph__Cache__Client() as _:
            import inspect
            sig = inspect.signature(_.graph_exists)
            params = list(sig.parameters.values())
            
            assert len(params) == 2
            assert params[0].name == 'graph_id'
            assert params[1].name == 'namespace'
            assert params[2].default == 'graphs'