from unittest                                                                               import TestCase
from osbot_utils.testing.__                                                                 import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.utils.Objects                                                              import base_classes
from osbot_fast_api.api.routes.Fast_API__Routes                                             import Fast_API__Routes
from mgraph_ai_service_graph.fast_api.routes.Routes__Graph__Query                           import Routes__Graph__Query
from mgraph_ai_service_graph.fast_api.routes.Routes__Graph__Query                           import TAG__ROUTES_GRAPH_QUERY
from mgraph_ai_service_graph.fast_api.routes.Routes__Graph__Query                           import ROUTES_PATHS__GRAPH_QUERY
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Request         import Schema__Graph__Find_Nodes__Request
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Response        import Schema__Graph__Find_Nodes__Response
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Node__Response         import Schema__Graph__Find_Node__Response
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Edges__Response        import Schema__Graph__Find_Edges__Response
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Neighbors__Response         import Schema__Graph__Neighbors__Response
from mgraph_ai_service_graph.service.areas.Area__Graph__Query                               import Area__Graph__Query


class test_Routes__Graph__Query(TestCase):

    def test__init__(self):                                                                 # Test auto-initialization
        with Routes__Graph__Query() as _:
            assert type(_)             is Routes__Graph__Query
            assert base_classes(_)     == [Fast_API__Routes, Type_Safe, object]
            assert _.tag               == TAG__ROUTES_GRAPH_QUERY
            assert _.tag               == 'graph-query'
            assert type(_.area_query)  is Area__Graph__Query

    def test__tag_constant(self):                                                           # Test tag constant
        assert TAG__ROUTES_GRAPH_QUERY == 'graph-query'

    def test__routes_paths_constant(self):                                                  # Test routes paths constant
        assert ROUTES_PATHS__GRAPH_QUERY == [ '/graph-query/find/nodes',
                                              '/graph-query/find/node',
                                              '/graph-query/find/edges',
                                              '/graph-query/neighbors']

    def test__area_dependency(self):                                                        # Test area class is injected
        with Routes__Graph__Query() as _:
            assert _.area_query is not None
            assert type(_.area_query) is Area__Graph__Query

    def test__find_nodes_method_signature(self):                                            # Test find__nodes method exists
        with Routes__Graph__Query() as _:
            assert hasattr(_, 'find__nodes')
            assert callable(_.find__nodes)

            import inspect
            sig    = inspect.signature(_.find__nodes)
            params = list(sig.parameters.values())
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Find_Nodes__Request
            assert sig.return_annotation == Schema__Graph__Find_Nodes__Response

    def test__setup_routes(self):                                                           # Test setup_routes method
        with Routes__Graph__Query() as _:
            assert hasattr(_, 'setup_routes')
            assert callable(_.setup_routes)

            result = _.setup_routes()
            assert result is _                                                              # Returns self for chaining
