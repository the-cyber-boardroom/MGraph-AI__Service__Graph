from unittest                                                                            import TestCase
from osbot_utils.testing.__                                                              import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.utils.Objects                                                           import base_classes
from osbot_fast_api.api.routes.Fast_API__Routes                                          import Fast_API__Routes
from mgraph_ai_service_graph.fast_api.routes.Routes__Graph                               import Routes__Graph, TAG__ROUTES_GRAPH
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Request           import Schema__Graph__Create__Request
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Response          import Schema__Graph__Create__Response
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Request              import Schema__Graph__Get__Request
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Response             import Schema__Graph__Get__Response
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Node__Request         import Schema__Graph__Add_Node__Request
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Node__Response        import Schema__Graph__Add_Node__Response
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Edge__Request         import Schema__Graph__Add_Edge__Request
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Edge__Response        import Schema__Graph__Add_Edge__Response
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Request      import Schema__Graph__Find_Nodes__Request
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Response     import Schema__Graph__Find_Nodes__Response
from mgraph_ai_service_graph.service.areas.Area__Graph__CRUD                             import Area__Graph__CRUD
from mgraph_ai_service_graph.service.areas.Area__Graph__Edit                             import Area__Graph__Edit
from mgraph_ai_service_graph.service.areas.Area__Graph__Query                            import Area__Graph__Query


class test_Routes__Graph(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Routes__Graph() as _:
            assert type(_)             is Routes__Graph
            assert base_classes(_)     == [Fast_API__Routes, Type_Safe, object]
            assert _.tag               == TAG__ROUTES_GRAPH
            assert _.tag               == 'graph'
            assert type(_.area_crud)   is Area__Graph__CRUD
            assert type(_.area_edit)   is Area__Graph__Edit
            assert type(_.area_query)  is Area__Graph__Query

    def test__tag_constant(self):                                                        # Test tag constant
        assert TAG__ROUTES_GRAPH == 'graph'

    def test__area_dependencies(self):                                                   # Test area classes are injected
        with Routes__Graph() as _:
            # All area classes should be initialized
            assert _.area_crud   is not None
            assert _.area_edit   is not None
            assert _.area_query  is not None

            # Check correct types
            assert type(_.area_crud)  is Area__Graph__CRUD
            assert type(_.area_edit)  is Area__Graph__Edit
            assert type(_.area_query) is Area__Graph__Query

    def test__create_method_signature(self):                                             # Test create method exists with correct signature
        with Routes__Graph() as _:
            assert hasattr(_, 'create')
            assert callable(_.create)

            # Method should accept Schema__Graph__Create__Request
            import inspect
            sig = inspect.signature(_.create)
            params = list(sig.parameters.values())
            assert len(params)                       == 1
            assert params[0].name                    == 'request'
            assert params[0].annotation              == Schema__Graph__Create__Request
            assert sig.return_annotation             == Schema__Graph__Create__Response

    def test__get_by_id_method_signature(self):                                          # Test get__by_id__graph_id method exists
        with Routes__Graph() as _:
            assert hasattr(_, 'get__by_id__graph_id')
            assert callable(_.get__by_id__graph_id)

    def test__add_node_method_signature(self):                                           # Test add__node method exists
        with Routes__Graph() as _:
            assert hasattr(_, 'add__node')
            assert callable(_.add__node)

            import inspect
            sig = inspect.signature(_.add__node)
            params = list(sig.parameters.values())
            assert len(params)           == 1
            assert params[0].annotation  == Schema__Graph__Add_Node__Request
            assert sig.return_annotation == Schema__Graph__Add_Node__Response

    def test__add_edge_method_signature(self):                                           # Test add__edge method exists
        with Routes__Graph() as _:
            assert hasattr(_, 'add__edge')
            assert callable(_.add__edge)

            import inspect
            sig = inspect.signature(_.add__edge)
            params = list(sig.parameters.values())
            assert len(params)           == 1
            assert params[0].annotation  == Schema__Graph__Add_Edge__Request
            assert sig.return_annotation == Schema__Graph__Add_Edge__Response

    def test__find_nodes_method_signature(self):                                         # Test find__nodes method exists
        with Routes__Graph() as _:
            assert hasattr(_, 'find__nodes')
            assert callable(_.find__nodes)

            import inspect
            sig = inspect.signature(_.find__nodes)
            params = list(sig.parameters.values())
            assert len(params)           == 1
            assert params[0].annotation  == Schema__Graph__Find_Nodes__Request
            assert sig.return_annotation == Schema__Graph__Find_Nodes__Response

    def test__setup_routes(self):                                                        # Test setup_routes method
        with Routes__Graph() as _:
            assert hasattr(_, 'setup_routes')
            assert callable(_.setup_routes)

            result = _.setup_routes()
            assert result is _                                                           # Returns self for chaining