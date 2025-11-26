from unittest                                                                            import TestCase
from osbot_utils.testing.__                                                              import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.utils.Objects                                                           import base_classes
from mgraph_ai_service_graph.service.graph.Graph__Service                                import Graph__Service
from mgraph_ai_service_graph.service.caching.Graph__Cache__Client                        import Graph__Cache__Client


class test_Graph__Service(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.graph_service = Graph__Service()

    def test__init__(self):                                                              # Test auto-initialization
        with Graph__Service() as _:
            assert type(_)              is Graph__Service
            assert base_classes(_)      == [Type_Safe, object]
            assert type(_.cache_client) is Graph__Cache__Client

    def test__cache_client_dependency(self):                                             # Test cache client is initialized
        with Graph__Service() as _:
            assert _.cache_client is not None
            assert type(_.cache_client) is Graph__Cache__Client

    def test__create_new_graph(self):                                                    # Test creating a new empty graph
        with self.graph_service as _:
            graph = _.create_new_graph()

            assert graph is not None
            # Note: MGraph type check would require mgraph_db installed
            # Just verify it returns something

    def test__create_new_graph__multiple_calls(self):                                    # Test multiple graphs are independent
        with self.graph_service as _:
            graph1 = _.create_new_graph()
            graph2 = _.create_new_graph()

            # Should be different instances
            assert graph1 is not graph2

    def test__method_signatures(self):                                                   # Test all methods exist with correct signatures
        with Graph__Service() as _:
            # Check all expected methods exist
            assert hasattr(_, 'create_new_graph')
            assert hasattr(_, 'get_or_create_graph')
            assert hasattr(_, 'save_graph')
            assert hasattr(_, 'delete_graph')
            assert hasattr(_, 'graph_exists')

            # All should be callable
            assert callable(_.create_new_graph)
            assert callable(_.get_or_create_graph)
            assert callable(_.save_graph)
            assert callable(_.delete_graph)
            assert callable(_.graph_exists)

    def test__get_or_create_graph__method_signature(self):                               # Test get_or_create_graph signature
        with Graph__Service() as _:
            import inspect
            sig = inspect.signature(_.get_or_create_graph)
            params = list(sig.parameters.values())

            # Should have graph_id and namespace parameters
            assert len(params) == 2
            assert params[0].name == 'graph_id'
            assert params[1].name == 'namespace'
            assert params[1].default == 'graphs'                                         # Default namespace

    def test__save_graph__method_signature(self):                                        # Test save_graph signature
        with Graph__Service() as _:
            import inspect
            sig = inspect.signature(_.save_graph)
            params = list(sig.parameters.values())

            # Should have graph_id, graph, and namespace parameters
            assert len(params) == 3
            assert params[0].name == 'graph_id'
            assert params[1].name == 'graph'
            assert params[2].name == 'namespace'
            assert params[2].default == 'graphs'

    def test__delete_graph__method_signature(self):                                      # Test delete_graph signature
        with Graph__Service() as _:
            import inspect
            sig = inspect.signature(_.delete_graph)
            params = list(sig.parameters.values())

            assert len(params) == 2
            assert params[0].name == 'graph_id'
            assert params[1].name == 'namespace'
            assert params[1].default == 'graphs'

    def test__graph_exists__method_signature(self):                                      # Test graph_exists signature
        with Graph__Service() as _:
            import inspect
            sig = inspect.signature(_.graph_exists)
            params = list(sig.parameters.values())

            assert len(params) == 2
            assert params[0].name == 'graph_id'
            assert params[1].name == 'namespace'
            assert params[1].default == 'graphs'