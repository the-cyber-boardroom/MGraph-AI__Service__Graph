from unittest                                                                                       import TestCase
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id                     import Safe_Str__Id
from osbot_utils.utils.Objects                                                                      import base_classes
from osbot_fast_api.api.routes.Fast_API__Routes                                                     import Fast_API__Routes
from mgraph_ai_service_graph.fast_api.routes.graph.Routes__Graph__Edit                              import Routes__Graph__Edit
from mgraph_ai_service_graph.fast_api.routes.graph.Routes__Graph__Edit                              import TAG__ROUTES_GRAPH_EDIT
from mgraph_ai_service_graph.schemas.graph_edit.nodes.Schema__Graph__Add_Node__Request              import Schema__Graph__Add_Node__Request
from mgraph_ai_service_graph.schemas.graph_edit.nodes.Schema__Graph__Add_Node__Response             import Schema__Graph__Add_Node__Response
from mgraph_ai_service_graph.schemas.graph_edit.nodes.Schema__Graph__Add_Node__Typed__Request       import Schema__Graph__Add_Node__Typed__Request
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Add_Edge__Request              import Schema__Graph__Add_Edge__Request
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Add_Edge__Response             import Schema__Graph__Add_Edge__Response
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Add_Edge__Typed__Request       import Schema__Graph__Add_Edge__Typed__Request
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Add_Edge__Predicate__Request   import Schema__Graph__Add_Edge__Predicate__Request
from mgraph_ai_service_graph.schemas.graph_edit.values.Schema__Graph__Add_Value__Request            import Schema__Graph__Add_Value__Request
from mgraph_ai_service_graph.schemas.graph_edit.values.Schema__Graph__Add_Value__Response           import Schema__Graph__Add_Value__Response
from mgraph_ai_service_graph.service.areas.Area__Graph__Edit                                        import Area__Graph__Edit
from mgraph_ai_service_graph.service.areas.Area__Graph__CRUD                                        import Area__Graph__CRUD
from mgraph_ai_service_graph.service.areas.Area__Graph__Query                                       import Area__Graph__Query
from mgraph_ai_service_graph.service.caching.Graph__Cache__Client                                   import Graph__Cache__Client
from mgraph_ai_service_graph.service.graph.Graph__Service                                           import Graph__Service
from tests.unit.Graph__Service__Fast_API__Test_Objs                                                 import client_cache_service


class test_Routes__Graph__Edit(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cache_client, cls.cache_service = client_cache_service()                        # Create in-memory cache service
        cls.graph_cache_client              = Graph__Cache__Client(cache_client=cls.cache_client)
        cls.graph_service                   = Graph__Service(graph_cache_client=cls.graph_cache_client)

        cls.area_crud                       = Area__Graph__CRUD (graph_service=cls.graph_service)
        cls.area_edit                       = Area__Graph__Edit (graph_service=cls.graph_service)
        cls.area_query                      = Area__Graph__Query(graph_service=cls.graph_service)

        cls.routes                          = Routes__Graph__Edit(area_edit=cls.area_edit)
        cls.test_namespace                  = Safe_Str__Id('test-routes-edit')

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization
        with Routes__Graph__Edit() as _:
            assert type(_)            is Routes__Graph__Edit
            assert base_classes(_)    == [Fast_API__Routes, Type_Safe, object]
            assert _.tag              == TAG__ROUTES_GRAPH_EDIT
            assert _.tag              == 'graph-edit'
            assert type(_.area_edit)  is Area__Graph__Edit

    def test__tag_constant(self):                                                           # Test tag constant
        assert TAG__ROUTES_GRAPH_EDIT == 'graph-edit'

    def test__area_dependency(self):                                                        # Test area class is injected
        with self.routes as _:
            assert _.area_edit is not None
            assert type(_.area_edit) is Area__Graph__Edit
            assert _.area_edit       is self.area_edit                                      # Same instance as setup

    # ═══════════════════════════════════════════════════════════════════════════════
    # Node Route Method Signature Tests
    # ═══════════════════════════════════════════════════════════════════════════════

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

    def test__add_node_typed_method_signature(self):                                        # Test add__node__typed method exists
        with Routes__Graph__Edit() as _:
            assert hasattr(_, 'add__node__typed')
            assert callable(_.add__node__typed)

            import inspect
            sig    = inspect.signature(_.add__node__typed)
            params = list(sig.parameters.values())
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Add_Node__Typed__Request
            assert sig.return_annotation == Schema__Graph__Add_Node__Response

    # ═══════════════════════════════════════════════════════════════════════════════
    # Value Route Method Signature Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__add_value_method_signature(self):                                             # Test add__value method exists
        with Routes__Graph__Edit() as _:
            assert hasattr(_, 'add__value')
            assert callable(_.add__value)

            import inspect
            sig    = inspect.signature(_.add__value)
            params = list(sig.parameters.values())
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Add_Value__Request
            assert sig.return_annotation == Schema__Graph__Add_Value__Response

    def test__add_value_get_or_create_method_signature(self):                               # Test add__value__get_or_create method exists
        with Routes__Graph__Edit() as _:
            assert hasattr(_, 'add__value__get_or_create')
            assert callable(_.add__value__get_or_create)

            import inspect
            sig    = inspect.signature(_.add__value__get_or_create)
            params = list(sig.parameters.values())
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Add_Value__Request
            assert sig.return_annotation == Schema__Graph__Add_Value__Response

    # ═══════════════════════════════════════════════════════════════════════════════
    # Edge Route Method Signature Tests
    # ═══════════════════════════════════════════════════════════════════════════════

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

    def test__add_edge_typed_method_signature(self):                                        # Test add__edge__typed method exists
        with Routes__Graph__Edit() as _:
            assert hasattr(_, 'add__edge__typed')
            assert callable(_.add__edge__typed)

            import inspect
            sig    = inspect.signature(_.add__edge__typed)
            params = list(sig.parameters.values())
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Add_Edge__Typed__Request
            assert sig.return_annotation == Schema__Graph__Add_Edge__Response

    def test__add_edge_predicate_method_signature(self):                                    # Test add__edge__predicate method exists
        with Routes__Graph__Edit() as _:
            assert hasattr(_, 'add__edge__predicate')
            assert callable(_.add__edge__predicate)

            import inspect
            sig    = inspect.signature(_.add__edge__predicate)
            params = list(sig.parameters.values())
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Add_Edge__Predicate__Request
            assert sig.return_annotation == Schema__Graph__Add_Edge__Response

    # ═══════════════════════════════════════════════════════════════════════════════
    # Delete Route Method Signature Tests
    # ═══════════════════════════════════════════════════════════════════════════════


    def test__setup_routes(self):                                                           # Test setup_routes method
        from fastapi import FastAPI
        with Routes__Graph__Edit(app=FastAPI()) as _:
            assert hasattr(_, 'setup_routes')
            assert callable(_.setup_routes)

            result = _.setup_routes()
            assert result is _                                                              # Returns self for chaining