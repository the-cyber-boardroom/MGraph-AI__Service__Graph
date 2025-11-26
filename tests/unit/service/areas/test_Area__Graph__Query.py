from unittest                                                                            import TestCase
from osbot_utils.testing.__                                                              import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.utils.Objects                                                           import base_classes
from mgraph_ai_service_graph.service.areas.Area__Graph__Query                            import Area__Graph__Query
from mgraph_ai_service_graph.service.graph.Graph__Service                                import Graph__Service
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Request      import Schema__Graph__Find_Nodes__Request
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Response     import Schema__Graph__Find_Nodes__Response


class test_Area__Graph__Query(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.area_query = Area__Graph__Query()

    def test__init__(self):                                                              # Test auto-initialization
        with Area__Graph__Query() as _:
            assert type(_)               is Area__Graph__Query
            assert base_classes(_)       == [Type_Safe, object]
            assert type(_.graph_service) is Graph__Service

    def test__graph_service_dependency(self):                                            # Test graph service is injected
        with Area__Graph__Query() as _:
            assert _.graph_service is not None
            assert type(_.graph_service) is Graph__Service

    def test__method_signatures(self):                                                   # Test all methods exist
        with Area__Graph__Query() as _:
            # Check all expected methods exist
            assert hasattr(_, 'find_nodes_by_type')
            assert hasattr(_, 'find_node_by_id')
            assert hasattr(_, 'get_neighbors')
            assert hasattr(_, 'find_edges_by_type')

            # All should be callable
            assert callable(_.find_nodes_by_type)
            assert callable(_.find_node_by_id)
            assert callable(_.get_neighbors)
            assert callable(_.find_edges_by_type)

    def test__find_nodes_by_type__method_signature(self):                                # Test find_nodes_by_type signature
        with Area__Graph__Query() as _:
            import inspect
            sig = inspect.signature(_.find_nodes_by_type)
            params = list(sig.parameters.values())

            # Should have exactly 1 request parameter
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Find_Nodes__Request
            assert sig.return_annotation == Schema__Graph__Find_Nodes__Response

    def test__find_node_by_id__method_signature(self):                                   # Test find_node_by_id signature
        with Area__Graph__Query() as _:
            import inspect
            sig = inspect.signature(_.find_node_by_id)
            params = list(sig.parameters.values())

            assert len(params) == 2
            assert params[0].name == 'graph_id'
            assert params[1].name == 'node_id'

    def test__get_neighbors__method_signature(self):                                     # Test get_neighbors signature
        with Area__Graph__Query() as _:
            import inspect
            sig = inspect.signature(_.get_neighbors)
            params = list(sig.parameters.values())

            assert len(params) == 2
            assert params[0].name == 'graph_id'
            assert params[1].name == 'node_id'

    def test__find_edges_by_type__method_signature(self):                                # Test find_edges_by_type signature
        with Area__Graph__Query() as _:
            import inspect
            sig = inspect.signature(_.find_edges_by_type)
            params = list(sig.parameters.values())

            assert len(params) == 2
            assert params[0].name == 'graph_id'
            assert params[1].name == 'edge_type'