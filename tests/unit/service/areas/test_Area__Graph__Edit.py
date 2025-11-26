from unittest                                                                            import TestCase
from osbot_utils.testing.__                                                              import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.utils.Objects                                                           import base_classes
from mgraph_ai_service_graph.service.areas.Area__Graph__Edit                             import Area__Graph__Edit
from mgraph_ai_service_graph.service.graph.Graph__Service                                import Graph__Service
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Node__Request         import Schema__Graph__Add_Node__Request
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Node__Response        import Schema__Graph__Add_Node__Response
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Edge__Request         import Schema__Graph__Add_Edge__Request
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Edge__Response        import Schema__Graph__Add_Edge__Response


class test_Area__Graph__Edit(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.area_edit = Area__Graph__Edit()

    def test__init__(self):                                                              # Test auto-initialization
        with Area__Graph__Edit() as _:
            assert type(_)               is Area__Graph__Edit
            assert base_classes(_)       == [Type_Safe, object]
            assert type(_.graph_service) is Graph__Service

    def test__graph_service_dependency(self):                                            # Test graph service is injected
        with Area__Graph__Edit() as _:
            assert _.graph_service is not None
            assert type(_.graph_service) is Graph__Service

    def test__method_signatures(self):                                                   # Test all methods exist
        with Area__Graph__Edit() as _:
            # Check all expected methods exist
            assert hasattr(_, 'add_node')
            assert hasattr(_, 'add_edge')
            assert hasattr(_, 'delete_node')
            assert hasattr(_, 'delete_edge')

            # All should be callable
            assert callable(_.add_node)
            assert callable(_.add_edge)
            assert callable(_.delete_node)
            assert callable(_.delete_edge)

    def test__add_node__method_signature(self):                                          # Test add_node signature
        with Area__Graph__Edit() as _:
            import inspect
            sig = inspect.signature(_.add_node)
            params = list(sig.parameters.values())

            # Should have exactly 1 request parameter
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Add_Node__Request
            assert sig.return_annotation == Schema__Graph__Add_Node__Response

    def test__add_edge__method_signature(self):                                          # Test add_edge signature
        with Area__Graph__Edit() as _:
            import inspect
            sig = inspect.signature(_.add_edge)
            params = list(sig.parameters.values())

            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Add_Edge__Request
            assert sig.return_annotation == Schema__Graph__Add_Edge__Response

    def test__delete_node__method_signature(self):                                       # Test delete_node signature
        with Area__Graph__Edit() as _:
            import inspect
            sig = inspect.signature(_.delete_node)
            params = list(sig.parameters.values())

            assert len(params) == 2
            assert params[0].name == 'graph_id'
            assert params[1].name == 'node_id'

    def test__delete_edge__method_signature(self):                                       # Test delete_edge signature
        with Area__Graph__Edit() as _:
            import inspect
            sig = inspect.signature(_.delete_edge)
            params = list(sig.parameters.values())

            assert len(params) == 2
            assert params[0].name == 'graph_id'
            assert params[1].name == 'edge_id'