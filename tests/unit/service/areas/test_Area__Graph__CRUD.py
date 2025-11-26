from unittest                                                                            import TestCase
from osbot_utils.testing.__                                                              import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                     import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                    import Random_Guid
from osbot_utils.utils.Objects                                                           import base_classes
from mgraph_ai_service_graph.service.areas.Area__Graph__CRUD                             import Area__Graph__CRUD
from mgraph_ai_service_graph.service.graph.Graph__Service                                import Graph__Service
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Request           import Schema__Graph__Create__Request
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Response          import Schema__Graph__Create__Response
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Request              import Schema__Graph__Get__Request
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Response             import Schema__Graph__Get__Response


class test_Area__Graph__CRUD(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.area_crud = Area__Graph__CRUD()

    def test__init__(self):                                                              # Test auto-initialization
        with Area__Graph__CRUD() as _:
            assert type(_)               is Area__Graph__CRUD
            assert base_classes(_)       == [Type_Safe, object]
            assert type(_.graph_service) is Graph__Service

    def test__graph_service_dependency(self):                                            # Test graph service is injected
        with Area__Graph__CRUD() as _:
            assert _.graph_service is not None
            assert type(_.graph_service) is Graph__Service

    def test__method_signatures(self):                                                   # Test all methods exist
        with Area__Graph__CRUD() as _:
            # Check all expected methods exist
            assert hasattr(_, 'create_graph')
            assert hasattr(_, 'get_graph')
            assert hasattr(_, 'delete_graph')
            assert hasattr(_, 'graph_exists')

            # All should be callable
            assert callable(_.create_graph)
            assert callable(_.get_graph)
            assert callable(_.delete_graph)
            assert callable(_.graph_exists)

    def test__create_graph__method_signature(self):                                      # Test create_graph signature
        with Area__Graph__CRUD() as _:
            import inspect
            sig = inspect.signature(_.create_graph)
            params = list(sig.parameters.values())

            # Should have exactly 1 request parameter
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Create__Request
            assert sig.return_annotation == Schema__Graph__Create__Response

    def test__get_graph__method_signature(self):                                         # Test get_graph signature
        with Area__Graph__CRUD() as _:
            import inspect
            sig = inspect.signature(_.get_graph)
            params = list(sig.parameters.values())

            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Get__Request
            assert sig.return_annotation == Schema__Graph__Get__Response

    def test__delete_graph__method_signature(self):                                      # Test delete_graph signature
        with Area__Graph__CRUD() as _:
            import inspect
            sig = inspect.signature(_.delete_graph)
            params = list(sig.parameters.values())

            assert len(params) == 2
            assert params[0].name == 'graph_id'
            assert params[1].name == 'namespace'

    def test__graph_exists__method_signature(self):                                      # Test graph_exists signature
        with Area__Graph__CRUD() as _:
            import inspect
            sig = inspect.signature(_.graph_exists)
            params = list(sig.parameters.values())

            assert len(params) == 2
            assert params[0].name == 'graph_id'
            assert params[1].name == 'namespace'