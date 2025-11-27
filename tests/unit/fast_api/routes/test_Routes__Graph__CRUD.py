from unittest                                                                               import TestCase
from osbot_utils.testing.__                                                                 import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.utils.Objects                                                              import base_classes
from osbot_fast_api.api.routes.Fast_API__Routes                                             import Fast_API__Routes
from mgraph_ai_service_graph.fast_api.routes.Routes__Graph__CRUD                            import Routes__Graph__CRUD
from mgraph_ai_service_graph.fast_api.routes.Routes__Graph__CRUD                            import TAG__ROUTES_GRAPH_CRUD
from mgraph_ai_service_graph.fast_api.routes.Routes__Graph__CRUD                            import ROUTES_PATHS__GRAPH_CRUD
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Request              import Schema__Graph__Create__Request
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Response             import Schema__Graph__Create__Response
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Response                import Schema__Graph__Get__Response
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Delete__Response             import Schema__Graph__Delete__Response
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Exists__Response             import Schema__Graph__Exists__Response
from mgraph_ai_service_graph.service.areas.Area__Graph__CRUD                                import Area__Graph__CRUD


class test_Routes__Graph__CRUD(TestCase):

    def test__init__(self):                                                                 # Test auto-initialization
        with Routes__Graph__CRUD() as _:
            assert type(_)            is Routes__Graph__CRUD
            assert base_classes(_)    == [Fast_API__Routes, Type_Safe, object]
            assert _.tag              == TAG__ROUTES_GRAPH_CRUD
            assert _.tag              == 'graph-crud'
            assert type(_.area_crud)  is Area__Graph__CRUD

    def test__tag_constant(self):                                                           # Test tag constant
        assert TAG__ROUTES_GRAPH_CRUD == 'graph-crud'

    def test__routes_paths_constant(self):                                                  # Test routes paths constant
        assert ROUTES_PATHS__GRAPH_CRUD == [ '/graph-crud/create'                     ,
                                             '/graph-crud/get/by-id/{graph_id}'       ,
                                             '/graph-crud/get/by-cache-id/{cache_id}' ,
                                             '/graph-crud/delete/{graph_id}'          ,
                                             '/graph-crud/exists/{graph_id}'          ]

    def test__area_dependency(self):                                                        # Test area class is injected
        with Routes__Graph__CRUD() as _:
            assert _.area_crud is not None
            assert type(_.area_crud) is Area__Graph__CRUD

    def test__create_method_signature(self):                                                # Test create method exists with correct signature
        with Routes__Graph__CRUD() as _:
            assert hasattr(_, 'create')
            assert callable(_.create)

            import inspect
            sig    = inspect.signature(_.create)
            params = list(sig.parameters.values())
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Create__Request
            assert sig.return_annotation == Schema__Graph__Create__Response

    def test__get_by_id_method_signature(self):                                             # Test get__by_id__graph_id method exists
        with Routes__Graph__CRUD() as _:
            assert hasattr(_, 'get__by_id__graph_id')
            assert callable(_.get__by_id__graph_id)

            import inspect
            sig    = inspect.signature(_.get__by_id__graph_id)
            params = list(sig.parameters.values())
            assert len(params)           == 2                                               # graph_id and namespace
            assert params[0].name        == 'graph_id'
            assert params[1].name        == 'namespace'
            assert sig.return_annotation == Schema__Graph__Get__Response

    def test__get_by_cache_id_method_signature(self):                                       # Test get__by_cache_id__cache_id method exists
        with Routes__Graph__CRUD() as _:
            assert hasattr(_, 'get__by_cache_id__cache_id')
            assert callable(_.get__by_cache_id__cache_id)

            import inspect
            sig    = inspect.signature(_.get__by_cache_id__cache_id)
            params = list(sig.parameters.values())
            assert len(params)           == 2                                               # cache_id and namespace
            assert params[0].name        == 'cache_id'
            assert params[1].name        == 'namespace'
            assert sig.return_annotation == Schema__Graph__Get__Response

    def test__delete_method_signature(self):                                                # Test delete__graph_id method exists
        with Routes__Graph__CRUD() as _:
            assert hasattr(_, 'delete__graph_id')
            assert callable(_.delete__graph_id)

            import inspect
            sig    = inspect.signature(_.delete__graph_id)
            params = list(sig.parameters.values())
            assert len(params)           == 2                                               # graph_id and namespace
            assert params[0].name        == 'graph_id'
            assert params[1].name        == 'namespace'
            assert sig.return_annotation == Schema__Graph__Delete__Response

    def test__exists_method_signature(self):                                                # Test exists__graph_id method exists
        with Routes__Graph__CRUD() as _:
            assert hasattr(_, 'exists__graph_id')
            assert callable(_.exists__graph_id)

            import inspect
            sig    = inspect.signature(_.exists__graph_id)
            params = list(sig.parameters.values())
            assert len(params)           == 2                                               # graph_id and namespace
            assert params[0].name        == 'graph_id'
            assert params[1].name        == 'namespace'
            assert sig.return_annotation == Schema__Graph__Exists__Response

    def test__setup_routes(self):                                                           # Test setup_routes method
        with Routes__Graph__CRUD() as _:
            assert hasattr(_, 'setup_routes')
            assert callable(_.setup_routes)

            result = _.setup_routes()
            assert result is _                                                              # Returns self for chaining
