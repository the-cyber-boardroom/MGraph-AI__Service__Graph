import inspect
from unittest                                                                               import TestCase
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.utils.Objects                                                              import base_classes
from mgraph_ai_service_graph.service.areas.Area__Graph__Query                               import Area__Graph__Query
from mgraph_ai_service_graph.service.graph.Graph__Service                                   import Graph__Service


# todo: add tests that actually test the Graph__Query logic
class test_Area__Graph__Query(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.area_query = Area__Graph__Query()

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization
        with Area__Graph__Query() as _:
            assert type(_)               is Area__Graph__Query
            assert base_classes(_)       == [Type_Safe, object]
            assert type(_.graph_service) is Graph__Service

    def test__graph_service_dependency(self):                                               # Test graph service is injected
        with Area__Graph__Query() as _:
            assert _.graph_service is not None
            assert type(_.graph_service) is Graph__Service

    # ═══════════════════════════════════════════════════════════════════════════════
    # Method Existence Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__method_signatures(self):                                                      # Test all methods exist
        with Area__Graph__Query() as _:
            assert hasattr(_, 'find_nodes_by_type')                                         # Check all expected methods exist
            assert hasattr(_, 'find_node_by_id')
            assert hasattr(_, 'get_neighbors')
            assert hasattr(_, 'find_edges_by_type')

            assert callable(_.find_nodes_by_type)                                           # All should be callable
            assert callable(_.find_node_by_id)
            assert callable(_.get_neighbors)
            assert callable(_.find_edges_by_type)

