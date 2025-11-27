from unittest                                                                               import TestCase
from osbot_utils.testing.__                                                                 import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.utils.Objects                                                              import base_classes
from osbot_fast_api.api.routes.Fast_API__Routes                                             import Fast_API__Routes
from mgraph_ai_service_graph.fast_api.routes.Routes__Graph__Edit                            import Routes__Graph__Edit
from mgraph_ai_service_graph.fast_api.routes.Routes__Graph__Edit                            import TAG__ROUTES_GRAPH_EDIT
from mgraph_ai_service_graph.fast_api.routes.Routes__Graph__Edit                            import ROUTES_PATHS__GRAPH_EDIT
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Node__Request            import Schema__Graph__Add_Node__Request
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Node__Response           import Schema__Graph__Add_Node__Response
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Edge__Request            import Schema__Graph__Add_Edge__Request
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Edge__Response           import Schema__Graph__Add_Edge__Response
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Delete_Node__Response        import Schema__Graph__Delete_Node__Response
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Delete_Edge__Response        import Schema__Graph__Delete_Edge__Response
from mgraph_ai_service_graph.service.areas.Area__Graph__Edit                                import Area__Graph__Edit


class test_Routes__Graph__Edit(TestCase):

    def test__init__(self):                                                                 # Test auto-initialization
        with Routes__Graph__Edit() as _:
            assert type(_)            is Routes__Graph__Edit
            assert base_classes(_)    == [Fast_API__Routes, Type_Safe, object]
            assert _.tag              == TAG__ROUTES_GRAPH_EDIT
            assert _.tag              == 'graph-edit'
            assert type(_.area_edit)  is Area__Graph__Edit

    def test__tag_constant(self):                                                           # Test tag constant
        assert TAG__ROUTES_GRAPH_EDIT == 'graph-edit'

    def test__routes_paths_constant(self):                                                  # Test routes paths constant
        assert ROUTES_PATHS__GRAPH_EDIT == [ '/graph-edit/add/node'                         ,
                                             '/graph-edit/add/edge'                         ,
                                             '/graph-edit/delete/node/{graph_id}/{node_id}' ,
                                             '/graph-edit/delete/edge/{graph_id}/{edge_id}' ]

    def test__area_dependency(self):                                                        # Test area class is injected
        with Routes__Graph__Edit() as _:
            assert _.area_edit is not None
            assert type(_.area_edit) is Area__Graph__Edit

    def test__add_node_method_signature(self):                                              # Test add__node method exists
        with Routes__Graph__Edit() as _:
            assert hasattr(_, 'add__node')
            assert callable(_.add__node)

            import inspect
            sig    = inspect.signature(_.add__node)
            params = list(sig.parameters.values())
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Add_Node__Request
            assert sig.return_annotation == Schema__Graph__Add_Node__Response

    def test__add_edge_method_signature(self):                                              # Test add__edge method exists
        with Routes__Graph__Edit() as _:
            assert hasattr(_, 'add__edge')
            assert callable(_.add__edge)

            import inspect
            sig    = inspect.signature(_.add__edge)
            params = list(sig.parameters.values())
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Add_Edge__Request
            assert sig.return_annotation == Schema__Graph__Add_Edge__Response

    def test__delete_node_method_signature(self):                                           # Test delete__node__graph_id__node_id method exists
        with Routes__Graph__Edit() as _:
            assert hasattr(_, 'delete__node__graph_id__node_id')
            assert callable(_.delete__node__graph_id__node_id)

            import inspect
            sig    = inspect.signature(_.delete__node__graph_id__node_id)
            params = list(sig.parameters.values())
            assert len(params)           == 2
            assert params[0].name        == 'graph_id'
            assert params[1].name        == 'node_id'
            assert sig.return_annotation == Schema__Graph__Delete_Node__Response

    def test__delete_edge_method_signature(self):                                           # Test delete__edge__graph_id__edge_id method exists
        with Routes__Graph__Edit() as _:
            assert hasattr(_, 'delete__edge__graph_id__edge_id')
            assert callable(_.delete__edge__graph_id__edge_id)

            import inspect
            sig    = inspect.signature(_.delete__edge__graph_id__edge_id)
            params = list(sig.parameters.values())
            assert len(params)           == 2
            assert params[0].name        == 'graph_id'
            assert params[1].name        == 'edge_id'
            assert sig.return_annotation == Schema__Graph__Delete_Edge__Response

    def test__setup_routes(self):                                                           # Test setup_routes method
        with Routes__Graph__Edit() as _:
            assert hasattr(_, 'setup_routes')
            assert callable(_.setup_routes)

            result = _.setup_routes()
            assert result is _                                                              # Returns self for chaining
